from ollama import AsyncClient

class OllamaClient:
    def __init__(self, host=None):
        self.host = host or 'http://ollama-server:11434'

    async def chat(self, model='tinyllama', messages=[], stream=False):
        try:
            return (AsyncClient(host=self.host)
                    .chat(model=model, messages=messages, stream=stream))
        except Exception as e:
            print(f"Error during Ollama chat: {e}")
            # Handle the error accordingly, raise or log as needed
            raise
