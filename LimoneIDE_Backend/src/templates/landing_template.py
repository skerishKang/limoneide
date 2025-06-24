def get_landing_template(features):
    """
    랜딩 페이지 템플릿 생성 (분리됨)
    """
    return f"""
<div x-data=\"landingPage()\" class=\"min-h-screen\">
    <!-- 이하 동일 (website_builder.py의 get_landing_template 함수 본문 전체 복사) -->
""" 