import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import asyncio
from tools.AI.AI_model_service import AIModelService


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        async def send(status, message=""):
            await self.send(json.dumps({"status": status, "message": message}))

        try:
            if bytes_data:
                text_data = bytes_data.decode("utf-8")

            if not text_data:
                await send("error", "Empty message")
                await self.close(4000)
                return

            text_data_json = json.loads(text_data)
            message = text_data_json.get("message", "")

            if not message.strip():
                await send("error", "Empty message")
                await self.close(4000)
                return

            model = AIModelService()
            stream = model.chat(message)

            await send("started")

            for chunk in stream:
                await send("streaming", chunk["message"]["content"])
                await asyncio.sleep(0)  # to force yield

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
