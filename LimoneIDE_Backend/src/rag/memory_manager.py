"""
🍋 LimoneIDE Memory Manager
구글 드라이브 기반 RAG 시스템 - 대화 기록 관리
"""

import json
import time
from typing import Dict, Any, List, Optional
from datetime import datetime

class MemoryManager:
    """
    LimoneIDE 메모리 관리자
    - 모든 대화 자동 저장
    - 벡터 검색 시스템
    - 개인 맞춤 컨텍스트 구축
    """
    
    def __init__(self):
        self.conversations = []
        self.user_profiles = {}
        self.search_index = {}

    async def save_conversation(self, user_id: str, user_message: str, ai_response: str, metadata: Dict[str, Any] = {}) -> bool:
        """
        대화 내용을 메모리에 저장
        """
        try:
            conversation = {
                "id": f"conv_{int(time.time())}",
                "user_id": user_id,
                "timestamp": datetime.now().isoformat(),
                "user_message": user_message,
                "ai_response": ai_response,
                "metadata": metadata,
                "tags": self.extract_tags(user_message, ai_response)
            }
            
            self.conversations.append(conversation)
            
            # 검색 인덱스 업데이트
            self.update_search_index(conversation)
            
            # 사용자 프로필 업데이트
            self.update_user_profile(user_id, conversation)
            
            return True
            
        except Exception as e:
            print(f"대화 저장 실패: {e}")
            return False

    def extract_tags(self, user_message: str, ai_response: str) -> List[str]:
        """
        대화에서 태그 추출 (프로토타입)
        """
        tags = []
        
        # 키워드 기반 태그 추출
        keywords = {
            "website": ["웹사이트", "사이트", "만들어줘", "생성"],
            "automation": ["자동화", "매일", "매주", "정기"],
            "analysis": ["분석", "통계", "데이터", "리포트"],
            "content": ["글", "콘텐츠", "블로그", "뉴스"],
            "ecommerce": ["쇼핑몰", "상품", "결제", "주문"],
            "blog": ["블로그", "글쓰기", "포스트", "카테고리"]
        }
        
        combined_text = (user_message + " " + ai_response).lower()
        
        for category, words in keywords.items():
            if any(word in combined_text for word in words):
                tags.append(category)
        
        return tags

    def update_search_index(self, conversation: Dict[str, Any]):
        """
        검색 인덱스 업데이트
        """
        # 간단한 키워드 기반 인덱싱 (실제로는 벡터 검색 사용)
        text = f"{conversation['user_message']} {conversation['ai_response']}"
        words = text.lower().split()
        
        for word in words:
            if len(word) > 2:  # 2글자 이상만 인덱싱
                if word not in self.search_index:
                    self.search_index[word] = []
                self.search_index[word].append(conversation['id'])

    def update_user_profile(self, user_id: str, conversation: Dict[str, Any]):
        """
        사용자 프로필 업데이트
        """
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = {
                "conversation_count": 0,
                "favorite_topics": {},
                "last_active": None,
                "preferences": {}
            }
        
        profile = self.user_profiles[user_id]
        profile["conversation_count"] += 1
        profile["last_active"] = conversation["timestamp"]
        
        # 주제별 선호도 업데이트
        for tag in conversation["tags"]:
            if tag not in profile["favorite_topics"]:
                profile["favorite_topics"][tag] = 0
            profile["favorite_topics"][tag] += 1

    async def search_conversations(self, query: str, user_id: str = "", limit: int = 10) -> List[Dict[str, Any]]:
        """
        과거 대화 검색
        """
        try:
            query_words = query.lower().split()
            relevant_conversations = []
            
            for word in query_words:
                if word in self.search_index:
                    conv_ids = self.search_index[word]
                    for conv_id in conv_ids:
                        conversation = next((c for c in self.conversations if c["id"] == conv_id), None)
                        if conversation and (user_id == "" or conversation["user_id"] == user_id):
                            if conversation not in relevant_conversations:
                                relevant_conversations.append(conversation)
            
            # 관련도 순으로 정렬 (태그 매칭 개수 기준)
            relevant_conversations.sort(
                key=lambda x: sum(1 for word in query_words if word in x["user_message"].lower() or word in x["ai_response"].lower()),
                reverse=True
            )
            
            return relevant_conversations[:limit]
            
        except Exception as e:
            print(f"대화 검색 실패: {e}")
            return []

    def get_user_context(self, user_id: str, limit: int = 5) -> Dict[str, Any]:
        """
        사용자별 컨텍스트 정보 반환
        """
        if user_id not in self.user_profiles:
            return {}
        
        profile = self.user_profiles[user_id]
        
        # 최근 대화들
        recent_conversations = [
            c for c in self.conversations 
            if c["user_id"] == user_id
        ][-limit:]
        
        # 선호 주제
        favorite_topics = sorted(
            profile["favorite_topics"].items(),
            key=lambda x: x[1],
            reverse=True
        )[:3]
        
        return {
            "user_id": user_id,
            "conversation_count": profile["conversation_count"],
            "last_active": profile["last_active"],
            "favorite_topics": [topic for topic, count in favorite_topics],
            "recent_conversations": recent_conversations,
            "preferences": profile["preferences"]
        }

    async def get_project_history(self, user_id: str, project_keywords: List[str]) -> List[Dict[str, Any]]:
        """
        특정 프로젝트 관련 대화 히스토리 반환
        """
        try:
            project_conversations = []
            
            for conversation in self.conversations:
                if conversation["user_id"] == user_id:
                    text = f"{conversation['user_message']} {conversation['ai_response']}"
                    if any(keyword.lower() in text.lower() for keyword in project_keywords):
                        project_conversations.append(conversation)
            
            return project_conversations
            
        except Exception as e:
            print(f"프로젝트 히스토리 검색 실패: {e}")
            return []

    def export_conversations(self, user_id: str = "") -> str:
        """
        대화 내보내기 (JSON 형식)
        """
        try:
            if user_id:
                user_conversations = [c for c in self.conversations if c["user_id"] == user_id]
            else:
                user_conversations = self.conversations
            
            export_data = {
                "export_time": datetime.now().isoformat(),
                "conversations": user_conversations,
                "user_profiles": self.user_profiles if user_id == "" else {user_id: self.user_profiles.get(user_id, {})}
            }
            
            return json.dumps(export_data, ensure_ascii=False, indent=2)
            
        except Exception as e:
            print(f"대화 내보내기 실패: {e}")
            return ""

    def get_statistics(self) -> Dict[str, Any]:
        """
        메모리 사용 통계
        """
        total_conversations = len(self.conversations)
        unique_users = len(set(c["user_id"] for c in self.conversations))
        
        # 태그별 통계
        tag_counts = {}
        for conversation in self.conversations:
            for tag in conversation["tags"]:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        return {
            "total_conversations": total_conversations,
            "unique_users": unique_users,
            "tag_distribution": tag_counts,
            "search_index_size": len(self.search_index),
            "memory_size_mb": len(json.dumps(self.conversations)) / (1024 * 1024)
        } 