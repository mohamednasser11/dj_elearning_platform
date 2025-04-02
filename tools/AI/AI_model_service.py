import ollama

class AIModelService:
    def __init__(self):
         self.client = ollama.Client(
            host="http://localhost:11434"
        )

    def generate(self, data, model='gemma3', options=None):
        try:
            response = self.client.generate(prompt= data, model= model, options= options or {})
            return response['response']
        except Exception as e:
            raise Exception(f"Failed to generate response: {e}")