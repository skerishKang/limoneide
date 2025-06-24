"""
🍋 LimoneIDE Website Builder
Alpine.js 기반 웹사이트 자동 생성 엔진
"""

from typing import Dict, Any, List
from src.templates.ecommerce_template import get_ecommerce_template
from src.templates.blog_template import get_blog_template
from src.templates.portfolio_template import get_portfolio_template
from src.templates.landing_template import get_landing_template
from src.templates.general_template import get_general_template

class WebsiteBuilder:
    """
    LimoneIDE 웹사이트 빌더
    - 요구사항 → Alpine.js 코드 자동 생성
    - 모바일 최적화 템플릿
    - 반응형 디자인 자동 적용
    """
    
    def __init__(self):
        self.templates = {
            "ecommerce": get_ecommerce_template,
            "blog": get_blog_template,
            "portfolio": get_portfolio_template,
            "landing": get_landing_template
        }

    def build_website(self, requirements: Dict[str, Any]) -> str:
        """
        요구사항을 받아 완전한 웹사이트 HTML 생성
        """
        website_type = requirements.get("website_type", "general")
        features = requirements.get("features", [])
        
        # 템플릿 선택
        template_func = self.templates.get(website_type, self.get_general_template)
        template = template_func(features)
        
        # 완전한 HTML 문서 생성
        html = self.generate_complete_html(template, requirements)
        
        return html

    def generate_complete_html(self, template: str, requirements: Dict[str, Any]) -> str:
        """
        완전한 HTML 문서 생성
        """
        title = requirements.get("title", "LimoneIDE 생성 웹사이트")
        
        return f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script defer src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        /* 모바일 최적화 스타일 */
        @media (max-width: 768px) {{
            .mobile-optimized {{
                padding: 1rem;
                font-size: 16px;
            }}
        }}
    </style>
</head>
<body class="bg-gray-50">
    {template}
    
    <footer class="bg-gray-800 text-white text-center py-4 mt-8">
        <p>🍋 Powered by LimoneIDE</p>
    </footer>
</body>
</html>
        """ 