import json
from weakref import WeakValueDictionary
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import asyncio
from tools.AI.AI_model_service import AIModelService


class ChatConsumer(AsyncWebsocketConsumer):
    active_clients = WeakValueDictionary()

    async def connect(self):
        await self.accept()
        self.user = self.scope["user"]
        self.history = []

    async def disconnect(self, code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        async def send(type, message=""):
            await self.send(json.dumps({"type": type, "message": message}))

        try:
            if bytes_data:
                text_data = bytes_data.decode("utf-8")

            if not text_data:
                await send("error", "Empty message")
                await self.close(4000)
                return

            text_data_json = json.loads(text_data)
            inbound_message = text_data_json.get("message", "")

            if not inbound_message.strip():
                await send("error", "Empty message")
                await self.close(4000)
                return

            self.history.append({"role": "user", "content": inbound_message})

            print(self.history)
            model = AIModelService()
            stream = model.chat(self.history)

            await send("started")

            outbound_message = ""
            for chunk in stream:
                response = chunk["message"]["content"]
                outbound_message += response
                await send("streaming", response)
                await asyncio.sleep(0)  # to force yield

            self.history.append({"role": "assistant", "content": outbound_message})

            await send("complete")

        except UnicodeDecodeError:
            await send("error", "Invalid binary data format")
            await self.close(4000)
            return
        except json.JSONDecodeError:
            await send("complete", "Invalid JSON format")
            await self.close(4000)
        except Exception as e:
            await send("complete", str(e))
            await self.close(4000)
