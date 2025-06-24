"""
🍋 LimoneIDE Website Builder
Alpine.js 기반 웹사이트 자동 생성 엔진
"""

from typing import Dict, Any, List

class WebsiteBuilder:
    """
    LimoneIDE 웹사이트 빌더
    - 요구사항 → Alpine.js 코드 자동 생성
    - 모바일 최적화 템플릿
    - 반응형 디자인 자동 적용
    """
    
    def __init__(self):
        self.templates = {
            "ecommerce": self.get_ecommerce_template,
            "blog": self.get_blog_template,
            "portfolio": self.get_portfolio_template,
            "landing": self.get_landing_template
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

    def get_ecommerce_template(self, features: List[str]) -> str:
        """
        쇼핑몰 템플릿 생성
        """
        return f"""
<div x-data="ecommerceStore()" class="container mx-auto px-4 py-8">
    <header class="text-center mb-8">
        <h1 class="text-4xl font-bold text-gray-800 mb-2">🛍️ 온라인 쇼핑몰</h1>
        <p class="text-gray-600">최고의 상품을 만나보세요</p>
    </header>
    
    <!-- 상품 목록 -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        <template x-for="product in products" :key="product.id">
            <div class="bg-white rounded-lg shadow-md overflow-hidden">
                <img :src="product.image" :alt="product.name" class="w-full h-48 object-cover">
                <div class="p-4">
                    <h3 class="text-lg font-semibold mb-2" x-text="product.name"></h3>
                    <p class="text-gray-600 mb-2" x-text="product.description"></p>
                    <div class="flex justify-between items-center">
                        <span class="text-xl font-bold text-blue-600" x-text="'₩' + product.price"></span>
                        <button @click="addToCart(product)" 
                                class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
                            장바구니 추가
                        </button>
                    </div>
                </div>
            </div>
        </template>
    </div>
    
    <!-- 장바구니 -->
    <div x-show="cart.length > 0" class="bg-white rounded-lg shadow-md p-6">
        <h2 class="text-2xl font-bold mb-4">🛒 장바구니</h2>
        <template x-for="item in cart" :key="item.id">
            <div class="flex justify-between items-center py-2 border-b">
                <span x-text="item.name"></span>
                <span x-text="'₩' + item.price"></span>
            </div>
        </template>
        <div class="mt-4 text-right">
            <p class="text-xl font-bold">총액: ₩<span x-text="getTotal()"></span></p>
            <button @click="checkout()" 
                    class="bg-green-500 text-white px-6 py-2 rounded hover:bg-green-600 mt-2">
                결제하기
            </button>
        </div>
    </div>
</div>

<script>
function ecommerceStore() {{
    return {{
        products: [
            {{
                id: 1,
                name: "프리미엄 케이크",
                description: "신선한 재료로 만든 맛있는 케이크",
                price: 25000,
                image: "https://via.placeholder.com/300x200?text=Cake"
            }},
            {{
                id: 2,
                name: "생일 케이크",
                description: "특별한 날을 위한 생일 케이크",
                price: 35000,
                image: "https://via.placeholder.com/300x200?text=Birthday"
            }}
        ],
        cart: [],
        
        addToCart(product) {{
            this.cart.push({{...product}});
            alert('장바구니에 추가되었습니다!');
        }},
        
        getTotal() {{
            return this.cart.reduce((sum, item) => sum + item.price, 0);
        }},
        
        checkout() {{
            alert('결제가 완료되었습니다!');
            this.cart = [];
        }}
    }}
}}
</script>
        """

    def get_blog_template(self, features: List[str]) -> str:
        """
        블로그 템플릿 생성
        """
        return f"""
<div x-data="blogSystem()" class="container mx-auto px-4 py-8">
    <header class="text-center mb-8">
        <h1 class="text-4xl font-bold text-gray-800 mb-2">📝 내 블로그</h1>
        <p class="text-gray-600">생각을 나누는 공간</p>
    </header>
    
    <!-- 글쓰기 폼 -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-8">
        <h2 class="text-2xl font-bold mb-4">새 글 작성</h2>
        <input x-model="newPost.title" 
               placeholder="제목을 입력하세요" 
               class="w-full p-2 border rounded mb-4">
        <textarea x-model="newPost.content" 
                  placeholder="내용을 입력하세요" 
                  class="w-full p-2 border rounded mb-4 h-32"></textarea>
        <button @click="addPost()" 
                class="bg-blue-500 text-white px-6 py-2 rounded hover:bg-blue-600">
            글 작성
        </button>
    </div>
    
    <!-- 글 목록 -->
    <div class="space-y-6">
        <template x-for="post in posts" :key="post.id">
            <article class="bg-white rounded-lg shadow-md p-6">
                <h3 class="text-2xl font-bold mb-2" x-text="post.title"></h3>
                <p class="text-gray-600 mb-4" x-text="post.content"></p>
                <div class="flex justify-between items-center text-sm text-gray-500">
                    <span x-text="post.date"></span>
                    <button @click="deletePost(post.id)" 
                            class="text-red-500 hover:text-red-700">
                        삭제
                    </button>
                </div>
            </article>
        </template>
    </div>
</div>

<script>
function blogSystem() {{
    return {{
        posts: [
            {{
                id: 1,
                title: "첫 번째 블로그 글",
                content: "안녕하세요! 이것은 첫 번째 블로그 글입니다.",
                date: "2025-01-27"
            }}
        ],
        newPost: {{ title: '', content: '' }},
        
        addPost() {{
            if (this.newPost.title && this.newPost.content) {{
                this.posts.unshift({{
                    id: Date.now(),
                    title: this.newPost.title,
                    content: this.newPost.content,
                    date: new Date().toISOString().split('T')[0]
                }});
                this.newPost = {{ title: '', content: '' }};
            }}
        }},
        
        deletePost(id) {{
            this.posts = this.posts.filter(post => post.id !== id);
        }}
    }}
}}
</script>
        """

    def get_portfolio_template(self, features: List[str]) -> str:
        """
        포트폴리오 템플릿 생성
        """
        return f"""
<div x-data="portfolio()" class="container mx-auto px-4 py-8">
    <header class="text-center mb-8">
        <h1 class="text-4xl font-bold text-gray-800 mb-2">🎨 포트폴리오</h1>
        <p class="text-gray-600">작품들을 소개합니다</p>
    </header>
    
    <!-- 프로젝트 목록 -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <template x-for="project in projects" :key="project.id">
            <div class="bg-white rounded-lg shadow-md overflow-hidden">
                <img :src="project.image" :alt="project.title" class="w-full h-48 object-cover">
                <div class="p-4">
                    <h3 class="text-xl font-bold mb-2" x-text="project.title"></h3>
                    <p class="text-gray-600 mb-4" x-text="project.description"></p>
                    <div class="flex flex-wrap gap-2">
                        <template x-for="tech in project.technologies" :key="tech">
                            <span class="bg-blue-100 text-blue-800 px-2 py-1 rounded text-sm" x-text="tech"></span>
                        </template>
                    </div>
                </div>
            </div>
        </template>
    </div>
</div>

<script>
function portfolio() {{
    return {{
        projects: [
            {{
                id: 1,
                title: "LimoneIDE",
                description: "AI 기반 모바일 자동화 플랫폼",
                image: "https://via.placeholder.com/400x300?text=LimoneIDE",
                technologies: ["Python", "Alpine.js", "AI"]
            }},
            {{
                id: 2,
                title: "웹 쇼핑몰",
                description: "반응형 온라인 쇼핑몰",
                image: "https://via.placeholder.com/400x300?text=E-commerce",
                technologies: ["React", "Node.js", "MongoDB"]
            }}
        ]
    }}
}}
</script>
        """

    def get_landing_template(self, features: List[str]) -> str:
        """
        랜딩 페이지 템플릿 생성
        """
        return f"""
<div x-data="landingPage()" class="min-h-screen">
    <!-- 히어로 섹션 -->
    <section class="bg-gradient-to-r from-blue-500 to-purple-600 text-white py-20">
        <div class="container mx-auto px-4 text-center">
            <h1 class="text-5xl font-bold mb-4">🚀 혁신적인 솔루션</h1>
            <p class="text-xl mb-8">미래를 만드는 기술</p>
            <button @click="scrollToContact()" 
                    class="bg-white text-blue-600 px-8 py-3 rounded-lg text-lg font-semibold hover:bg-gray-100">
                시작하기
            </button>
        </div>
    </section>
    
    <!-- 특징 섹션 -->
    <section class="py-16 bg-gray-50">
        <div class="container mx-auto px-4">
            <h2 class="text-3xl font-bold text-center mb-12">주요 특징</h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div class="text-center">
                    <div class="text-4xl mb-4">⚡</div>
                    <h3 class="text-xl font-bold mb-2">빠른 성능</h3>
                    <p class="text-gray-600">최적화된 성능으로 빠른 응답</p>
                </div>
                <div class="text-center">
                    <div class="text-4xl mb-4">🔒</div>
                    <h3 class="text-xl font-bold mb-2">안전한 보안</h3>
                    <p class="text-gray-600">엔터프라이즈급 보안 시스템</p>
                </div>
                <div class="text-center">
                    <div class="text-4xl mb-4">📱</div>
                    <h3 class="text-xl font-bold mb-2">모바일 최적화</h3>
                    <p class="text-gray-600">모든 기기에서 완벽한 경험</p>
                </div>
            </div>
        </div>
    </section>
    
    <!-- 연락처 섹션 -->
    <section id="contact" class="py-16">
        <div class="container mx-auto px-4 text-center">
            <h2 class="text-3xl font-bold mb-8">연락하기</h2>
            <div class="max-w-md mx-auto">
                <input x-model="contact.email" 
                       placeholder="이메일 주소" 
                       class="w-full p-3 border rounded mb-4">
                <textarea x-model="contact.message" 
                          placeholder="메시지" 
                          class="w-full p-3 border rounded mb-4 h-32"></textarea>
                <button @click="sendMessage()" 
                        class="bg-blue-500 text-white px-8 py-3 rounded hover:bg-blue-600">
                    메시지 보내기
                </button>
            </div>
        </div>
    </section>
</div>

<script>
function landingPage() {{
    return {{
        contact: {{ email: '', message: '' }},
        
        scrollToContact() {{
            document.getElementById('contact').scrollIntoView({{ behavior: 'smooth' }});
        }},
        
        sendMessage() {{
            if (this.contact.email && this.contact.message) {{
                alert('메시지가 전송되었습니다!');
                this.contact = {{ email: '', message: '' }};
            }}
        }}
    }}
}}
</script>
        """

    def get_general_template(self, features: List[str]) -> str:
        """
        일반 템플릿 생성
        """
        return f"""
<div x-data="generalPage()" class="container mx-auto px-4 py-8">
    <header class="text-center mb-8">
        <h1 class="text-4xl font-bold text-gray-800 mb-2">🍋 LimoneIDE 생성 웹사이트</h1>
        <p class="text-gray-600">AI가 만든 맞춤형 웹사이트</p>
    </header>
    
    <div class="bg-white rounded-lg shadow-md p-6">
        <h2 class="text-2xl font-bold mb-4">환영합니다!</h2>
        <p class="text-gray-600 mb-4">
            이 웹사이트는 LimoneIDE의 AI가 자동으로 생성했습니다.
            음성 명령만으로 30초 만에 완성된 웹사이트입니다.
        </p>
        <button @click="showInfo()" 
                class="bg-blue-500 text-white px-6 py-2 rounded hover:bg-blue-600">
            자세히 보기
        </button>
    </div>
</div>

<script>
function generalPage() {{
    return {{
        showInfo() {{
            alert('LimoneIDE는 AI 기반 모바일 자동화 플랫폼입니다!');
        }}
    }}
}}
</script>
        """ 