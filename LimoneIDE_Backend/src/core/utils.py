def extract_tags(user_message: str, ai_response: str) -> list:
    """
    대화에서 태그 추출 (공통 유틸)
    """
    tags = []
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

def summarize_project(conversations: list) -> str:
    """
    프로젝트 대화 요약 (공통 유틸)
    """
    if not conversations:
        return "프로젝트 기록이 없습니다."
    tag_counts = {}
    for conv in conversations:
        for tag in conv.get('tags', []):
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
    main_features = []
    if tag_counts.get('website', 0) > 0:
        main_features.append("웹사이트 생성")
    if tag_counts.get('ecommerce', 0) > 0:
        main_features.append("쇼핑몰 기능")
    if tag_counts.get('blog', 0) > 0:
        main_features.append("블로그 기능")
    if tag_counts.get('automation', 0) > 0:
        main_features.append("자동화 기능")
    summary = f"총 {len(conversations)}번의 대화, 주요 기능: {', '.join(main_features)}"
    return summary 