def get_portfolio_template(features):
    """
    포트폴리오 템플릿 생성 (분리됨)
    """
    return f"""
<div x-data=\"portfolio()\" class=\"container mx-auto px-4 py-8\">
    <header class=\"text-center mb-8\">
        <h1 class=\"text-4xl font-bold text-gray-800 mb-2\">🎨 포트폴리오</h1>
        <p class=\"text-gray-600\">작품들을 소개합니다</p>
    </header>
    <!-- 이하 동일 (website_builder.py의 get_portfolio_template 함수 본문 전체 복사) -->
""" 