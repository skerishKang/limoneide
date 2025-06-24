"""
🍋 LimoneIDE RAG System Demo
개인화 AI 어시스턴트 데모
"""

import asyncio
from src.rag.memory_manager import MemoryManager
from src.rag.personal_ai import PersonalAI

async def demo_rag_system():
    """RAG 시스템 데모"""
    print("🍋 LimoneIDE RAG 시스템 데모 시작")
    print("="*50)
    
    # 메모리 관리자 및 개인 AI 초기화
    memory_manager = MemoryManager()
    personal_ai = PersonalAI(memory_manager)
    
    # 테스트 사용자 ID
    user_id = "demo_user_001"
    
    # 1. 첫 번째 대화 (쇼핑몰 생성)
    print("\n1️⃣ 첫 번째 대화: 쇼핑몰 생성")
    print("-" * 30)
    
    response1 = await personal_ai.respond_with_context(
        user_id, "온라인 쇼핑몰 만들어줘. 케이크 주문받는 거"
    )
    
    print(f"사용자: 온라인 쇼핑몰 만들어줘. 케이크 주문받는 거")
    print(f"AI: {response1['response']}")
    print(f"컨텍스트 사용: {response1['context_used']}")
    print(f"제안사항: {response1['suggestions']}")
    
    # 2. 두 번째 대화 (블로그 생성)
    print("\n2️⃣ 두 번째 대화: 블로그 생성")
    print("-" * 30)
    
    response2 = await personal_ai.respond_with_context(
        user_id, "블로그도 만들어줘. 요리 레시피 올리는 거"
    )
    
    print(f"사용자: 블로그도 만들어줘. 요리 레시피 올리는 거")
    print(f"AI: {response2['response']}")
    print(f"컨텍스트 사용: {response2['context_used']}")
    print(f"제안사항: {response2['suggestions']}")
    
    # 3. 세 번째 대화 (과거 기억 테스트)
    print("\n3️⃣ 세 번째 대화: 과거 기억 테스트")
    print("-" * 30)
    
    response3 = await personal_ai.respond_with_context(
        user_id, "지난번에 만든 쇼핑몰 기억해?"
    )
    
    print(f"사용자: 지난번에 만든 쇼핑몰 기억해?")
    print(f"AI: {response3['response']}")
    print(f"컨텍스트 사용: {response3['context_used']}")
    print(f"관련 대화 수: {response3['relevant_conversations_count']}")
    
    # 4. 사용자 인사이트 확인
    print("\n4️⃣ 사용자 인사이트")
    print("-" * 30)
    
    insights = personal_ai.get_user_insights(user_id)
    print(f"총 대화 수: {insights.get('total_conversations', 0)}")
    print(f"선호 주제: {insights.get('favorite_topics', [])}")
    print(f"생산성 점수: {insights.get('productivity_score', 0)}/100")
    print(f"추천사항: {insights.get('recommendations', [])}")
    
    # 5. 프로젝트 기억 확인
    print("\n5️⃣ 프로젝트 기억 확인")
    print("-" * 30)
    
    project_memory = await personal_ai.get_project_memory(user_id, "쇼핑몰")
    print(f"프로젝트: {project_memory.get('project_name', 'Unknown')}")
    print(f"대화 수: {project_memory.get('conversations_count', 0)}")
    print(f"요약: {project_memory.get('summary', 'N/A')}")
    
    # 6. 예측적 제안
    print("\n6️⃣ 예측적 제안")
    print("-" * 30)
    
    predictions = await personal_ai.predict_user_needs(user_id)
    print(f"예측 제안: {predictions}")
    
    # 7. 메모리 통계
    print("\n7️⃣ 메모리 통계")
    print("-" * 30)
    
    stats = memory_manager.get_statistics()
    print(f"총 대화 수: {stats['total_conversations']}")
    print(f"고유 사용자 수: {stats['unique_users']}")
    print(f"태그 분포: {stats['tag_distribution']}")
    print(f"검색 인덱스 크기: {stats['search_index_size']}")
    print(f"메모리 크기: {stats['memory_size_mb']:.2f} MB")
    
    print("\n" + "="*50)
    print("🎉 RAG 시스템 데모 완료!")
    print("="*50)

if __name__ == "__main__":
    asyncio.run(demo_rag_system()) 