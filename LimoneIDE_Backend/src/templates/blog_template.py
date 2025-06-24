def get_blog_template(features):
    """
    블로그 템플릿 생성 (분리됨)
    """
    return f"""
<div x-data=\"blogSystem()\" class=\"container mx-auto px-4 py-8\">
    <header class=\"text-center mb-8\">
        <h1 class=\"text-4xl font-bold text-gray-800 mb-2\">📝 내 블로그</h1>
        <p class=\"text-gray-600\">생각을 나누는 공간</p>
    </header>
    <!-- 이하 동일 (website_builder.py의 get_blog_template 함수 본문 전체 복사) -->
""" 