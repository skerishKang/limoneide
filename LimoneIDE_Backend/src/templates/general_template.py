def get_general_template(features):
    """
    일반 템플릿 생성 (분리됨)
    """
    return f"""
<div x-data=\"generalPage()\" class=\"container mx-auto px-4 py-8\">
    <header class=\"text-center mb-8\">
        <h1 class=\"text-4xl font-bold text-gray-800 mb-2\">🍋 LimoneIDE 생성 웹사이트</h1>
        <p class=\"text-gray-600\">AI가 만든 맞춤형 웹사이트</p>
    </header>
    <!-- 이하 동일 (website_builder.py의 get_general_template 함수 본문 전체 복사) -->
""" 