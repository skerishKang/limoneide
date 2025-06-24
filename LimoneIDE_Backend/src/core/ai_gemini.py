from src.core.ai_base import BaseAIHandler
import google.generativeai as genai
import os
import logging

logger = logging.getLogger(__name__)

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

class GeminiService:
    """Google Gemini 서비스 클래스"""
    
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY", "")
        self.model = None
        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-pro')
                logger.info("Gemini 서비스 초기화 완료")
            except Exception as e:
                logger.error(f"Gemini 서비스 초기화 실패: {e}")
    
    def is_available(self) -> bool:
        """서비스 사용 가능 여부 확인"""
        return self.model is not None and bool(self.api_key)
    
    async def generate_response(self, prompt: str) -> str:
        """
        Gemini API를 사용하여 응답 생성
        
        Args:
            prompt: 사용자 입력 프롬프트
            
        Returns:
            str: AI 응답
        """
        if not self.is_available():
            return "Gemini API 키가 설정되지 않았습니다. 환경변수 GEMINI_API_KEY를 확인해주세요."
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"Gemini API 호출 중 오류 발생: {e}")
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
        code_prompt = f"다음 요청에 따라 {language} 코드를 생성해주세요. 코드만 응답하고 설명은 포함하지 마세요:\n\n{prompt}"
        
        try:
            response = self.model.generate_content(code_prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"코드 생성 중 오류 발생: {e}")
            return f"# 코드 생성 중 오류 발생: {str(e)}" 