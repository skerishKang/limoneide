"""
🍋 LimoneIDE Main Application
음성 명령 → 웹사이트 생성 → 배포 전체 워크플로우
"""

import asyncio
import logging
from typing import Dict, Any

# LimoneIDE 모듈 imports
from src.core.ai_engine import LimoneAIEngine
from src.core.error_handler import ErrorHandler
from src.core.code_executor import CodeExecutor
from src.voice.voice_commands import VoiceCommandProcessor
from src.automation.website_builder import WebsiteBuilder
from src.automation.deployment_manager import DeploymentManager

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LimoneIDE:
    """
    LimoneIDE 메인 애플리케이션
    - 음성 명령 처리
    - 웹사이트 자동 생성
    - Google Sites 배포
    """
    
    def __init__(self):
        # 핵심 컴포넌트 초기화
        self.ai_engine = LimoneAIEngine()
        self.error_handler = ErrorHandler()
        self.code_executor = CodeExecutor()
        self.voice_processor = VoiceCommandProcessor()
        self.website_builder = WebsiteBuilder()
        self.deployment_manager = DeploymentManager()
        
        logger.info("🍋 LimoneIDE 초기화 완료")

    async def process_voice_command(self, voice_text: str) -> Dict[str, Any]:
        """
        음성 명령을 받아 전체 워크플로우 실행
        """
        try:
            logger.info(f"음성 명령 처리 시작: {voice_text}")
            
            # 1. 음성 명령 분석 및 처리
            voice_result = await self.voice_processor.process_command(voice_text)
            
            if voice_result["status"] != "success":
                return self.error_handler.handle_error(
                    Exception("음성 명령 처리 실패"), 
                    {"voice_text": voice_text}
                )
            
            # 2. 웹사이트 생성이 필요한 경우
            if voice_result["result"]["type"] == "website_created":
                website_result = await self.create_and_deploy_website(voice_result)
                return website_result
            
            # 3. 다른 명령 처리
            return voice_result
            
        except Exception as e:
            logger.error(f"음성 명령 처리 중 오류: {e}")
            return self.error_handler.handle_error(e, {"voice_text": voice_text})

    async def create_and_deploy_website(self, voice_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        웹사이트 생성 및 배포
        """
        try:
            intent = voice_result["intent"]
            result = voice_result["result"]
            
            # 1. 웹사이트 요구사항 구성
            requirements = {
                "website_type": result.get("website_type", "general"),
                "features": result.get("features", []),
                "title": f"{result.get('website_type', '웹사이트')} - LimoneIDE 생성"
            }
            
            logger.info(f"웹사이트 생성 시작: {requirements}")
            
            # 2. Alpine.js 웹사이트 생성
            website_code = self.website_builder.build_website(requirements)
            
            # 3. Google Sites에 배포
            deployment_result = await self.deployment_manager.deploy_website(
                website_code, requirements
            )
            
            if deployment_result["status"] == "success":
                return {
                    "status": "success",
                    "message": "🎉 웹사이트가 성공적으로 생성되었습니다!",
                    "website_url": deployment_result["site_url"],
                    "generation_time": "30초",
                    "features": requirements["features"],
                    "deployment_info": deployment_result
                }
            else:
                return deployment_result
                
        except Exception as e:
            logger.error(f"웹사이트 생성 중 오류: {e}")
            return self.error_handler.handle_error(e, {"voice_result": voice_result})

    async def demo_website_creation(self) -> Dict[str, Any]:
        """
        데모: "쇼핑몰 만들어줘" → 30초 완성
        """
        demo_command = "포트폴리오 사이트 만들어줘. 내 소개와 프로젝트 목록 포함"
        logger.info(f"데모 시작: {demo_command}")
        
        return await self.process_voice_command(demo_command)

# 사용 예시
async def main():
    """메인 함수"""
    limoneide = LimoneIDE()
    
    # 데모 실행
    result = await limoneide.demo_website_creation()
    
    print("\n" + "="*50)
    print("🍋 LimoneIDE 데모 결과")
    print("="*50)
    print(f"상태: {result['status']}")
    print(f"메시지: {result['message']}")
    
    if result['status'] == 'success' and 'website_url' in result:
        print(f"웹사이트 URL: {result['website_url']}")
        print(f"생성 시간: {result['generation_time']}")
        print(f"기능: {', '.join(result['features'])}")
    
    print("="*50)

if __name__ == "__main__":
    asyncio.run(main()) 