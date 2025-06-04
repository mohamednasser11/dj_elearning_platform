import json
from urllib.parse import parse_qs
from channels.consumer import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import asyncio
from chat.models import ChatMessage, ChatSession
from tools.AI.AI_model_service import AIModelService


MAX_HISTORY_LENGTH = 20


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        self.user = self.scope["user"]
        # self.course =

        self.session = await self._get_session()
        if self.session and (await self._is_session_owner()):
            await self._send_error("Unauthorized")
            return

        if self.session:
            history = list(await self._get_history())
            self.history = history[:MAX_HISTORY_LENGTH]
            await self._send("session.resume", {"history": history})
        else:
            self.history = []

    async def disconnect(self, code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        try:
            if not self.session:
                self.session = await self._create_session()
                await self._send("session.new", {"session_id": str(self.session.id)})

            if bytes_data:
                text_data = bytes_data.decode("utf-8")

            if not text_data:
                await self._send_error("Empty message")
                return

            text_data_json = json.loads(text_data)
            inbound_message = text_data_json.get("message", "")

            if not inbound_message.strip():
                await self._send_error("Empty message")
                return

            await self._append_history("user", inbound_message)

            await self._send("stream.start")

            model = AIModelService()
            stream = model.chat(self.history)

            outbound_message = ""
            for chunk in stream:
                response = chunk["message"]["content"]
                outbound_message += response
                await self._send_message("stream.chunk", response)
                await asyncio.sleep(0)  # to force yield

            await self._append_history("assistant", outbound_message)

            await self._send("stream.end")

        except UnicodeDecodeError:
            await self._send_error("Invalid binary data format")
        except json.JSONDecodeError:
            await self._send_error("Invalid JSON format")
        except Exception as e:
            await self._send_error(str(e))

    @database_sync_to_async
    def _get_session(self):
        query_string = self.scope.get("query_string", b"").decode()
        query_params = parse_qs(query_string)
        session_id = query_params.get("session_id", [None])[0]
        if session_id:
            return ChatSession.objects.get(id=session_id, user=self.user)
        else:
            return None

    @database_sync_to_async
    def _create_session(self):
        return ChatSession.objects.create(user=self.user)

    @database_sync_to_async
    def _is_session_owner(self):
        return self.session.user != self.user

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
        if len(self.history) > MAX_HISTORY_LENGTH:
            self.history.pop(0)

    async def _send(self, type, data={}):
        await self.send(json.dumps({"type": type, **data}))

    async def _send_message(self, type, message):
        await self._send(type, {"message": message})

    async def _send_error(self, message, code=4000, close=True):
        await self._send_message("error", message)
        if close:
            await self.close(code)
