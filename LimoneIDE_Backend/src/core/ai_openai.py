from src.core.ai_base import BaseAIHandler
import openai
import os
import logging

logger = logging.getLogger(__name__)

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

class OpenAIService:
    """OpenAI 서비스 클래스"""
    
    def __init__(self):
        self.api_key = os.environ.get("OPENAI_API_KEY", "")
        self.client = None
        if self.api_key:
            try:
                self.client = openai.AsyncOpenAI(api_key=self.api_key)
                logger.info("OpenAI 서비스 초기화 완료")
            except Exception as e:
                logger.error(f"OpenAI 서비스 초기화 실패: {e}")
    
    def is_available(self) -> bool:
        """서비스 사용 가능 여부 확인"""
        return self.client is not None and bool(self.api_key)
    
    async def generate_response(self, prompt: str, model: str = "gpt-3.5-turbo") -> str:
        """
        OpenAI API를 사용하여 응답 생성
        
        Args:
            prompt: 사용자 입력 프롬프트
            model: 사용할 모델명
            
        Returns:
            str: AI 응답
        """
        if not self.is_available():
            return "OpenAI API 키가 설정되지 않았습니다. 환경변수 OPENAI_API_KEY를 확인해주세요."
        
        try:
            response = await self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "당신은 LimoneIDE의 AI 어시스턴트입니다. 사용자의 요청에 친절하고 도움이 되는 응답을 제공해주세요."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"OpenAI API 호출 중 오류 발생: {e}")
            return f"죄송합니다. 응답 생성 중 오류가 발생했습니다: {str(e)}"
    
    async def generate_code(self, prompt: str, language: str = "python") -> str:
        """
        코드 생성 전용 메서드
        
        Args:
            prompt: 코드 생성 요청
            language: 프로그래밍 언어
            
        Returns:
            str: 생성된 코드
        """
        system_prompt = f"""당신은 전문 프로그래머입니다. 
사용자의 요청에 따라 {language} 코드를 생성해주세요.
코드만 응답하고 설명은 포함하지 마세요."""

        try:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.3
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"코드 생성 중 오류 발생: {e}")
            return f"# 코드 생성 중 오류 발생: {str(e)}" 