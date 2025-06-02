import ollama
from decouple import config


class AIModelService:
    def __init__(self):
        self.client = ollama.Client(
            host=f"{config('OLLAMA_HOST')}:{config('OLLAMA_PORT')}"
        )

    def generate(self, prompt, model="gemma3", options=None):
        try:
            response = self.client.generate(
                prompt=prompt, model=model, options=options or {}
            )
            return response["response"]
        except Exception as e:
            raise Exception(f"Failed to generate response: {e}")

    def chat(self, message, model="gemma3", options=None):
        try:
            return self.client.chat(
                model=model,
                messages=[{"role": "user", "content": message}],
                stream=True,
                options=options or {},
            )
        except Exception as e:
            raise Exception(f"Failed to get chat stream: {e}")
