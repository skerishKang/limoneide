from src.core.ai_base import BaseAIHandler
import openai

class OpenAIHandler(BaseAIHandler):
    """OpenAI GPT 핸들러"""
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.client = None
        if api_key:
            self.client = openai.AsyncOpenAI(api_key=api_key)

    def is_available(self) -> bool:
        return self.client is not None

    async def generate_response(self, prompt: str) -> str:
        if not self.is_available():
            raise Exception("OpenAI API 키가 설정되지 않았습니다.")
        response = await self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content 