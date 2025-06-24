"""
🍋 LimoneIDE Intent Analyzer
음성 명령의 의도 분석 (자연어 처리 + AI)
"""

from typing import Dict, Any, List

class IntentAnalyzer:
    """
    LimoneIDE 의도 분석 엔진
    - 자연어 → 자동화 의도 파악
    - AI 기반 의도 분류
    """
    def __init__(self):
        self.intent_patterns = {
            "website_creation": ["만들어줘", "생성", "웹사이트", "사이트"],
            "workflow_automation": ["자동화", "매일", "매주", "정기"],
            "data_analysis": ["분석", "통계", "데이터", "리포트"],
            "content_generation": ["글", "콘텐츠", "블로그", "뉴스"]
        }

    def analyze(self, text: str) -> Dict[str, Any]:
        """
        텍스트를 분석하여 의도와 매개변수 추출
        
        Args:
            text: 분석할 텍스트
            
        Returns:
            Dict: 분석 결과
        """
        return self.analyze_intent(text)

    def analyze_intent(self, text: str) -> Dict[str, Any]:
        """
        텍스트를 분석하여 의도와 매개변수 추출
        """
        intent_type = self.classify_intent(text)
        parameters = self.extract_parameters(text, intent_type)
        
        return {
            "type": intent_type,
            "confidence": 0.85,  # 실제로는 AI 모델의 신뢰도
            "parameters": parameters,
            "original_text": text,
            **parameters  # 매개변수를 최상위 수준에 추가
        }

    def classify_intent(self, text: str) -> str:
        """
        의도 분류 (프로토타입)
        """
        text_lower = text.lower()
        
        for intent, patterns in self.intent_patterns.items():
            if any(pattern in text_lower for pattern in patterns):
                return intent
        
        return "general"

    def extract_parameters(self, text: str, intent_type: str) -> Dict[str, Any]:
        """
        의도에 따른 매개변수 추출
        """
        params = {}
        
        if intent_type == "website_creation":
            # 웹사이트 생성 관련 매개변수
            if "쇼핑몰" in text:
                params["website_type"] = "ecommerce"
                params["features"] = ["상품 목록", "장바구니", "결제"]
            elif "블로그" in text:
                params["website_type"] = "blog"
                params["features"] = ["글쓰기", "댓글", "카테고리"]
            elif "포트폴리오" in text:
                params["website_type"] = "portfolio"
                params["features"] = ["프로젝트", "소개", "연락처"]
            elif "랜딩" in text:
                params["website_type"] = "landing"
                params["features"] = ["헤더", "특징", "가격", "연락처"]
            else:
                params["website_type"] = "general"
                params["features"] = ["기본 레이아웃", "반응형"]
        
        elif intent_type == "workflow_automation":
            # 자동화 관련 매개변수
            if "매일" in text:
                params["frequency"] = "daily"
            elif "매주" in text:
                params["frequency"] = "weekly"
        
        return params

    def get_suggestions(self, intent: Dict[str, Any]) -> List[str]:
        """
        의도에 따른 제안사항 반환
        """
        suggestions = []
        
        if intent["type"] == "website_creation":
            suggestions = [
                "결제 시스템을 추가하시겠습니까?",
                "관리자 페이지가 필요하신가요?",
                "모바일 최적화를 적용할까요?"
            ]
        
        return suggestions 