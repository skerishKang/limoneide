"""
🍋 LimoneIDE AI Engine
AI_Solarbot의 ai_handler.py를 기반으로 확장된 멀티 AI 엔진
"""

import asyncio
import json
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

# AI 모델 imports
import openai
import google.generativeai as genai
from anthropic import Anthropic

# 로컬 AI (선택적)
try:
    from ollama import Client as OllamaClient
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

@dataclass
class AIResponse:
    """AI 응답 데이터 클래스"""
    content: str
    model: str
    tokens_used: int
    response_time: float
    metadata: Dict[str, Any] = None

class LimoneAIEngine:
    """
    LimoneIDE의 핵심 AI 엔진
    - Gemini, GPT-4, Claude, Ollama 지원
    - 음성 명령 처리
    - 워크플로우 자동 생성
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # AI 모델 핸들러 초기화
        self.gemini_handler = GeminiHandler(self.config.get('gemini_api_key'))
        self.openai_handler = OpenAIHandler(self.config.get('openai_api_key'))
        self.claude_handler = ClaudeHandler(self.config.get('claude_api_key'))
        
        if OLLAMA_AVAILABLE:
            self.ollama_handler = OllamaHandler()
        
        # 음성 처리 및 워크플로우 생성기
        self.voice_processor = VoiceProcessor()
        self.workflow_generator = WorkflowGenerator()
        
        # 응답 캐시
        self.response_cache = {}
    
    async def process_voice_command(self, audio_data: bytes) -> Dict[str, Any]:
        """
        음성 → 워크플로우 생성 (핵심 기능)
        
        Args:
            audio_data: 음성 오디오 데이터
            
        Returns:
            Dict: 처리 결과
        """
        try:
            # 1. 음성 → 텍스트 변환
            text = await self.voice_processor.transcribe(audio_data)
            self.logger.info(f"음성 인식 결과: {text}")
            
            # 2. 의도 분석
            intent = await self.analyze_automation_intent(text)
            self.logger.info(f"의도 분석: {intent}")
            
            # 3. 워크플로우 생성
            workflow = await self.generate_workflow(intent)
            self.logger.info(f"워크플로우 생성 완료")
            
            # 4. 즉시 실행
            result = await self.execute_workflow(workflow)
            
            return {
                "status": "success",
                "original_text": text,
                "intent": intent,
                "workflow": workflow,
                "result": result
            }
            
        except Exception as e:
            self.logger.error(f"음성 명령 처리 오류: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def analyze_automation_intent(self, text: str) -> Dict[str, Any]:
        """
        자연어 → 자동화 의도 분석
        """
        prompt = f"""
        다음 음성 명령을 분석하여 자동화 의도를 파악해주세요:
        
        명령: "{text}"
        
        다음 형식으로 응답해주세요:
        {{
            "type": "website_creation|workflow_automation|data_analysis|content_generation",
            "target": "웹사이트/자동화/분석/콘텐츠 대상",
            "features": ["필요한 기능들"],
            "priority": "high|medium|low",
            "estimated_time": "예상 소요 시간"
        }}
        """
        
        response = await self.get_best_ai_response(prompt)
        
        try:
            return json.loads(response.content)
        except json.JSONDecodeError:
            # 기본 의도 반환
            return {
                "type": "general",
                "target": text,
                "features": [],
                "priority": "medium",
                "estimated_time": "5분"
            }
    
    async def generate_workflow(self, intent: Dict[str, Any]) -> Dict[str, Any]:
        """
        의도 → 워크플로우 생성
        """
        return await self.workflow_generator.create_workflow(intent)
    
    async def execute_workflow(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """
        워크플로우 실행
        """
        # 실제 구현은 workflow_engine.py에서 처리
        return {"status": "workflow_executed", "workflow_id": workflow.get("id")}
    
    async def get_best_ai_response(self, prompt: str, model_preference: str = "auto") -> AIResponse:
        """
        최적의 AI 모델로 응답 생성
        """
        models = []
        
        # 사용 가능한 모델들 수집
        if self.gemini_handler.is_available():
            models.append(("gemini", self.gemini_handler))
        
        if self.openai_handler.is_available():
            models.append(("gpt", self.openai_handler))
        
        if self.claude_handler.is_available():
            models.append(("claude", self.claude_handler))
        
        if not models:
            raise Exception("사용 가능한 AI 모델이 없습니다.")
        
        # 모델 선택
        if model_preference == "auto":
            # 자동 선택 (무료 우선)
            selected_model = models[0]  # Gemini가 무료이므로 우선
        else:
            # 특정 모델 선택
            selected_model = next((m for m in models if m[0] == model_preference), models[0])
        
        model_name, handler = selected_model
        
        # 응답 생성
        start_time = asyncio.get_event_loop().time()
        response = await handler.generate_response(prompt)
        end_time = asyncio.get_event_loop().time()
        
        return AIResponse(
            content=response,
            model=model_name,
            tokens_used=0,  # 실제 토큰 수는 각 핸들러에서 계산
            response_time=end_time - start_time
        )

class GeminiHandler:
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

class OpenAIHandler:
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

class ClaudeHandler:
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

class OllamaHandler:
    """로컬 Ollama 핸들러"""
    
    def __init__(self):
        self.client = OllamaClient()
    
    def is_available(self) -> bool:
        try:
            # 간단한 연결 테스트
            return True
        except:
            return False
    
    async def generate_response(self, prompt: str) -> str:
        response = self.client.chat(model='llama2', messages=[
            {'role': 'user', 'content': prompt}
        ])
        return response['message']['content']

class VoiceProcessor:
    """음성 처리 클래스 (프로토타입)"""
    
    async def transcribe(self, audio_data: bytes) -> str:
        """
        음성 → 텍스트 변환 (프로토타입)
        실제 구현에서는 Whisper API 사용
        """
        # 임시 구현
        return "온라인 쇼핑몰 만들어줘"

class WorkflowGenerator:
    """워크플로우 생성기 (프로토타입)"""
    
    async def create_workflow(self, intent: Dict[str, Any]) -> Dict[str, Any]:
        """
        의도 → 워크플로우 생성 (프로토타입)
        """
        workflow_id = f"workflow_{int(asyncio.get_event_loop().time())}"
        
        return {
            "id": workflow_id,
            "type": intent.get("type", "general"),
            "steps": [
                {
                    "id": "step_1",
                    "action": "analyze_requirements",
                    "input": intent.get("target", ""),
                    "output": "requirements"
                },
                {
                    "id": "step_2", 
                    "action": "generate_code",
                    "input": "requirements",
                    "output": "website_code"
                },
                {
                    "id": "step_3",
                    "action": "deploy_website",
                    "input": "website_code",
                    "output": "website_url"
                }
            ],
            "metadata": intent
        }

# 사용 예시
if __name__ == "__main__":
    # 테스트
    async def test_ai_engine():
        engine = LimoneAIEngine()
        
        # 음성 명령 시뮬레이션
        test_audio = b"test_audio_data"
        result = await engine.process_voice_command(test_audio)
        print(f"결과: {result}")
    
    asyncio.run(test_ai_engine()) 