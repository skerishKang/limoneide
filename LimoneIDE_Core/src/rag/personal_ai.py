"""
🍋 LimoneIDE Personal AI
개인화 AI 어시스턴트 - 과거 기억 + 예측적 제안
"""

from typing import Dict, Any, List, Optional
from .memory_manager import MemoryManager

class PersonalAI:
    """
    LimoneIDE 개인화 AI 어시스턴트
    - 과거 프로젝트 완벽 기억
    - 사용자 패턴 학습
    - 예측적 제안 시스템
    """
    
    def __init__(self, memory_manager: MemoryManager):
        self.memory = memory_manager
        self.user_preferences = {}

    async def respond_with_context(self, user_id: str, user_message: str) -> Dict[str, Any]:
        """
        과거 컨텍스트를 포함한 개인화 응답 생성
        """
        try:
            # 1. 사용자 컨텍스트 가져오기
            user_context = self.memory.get_user_context(user_id)
            
            # 2. 관련 과거 대화 검색
            relevant_conversations = await self.memory.search_conversations(
                user_message, user_id, limit=5
            )
            
            # 3. 개인화된 응답 생성
            personalized_response = await self.generate_personalized_response(
                user_message, user_context, relevant_conversations
            )
            
            # 4. 대화 저장
            await self.memory.save_conversation(
                user_id, user_message, personalized_response["response"]
            )
            
            return personalized_response
            
        except Exception as e:
            return {
                "response": f"죄송합니다. 개인화 응답 생성 중 오류가 발생했습니다: {str(e)}",
                "context_used": False,
                "suggestions": []
            }

    async def generate_personalized_response(self, user_message: str, user_context: Dict[str, Any], relevant_conversations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        개인화된 응답 생성
        """
        # 기본 응답
        base_response = "안녕하세요! 무엇을 도와드릴까요?"
        
        # 컨텍스트가 있는 경우 개인화
        if user_context and relevant_conversations:
            context_info = self.build_context_summary(user_context, relevant_conversations)
            
            # 개인화된 응답 생성
            if "쇼핑몰" in user_message.lower():
                base_response = f"네! 이전에 {user_context.get('conversation_count', 0)}번의 대화를 나눈 것을 기억합니다. "
                base_response += "쇼핑몰을 만들어드릴게요. 이전에 만든 쇼핑몰과 비슷한 스타일로 만들까요?"
            
            elif "블로그" in user_message.lower():
                base_response = f"블로그 생성이군요! 지금까지 {len(relevant_conversations)}개의 관련 대화를 나눈 것을 기억합니다. "
                base_response += "이전에 선호하신 스타일로 블로그를 만들어드릴게요."
            
            else:
                base_response = f"안녕하세요! {user_context.get('conversation_count', 0)}번째 대화네요. "
                base_response += "이전에 관심을 보이신 주제들을 기억하고 있습니다."
        
        # 제안사항 생성
        suggestions = self.generate_suggestions(user_context, user_message)
        
        return {
            "response": base_response,
            "context_used": bool(user_context and relevant_conversations),
            "suggestions": suggestions,
            "user_context": user_context,
            "relevant_conversations_count": len(relevant_conversations)
        }

    def build_context_summary(self, user_context: Dict[str, Any], relevant_conversations: List[Dict[str, Any]]) -> str:
        """
        컨텍스트 요약 생성
        """
        summary = f"사용자 {user_context.get('user_id', 'Unknown')}의 "
        summary += f"총 {user_context.get('conversation_count', 0)}번의 대화, "
        summary += f"선호 주제: {', '.join(user_context.get('favorite_topics', []))}, "
        summary += f"관련 대화 {len(relevant_conversations)}개 발견"
        
        return summary

    def generate_suggestions(self, user_context: Dict[str, Any], current_message: str) -> List[str]:
        """
        사용자 패턴 기반 제안사항 생성
        """
        suggestions = []
        
        if not user_context:
            # 기본 제안사항
            suggestions = [
                "웹사이트를 만들어보시겠어요?",
                "자동화 워크플로우를 설정해보시겠어요?",
                "데이터 분석을 도와드릴까요?"
            ]
        else:
            # 개인화된 제안사항
            favorite_topics = user_context.get('favorite_topics', [])
            
            if 'website' in favorite_topics:
                suggestions.append("새로운 웹사이트를 만들어보시겠어요?")
            
            if 'ecommerce' in favorite_topics:
                suggestions.append("쇼핑몰 기능을 추가해보시겠어요?")
            
            if 'blog' in favorite_topics:
                suggestions.append("블로그 콘텐츠를 생성해보시겠어요?")
            
            if 'automation' in favorite_topics:
                suggestions.append("새로운 자동화 워크플로우를 설정해보시겠어요?")
            
            # 최근 활동 기반 제안
            recent_conversations = user_context.get('recent_conversations', [])
            if recent_conversations:
                last_conversation = recent_conversations[-1]
                if "쇼핑몰" in last_conversation.get('user_message', ''):
                    suggestions.append("쇼핑몰에 결제 시스템을 추가해보시겠어요?")
                elif "블로그" in last_conversation.get('user_message', ''):
                    suggestions.append("블로그에 댓글 시스템을 추가해보시겠어요?")
        
        return suggestions[:3]  # 최대 3개 제안

    async def get_project_memory(self, user_id: str, project_name: str) -> Dict[str, Any]:
        """
        특정 프로젝트의 기억 반환
        """
        try:
            # 프로젝트 관련 키워드
            project_keywords = [project_name, "프로젝트", "개발", "만들기"]
            
            # 프로젝트 히스토리 검색
            project_conversations = await self.memory.get_project_history(user_id, project_keywords)
            
            if project_conversations:
                # 프로젝트 요약 생성
                project_summary = self.summarize_project(project_conversations)
                
                return {
                    "project_name": project_name,
                    "conversations_count": len(project_conversations),
                    "first_created": project_conversations[0]["timestamp"],
                    "last_updated": project_conversations[-1]["timestamp"],
                    "summary": project_summary,
                    "conversations": project_conversations
                }
            else:
                return {
                    "project_name": project_name,
                    "conversations_count": 0,
                    "message": "해당 프로젝트에 대한 기록이 없습니다."
                }
                
        except Exception as e:
            return {
                "project_name": project_name,
                "error": str(e),
                "message": "프로젝트 기억 검색 중 오류가 발생했습니다."
            }

    def summarize_project(self, conversations: List[Dict[str, Any]]) -> str:
        """
        프로젝트 대화 요약 생성
        """
        if not conversations:
            return "프로젝트 기록이 없습니다."
        
        # 태그별 빈도 계산
        tag_counts = {}
        for conv in conversations:
            for tag in conv.get('tags', []):
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        # 주요 기능 추출
        main_features = []
        if tag_counts.get('website', 0) > 0:
            main_features.append("웹사이트 생성")
        if tag_counts.get('ecommerce', 0) > 0:
            main_features.append("쇼핑몰 기능")
        if tag_counts.get('blog', 0) > 0:
            main_features.append("블로그 기능")
        if tag_counts.get('automation', 0) > 0:
            main_features.append("자동화 기능")
        
        summary = f"총 {len(conversations)}번의 대화, "
        summary += f"주요 기능: {', '.join(main_features)}, "
        summary += f"시작일: {conversations[0]['timestamp'][:10]}"
        
        return summary

    async def predict_user_needs(self, user_id: str) -> List[str]:
        """
        사용자 패턴 기반 예측적 제안
        """
        try:
            user_context = self.memory.get_user_context(user_id)
            
            if not user_context:
                return []
            
            predictions = []
            favorite_topics = user_context.get('favorite_topics', [])
            recent_conversations = user_context.get('recent_conversations', [])
            
            # 선호 주제 기반 예측
            if 'website' in favorite_topics and len(recent_conversations) > 0:
                last_conv = recent_conversations[-1]
                if "쇼핑몰" in last_conv.get('user_message', ''):
                    predictions.append("쇼핑몰에 관리자 페이지를 추가해보시겠어요?")
                elif "블로그" in last_conv.get('user_message', ''):
                    predictions.append("블로그에 SEO 최적화를 적용해보시겠어요?")
            
            # 시간 패턴 기반 예측
            if len(recent_conversations) >= 3:
                # 매일 같은 시간에 접속하는 패턴이 있는지 확인
                predictions.append("정기적인 자동화 워크플로우를 설정해보시겠어요?")
            
            return predictions[:2]  # 최대 2개 예측
            
        except Exception as e:
            print(f"사용자 니즈 예측 실패: {e}")
            return []

    def get_user_insights(self, user_id: str) -> Dict[str, Any]:
        """
        사용자 인사이트 제공
        """
        try:
            user_context = self.memory.get_user_context(user_id)
            
            if not user_context:
                return {"message": "사용자 데이터가 부족합니다."}
            
            insights = {
                "total_conversations": user_context.get('conversation_count', 0),
                "favorite_topics": user_context.get('favorite_topics', []),
                "last_active": user_context.get('last_active', 'Unknown'),
                "productivity_score": self.calculate_productivity_score(user_context),
                "recommendations": self.generate_recommendations(user_context)
            }
            
            return insights
            
        except Exception as e:
            return {"error": str(e)}

    def calculate_productivity_score(self, user_context: Dict[str, Any]) -> int:
        """
        생산성 점수 계산 (1-100)
        """
        conversation_count = user_context.get('conversation_count', 0)
        favorite_topics = user_context.get('favorite_topics', [])
        
        # 대화 수 기반 점수 (최대 50점)
        conversation_score = min(conversation_count * 5, 50)
        
        # 주제 다양성 기반 점수 (최대 50점)
        topic_score = min(len(favorite_topics) * 10, 50)
        
        return conversation_score + topic_score

    def generate_recommendations(self, user_context: Dict[str, Any]) -> List[str]:
        """
        개인화된 추천사항 생성
        """
        recommendations = []
        favorite_topics = user_context.get('favorite_topics', [])
        
        if 'website' in favorite_topics:
            recommendations.append("웹사이트 템플릿 라이브러리를 확장해보세요")
        
        if 'ecommerce' in favorite_topics:
            recommendations.append("결제 시스템 통합을 고려해보세요")
        
        if 'automation' in favorite_topics:
            recommendations.append("복잡한 워크플로우 자동화를 시도해보세요")
        
        if len(favorite_topics) < 3:
            recommendations.append("다양한 기능을 시도해보세요")
        
        return recommendations 