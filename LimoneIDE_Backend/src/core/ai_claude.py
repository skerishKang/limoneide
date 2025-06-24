from src.core.ai_base import BaseAIHandler
from anthropic import Anthropic

class ClaudeHandler(BaseAIHandler):
    """Anthropic Claude 핸들러"""
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.client = None
        if api_key:
            self.client = Anthropic(api_key=api_key)

    def is_available(self) -> bool:
        return self.client is not None

    async def generate_response(self, prompt: str) -> str:
        if not self.is_available():
            raise Exception("Claude API 키가 설정되지 않았습니다.")
        response = await self.client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text 