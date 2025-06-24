"""
🍋 LimoneIDE Voice Commands
음성 명령 처리 및 워크플로우 연결
"""

from typing import Dict, Any
from .intent_analyzer import IntentAnalyzer

class VoiceCommandProcessor:
    """
    LimoneIDE 음성 명령 처리기
    - 다양한 명령 유형 처리
    - 워크플로우 자동 연결
    """
    def __init__(self):
        self.intent_analyzer = IntentAnalyzer()
        self.command_handlers = {
            "website_creation": self.handle_website_creation,
            "workflow_automation": self.handle_workflow_automation,
            "data_analysis": self.handle_data_analysis,
            "content_generation": self.handle_content_generation
        }

    async def process_command(self, voice_text: str) -> Dict[str, Any]:
        """
        음성 명령을 받아 적절한 핸들러로 라우팅
        """
        # 1. 의도 분석
        intent = self.intent_analyzer.analyze_intent(voice_text)
        
        # 2. 적절한 핸들러 호출
        handler = self.command_handlers.get(intent["type"], self.handle_general)
        result = await handler(voice_text, intent)
        
        return {
            "status": "success",
            "intent": intent,
            "result": result,
            "suggestions": self.intent_analyzer.get_suggestions(intent)
        }

    async def handle_website_creation(self, voice_text: str, intent: Dict[str, Any]) -> Dict[str, Any]:
        """
        웹사이트 생성 명령 처리
        """
        params = intent.get("parameters", {})
        
        return {
            "type": "website_created",
            "website_type": params.get("website_type", "general"),
            "features": params.get("features", []),
            "estimated_time": "30초",
            "message": f"{params.get('website_type', '웹사이트')}를 생성합니다..."
        }

    async def handle_workflow_automation(self, voice_text: str, intent: Dict[str, Any]) -> Dict[str, Any]:
        """
        자동화 워크플로우 명령 처리
        """
        params = intent.get("parameters", {})
        
        return {
            "type": "workflow_created",
            "frequency": params.get("frequency", "once"),
            "message": f"{params.get('frequency', '일회성')} 자동화를 설정합니다..."
        }

    async def handle_data_analysis(self, voice_text: str, intent: Dict[str, Any]) -> Dict[str, Any]:
        """
        데이터 분석 명령 처리
        """
        return {
            "type": "analysis_started",
            "message": "데이터 분석을 시작합니다..."
        }

    async def handle_content_generation(self, voice_text: str, intent: Dict[str, Any]) -> Dict[str, Any]:
        """
        콘텐츠 생성 명령 처리
        """
        return {
            "type": "content_generated",
            "message": "콘텐츠를 생성합니다..."
        }

    async def handle_general(self, voice_text: str, intent: Dict[str, Any]) -> Dict[str, Any]:
        """
        일반 명령 처리
        """
        return {
            "type": "general_response",
            "message": "죄송합니다. 명령을 이해하지 못했습니다. 다시 말씀해 주세요."
        } 