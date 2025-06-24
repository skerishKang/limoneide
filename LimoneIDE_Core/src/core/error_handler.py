"""
🍋 LimoneIDE Error Handler
AI_Solarbot의 error_handler.py 기반, 모바일 친화적 오류 처리
"""

import logging
from typing import Any, Dict

class ErrorHandler:
    """
    LimoneIDE 오류 처리 시스템
    - 사용자 친화적 메시지
    - 자동 복구 로직
    - 모바일 환경 최적화
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def handle_error(self, error: Exception, context: Dict[str, Any] = None) -> Dict[str, Any]:
        self.logger.error(f"오류 발생: {error}")
        user_message = self.get_user_friendly_message(error)
        recovery = self.try_auto_recover(error, context)
        return {
            "status": "error",
            "message": user_message,
            "recovery": recovery
        }

    def get_user_friendly_message(self, error: Exception) -> str:
        # 실제 구현에서는 다양한 오류 유형별 메시지 제공
        return f"문제가 발생했습니다: {str(error)}\n잠시 후 다시 시도해 주세요."

    def try_auto_recover(self, error: Exception, context: Dict[str, Any] = None) -> str:
        # 자동 복구 로직 (예시)
        if isinstance(error, ConnectionError):
            return "네트워크를 다시 연결 중입니다."
        if isinstance(error, TimeoutError):
            return "서버 응답이 느립니다. 잠시 후 재시도합니다."
        return "자동 복구 불가. 관리자에게 문의하세요." 