import json
from urllib.parse import parse_qs
from channels.consumer import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import asyncio
from chat.models import ChatMessage, ChatSession
from departments.models.courses_models.course_lesson_models import CoursesLesson
from departments.models.courses_models.course_models import Course
from departments.models.courses_models.user_courses_purchase_model import (
    UserCoursePurchase,
)
from tools.AI.AI_model_service import AIModelService


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_streaming = False
        self.stream_task = None
        self.user = None
        self.course = None
        self.session = None
        self.history = []

    async def connect(self):
        await self.accept()

        self.user = self.scope["user"]
        self.course = await self._get_course()
        if not self.course:
            await self._send_error("Course does not exist")
            return

        if not await self._is_enrolled():
            await self._send_error("User not enrolled")
            return

        if self._has_qs("session_id"):
            self.session = await self._get_session()

            if not self.session:
                await self._send_error("Session does not exist")
                return

            if not await self._is_session_owner():
                await self._send_error("Unauthorized")
                return

            self.history = await self._get_history()
            await self._send("session.resume", {"history": self.history[1:]})
        else:
            self.session = None
            self.history = []

    async def disconnect(self, code):
        if self.stream_task and not self.stream_task.done():
            self.stream_task.cancel()

    async def receive(self, text_data=None, bytes_data=None):
        try:
            if not self.session:
                self.session = await self._create_session()
                await self._append_history(
                    "system", await self._generate_system_prompt()
                )
                self.history = await self._get_history()
                await self._send("session.new", {"session_id": str(self.session.id)})

            if bytes_data:
                text_data = bytes_data.decode("utf-8")

            if not text_data:
                await self._send_error("Empty message")
                return

            text_data_json = json.loads(text_data)

            type = text_data_json.get("type", None)
            if type is None:
                await self._send_error("type not provided")
                return

            data = text_data_json.get("data", None)
            if data is None:
                await self._send_error("data not provided")
                return

            match type:
                case "send":
                    if self.is_streaming and self.stream_task:
                        self.stream_task.cancel()
                        await asyncio.sleep(0.1)

                    message = data.get("message", None)
                    if not message or not message.strip():
                        await self._send_error("Empty message")
                        return

                    await self._append_history("user", message)

                    self.is_streaming = True
                    self.stream_task = asyncio.create_task(
                        self._handle_stream_response()
                    )
                case "cancel":
                    if self.stream_task:
                        self.stream_task.cancel()
                        await asyncio.sleep(0.1)
                    else:
                        await self._send_error("no task to cancel")
                        return
                case _:
                    await self._send_error("invalid type")
                    return

        except UnicodeDecodeError:
            await self._send_error("Invalid binary data format")
        except json.JSONDecodeError:
            await self._send_error("Invalid JSON format")
        except Exception as e:
            await self._send_error(str(e))

    async def _handle_stream_response(self):
        outbound_message = ""
        try:
            await self._send("stream.start")

            model = AIModelService()
            stream = model.chat(self.history)

            async for chunk in self._stream_generator(stream):
                response = chunk["message"]["content"]
                outbound_message += response
                await self._send_message("stream.chunk", response)

                if not self.is_streaming:
                    break

        except asyncio.CancelledError:
            pass
        except Exception as e:
            await self._send_error(str(e))
        finally:
            await self._append_history("assistant", outbound_message)
            await self._send("stream.end")
            self.is_streaming = False
            self.stream_task = None

    async def _stream_generator(self, stream):
        for chunk in stream:
            if not self.is_streaming:
                break
            yield chunk
            await asyncio.sleep(0)

    def _has_qs(self, key):
        query_string = self.scope.get("query_string", b"").decode()
        query_params = parse_qs(query_string)
        return query_params.get(key, [None])[0] is not None

    def _get_from_qs(self, key):
        query_string = self.scope.get("query_string", b"").decode()
        query_params = parse_qs(query_string)
        return query_params.get(key, [None])[0]

    @database_sync_to_async
    def _get_course(self):
        course_id = self._get_from_qs("course_id")
        if course_id:
            try:
                return Course.objects.get(courseId=course_id)
            except Exception:
                return None
        else:
            return None

    @database_sync_to_async
    def _get_session(self):
        try:
            session_id = self._get_from_qs("session_id")
            if session_id:
                return ChatSession.objects.get(
                    id=session_id, user=self.user, course=self.course
                )
            else:
                return None
        except Exception:
            return None

    @database_sync_to_async
    def _create_session(self):
        return ChatSession.objects.create(user=self.user, course=self.course)

    @database_sync_to_async
    def _is_enrolled(self):
        return UserCoursePurchase.objects.filter(
            user=self.user, course=self.course
        ).exists()

    @database_sync_to_async
    def _is_session_owner(self):
        return self.session and self.session.user == self.user

    @database_sync_to_async
    def _get_history(self):
        messages = ChatMessage.objects.filter(session=self.session).order_by(
            "-created_at"
        )
        return [
            {"role": msg.role, "content": msg.content} for msg in reversed(messages)
        ]

    @database_sync_to_async
    def _append_history(self, role, content):
        ChatMessage.objects.create(session=self.session, role=role, content=content)
        self.history.append({"role": role, "content": content})

    async def _send(self, type, data={}):
        await self.send(json.dumps({"type": type, "data": data}))

    async def _send_message(self, type, message):
        await self._send(type, {"message": message})

    async def _send_error(self, message, code=4000, close=True):
        await self._send_message("error", message)
        if close:
            await self.close(code)

    @database_sync_to_async
    def _generate_system_prompt(self):
        lessons = CoursesLesson.objects.filter(courseId=self.course).order_by(
            "created_at"
        )

        lessons_data = []
        for lesson in lessons:
            lessons_data.append(
                {
                    "lesson_title": lesson.title,
                    "lesson_description": lesson.description,
                }
            )

        prompt = f"""
        You are an advanced AI teaching assistant with comprehensive knowledge about all courses and their lesson content. Your capabilities include:

        1. COURSE KNOWLEDGE BASE:
        - Course Title: {self.course.title}
        - Course Description: {self.course.description}
        - Instructor: {self.course.instructorId.first_name} {self.course.instructorId.last_name}
        - Department: {self.course.departmentId.name}

        2. LESSON LIBRARY:
        {json.dumps(lessons_data, indent=4)}

        3. ASSISTANT PROTOCOLS:
        - Always reference specific lesson content when answering questions
        - Break down complex topics using the structured lesson progression
        - Suggest which lessons to review based on the user's question
        - Maintain academic integrity while helping students understand concepts
        - Offer multiple explanations for difficult topics
        - Guide users through the course curriculum in logical sequences
        """

        return prompt
