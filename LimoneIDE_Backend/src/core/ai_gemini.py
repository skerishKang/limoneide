from src.core.ai_base import BaseAIHandler
import google.generativeai as genai

class GeminiHandler(BaseAIHandler):
    """Google Gemini AI 핸들러"""
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.model = None
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')

    def is_available(self) -> bool:
        return self.model is not None

    async def generate_response(self, prompt: str) -> str:
        if not self.is_available():
            raise Exception("Gemini API 키가 설정되지 않았습니다.")
        response = self.model.generate_content(prompt)
        return response.text 