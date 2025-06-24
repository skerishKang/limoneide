def get_ecommerce_template(features):
    """
    쇼핑몰 템플릿 생성 (분리됨)
    """
    return f"""
<div x-data=\"ecommerceStore()\" class=\"container mx-auto px-4 py-8\">
    <header class=\"text-center mb-8\">
        <h1 class=\"text-4xl font-bold text-gray-800 mb-2\">🛍️ 온라인 쇼핑몰</h1>
        <p class=\"text-gray-600\">최고의 상품을 만나보세요</p>
    </header>
    <!-- 이하 동일 (website_builder.py의 get_ecommerce_template 함수 본문 전체 복사) -->
""" 