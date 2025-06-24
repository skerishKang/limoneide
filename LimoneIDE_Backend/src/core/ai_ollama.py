from src.core.ai_base import BaseAIHandler
try:
    from ollama import Client as OllamaClient
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

class OllamaHandler(BaseAIHandler):
    """0로컬 Ollama 핸들러"""
    def __init__(self):
        if OLLAMA_AVAILABLE:
            self.client = OllamaClient()
        else:
            self.client = None

    def is_available(self) -> bool:
        return self.client is not None

    async def generate_response(self, prompt: str) -> str:
        if not self.is_available():
            raise Exception("Ollama가 설치되어 있지 않습니다.")
        response = self.client.chat(model='llama2', messages=[
            {'role': 'user', 'content': prompt}
        ])
        return response['message']['content'] 