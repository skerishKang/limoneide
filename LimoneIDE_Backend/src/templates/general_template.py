"""
🍋 LimoneIDE General Template
일반 웹사이트 템플릿
"""

import asyncio
from typing import Dict, Any, List

class GeneralTemplate:
    """
    LimoneIDE 일반 웹사이트 템플릿
    - 기본 HTML, CSS, JS 생성
    - 반응형 디자인
    """
    
    def __init__(self):
        self.template_name = "general"
        self.template_description = "기본 웹사이트 템플릿"
    
    async def generate_code(self, command: str, features: List[str] = None) -> Dict[str, str]:
        """
        웹사이트 코드 생성
        
        Args:
            command: 사용자 명령
            features: 웹사이트 기능 목록
            
        Returns:
            Dict: 생성된 웹사이트 코드 (HTML, CSS, JS)
        """
        if features is None:
            features = ["basic_layout", "responsive"]
        
        # 실제 구현에서는 AI 모델을 사용하여 코드 생성
        # 현재는 기본 템플릿 반환
        
        html = self._generate_html(command, features)
        css = self._generate_css(features)
        js = self._generate_js(features)
        
        return {
            "html": html,
            "css": css,
            "js": js
        }
    
    def _generate_html(self, command: str, features: List[str]) -> str:
        """
        HTML 코드 생성
        """
        title = "LimoneIDE 웹사이트"
        description = "AI로 생성된 웹사이트"
        
        # 명령에서 제목 추출 시도
        if ":" in command:
            title_part = command.split(":", 1)[1].strip()
            if title_part:
                title = title_part
                
        # 기본 HTML 구조
        html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <link rel="stylesheet" href="styles.css">
    <link rel="icon" href="favicon.ico" type="image/x-icon">
</head>
<body>
    <header class="site-header">
        <div class="container">
            <div class="logo">
                <h1>{title}</h1>
            </div>
            <nav class="main-nav">
                <ul>
                    <li><a href="#home">홈</a></li>
                    <li><a href="#about">소개</a></li>
                    <li><a href="#services">서비스</a></li>
                    <li><a href="#contact">연락처</a></li>
                </ul>
            </nav>
            <div class="mobile-menu-toggle">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    </header>

    <main>
        <section id="home" class="hero-section">
            <div class="container">
                <h2>환영합니다</h2>
                <p>LimoneIDE로 생성된 웹사이트입니다.</p>
                <a href="#contact" class="btn primary-btn">문의하기</a>
            </div>
        </section>

        <section id="about" class="about-section">
            <div class="container">
                <h2>소개</h2>
                <div class="about-content">
                    <div class="about-text">
                        <p>이 웹사이트는 LimoneIDE의 AI 기술로 자동 생성되었습니다.</p>
                        <p>원하는 대로 수정하고 확장할 수 있습니다.</p>
                    </div>
                    <div class="about-image">
                        <img src="https://via.placeholder.com/400x300" alt="소개 이미지">
                    </div>
                </div>
            </div>
        </section>

        <section id="services" class="services-section">
            <div class="container">
                <h2>서비스</h2>
                <div class="services-grid">
                    <div class="service-card">
                        <div class="service-icon">🚀</div>
                        <h3>빠른 시작</h3>
                        <p>몇 분 안에 웹사이트를 생성하고 배포합니다.</p>
                    </div>
                    <div class="service-card">
                        <div class="service-icon">🎨</div>
                        <h3>맞춤 디자인</h3>
                        <p>원하는 스타일로 디자인을 변경할 수 있습니다.</p>
                    </div>
                    <div class="service-card">
                        <div class="service-icon">📱</div>
                        <h3>반응형 레이아웃</h3>
                        <p>모든 디바이스에서 완벽하게 작동합니다.</p>
                    </div>
                </div>
            </div>
        </section>

        <section id="contact" class="contact-section">
            <div class="container">
                <h2>연락처</h2>
                <div class="contact-form">
                    <form>
                        <div class="form-group">
                            <label for="name">이름</label>
                            <input type="text" id="name" name="name" required>
                        </div>
                        <div class="form-group">
                            <label for="email">이메일</label>
                            <input type="email" id="email" name="email" required>
                        </div>
                        <div class="form-group">
                            <label for="message">메시지</label>
                            <textarea id="message" name="message" rows="5" required></textarea>
                        </div>
                        <button type="submit" class="btn primary-btn">보내기</button>
                    </form>
                </div>
            </div>
        </section>
    </main>

    <footer class="site-footer">
        <div class="container">
            <p>&copy; 2025 {title}. All rights reserved.</p>
            <p>Powered by <a href="https://limoneide.com" target="_blank">LimoneIDE</a></p>
        </div>
    </footer>

    <script src="app.js"></script>
</body>
</html>"""
        
        return html
    
    def _generate_css(self, features: List[str]) -> str:
        """
        CSS 코드 생성
        """
        css = """/* 🍋 LimoneIDE 생성 스타일시트 */

/* 기본 스타일 리셋 */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

/* 기본 스타일 */
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: #333;
    background-color: #f9f9f9;
}

.container {
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

/* 타이포그래피 */
h1, h2, h3, h4, h5, h6 {
    font-weight: 700;
    line-height: 1.2;
    margin-bottom: 1rem;
    color: #222;
}

h1 {
    font-size: 2.5rem;
}

h2 {
    font-size: 2rem;
    text-align: center;
    margin-bottom: 2rem;
}

h3 {
    font-size: 1.5rem;
}

p {
    margin-bottom: 1rem;
}

a {
    color: #4ade80;
    text-decoration: none;
    transition: color 0.3s ease;
}

a:hover {
    color: #22c55e;
}

/* 버튼 */
.btn {
    display: inline-block;
    padding: 0.8rem 1.5rem;
    background-color: #4ade80;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-weight: 600;
    text-align: center;
    transition: background-color 0.3s ease;
}

.btn:hover {
    background-color: #22c55e;
}

.primary-btn {
    background-color: #4ade80;
}

.secondary-btn {
    background-color: #64748b;
}

/* 헤더 */
.site-header {
    background-color: white;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    position: sticky;
    top: 0;
    z-index: 100;
}

.site-header .container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 80px;
}

.logo h1 {
    font-size: 1.8rem;
    margin: 0;
}

/* 네비게이션 */
.main-nav ul {
    display: flex;
    list-style: none;
}

.main-nav li {
    margin-left: 1.5rem;
}

.main-nav a {
    color: #333;
    font-weight: 500;
}

.main-nav a:hover {
    color: #4ade80;
}

.mobile-menu-toggle {
    display: none;
    flex-direction: column;
    cursor: pointer;
}

.mobile-menu-toggle span {
    display: block;
    width: 25px;
    height: 3px;
    background-color: #333;
    margin: 2px 0;
    transition: all 0.3s ease;
}

/* 히어로 섹션 */
.hero-section {
    background-color: #4ade80;
    color: white;
    text-align: center;
    padding: 6rem 0;
}

.hero-section h2 {
    font-size: 3rem;
    margin-bottom: 1rem;
    color: white;
}

.hero-section p {
    font-size: 1.2rem;
    margin-bottom: 2rem;
}

.hero-section .btn {
    background-color: white;
    color: #4ade80;
}

.hero-section .btn:hover {
    background-color: #f9f9f9;
}

/* 섹션 공통 */
section {
    padding: 5rem 0;
}

/* 소개 섹션 */
.about-content {
    display: flex;
    align-items: center;
    gap: 2rem;
}

.about-text {
    flex: 1;
}

.about-image {
    flex: 1;
}

.about-image img {
    width: 100%;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

/* 서비스 섹션 */
.services-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
}

.service-card {
    background-color: white;
    border-radius: 8px;
    padding: 2rem;
    text-align: center;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
}

.service-card:hover {
    transform: translateY(-5px);
}

.service-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
}

/* 연락처 섹션 */
.contact-form {
    max-width: 600px;
    margin: 0 auto;
    background-color: white;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.form-group {
    margin-bottom: 1.5rem;
}

.form-group label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
}

.form-group input,
.form-group textarea {
    width: 100%;
    padding: 0.8rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-family: inherit;
    font-size: 1rem;
}

.form-group input:focus,
.form-group textarea:focus {
    border-color: #4ade80;
    outline: none;
}

/* 푸터 */
.site-footer {
    background-color: #333;
    color: white;
    padding: 2rem 0;
    text-align: center;
}

.site-footer a {
    color: #4ade80;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
    .site-header .container {
        height: 70px;
    }
    
    .mobile-menu-toggle {
        display: flex;
    }
    
    .main-nav {
        position: absolute;
        top: 70px;
        left: 0;
        right: 0;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        padding: 1rem 0;
        display: none;
    }
    
    .main-nav.active {
        display: block;
    }
    
    .main-nav ul {
        flex-direction: column;
    }
    
    .main-nav li {
        margin: 0;
    }
    
    .main-nav a {
        display: block;
        padding: 0.8rem 1.5rem;
    }
    
    .about-content {
        flex-direction: column;
    }
    
    .hero-section {
        padding: 4rem 0;
    }
    
    .hero-section h2 {
        font-size: 2.5rem;
    }
}

@media (max-width: 480px) {
    h1 {
        font-size: 2rem;
    }
    
    h2 {
        font-size: 1.8rem;
    }
    
    .hero-section h2 {
        font-size: 2rem;
    }
    
    .hero-section {
        padding: 3rem 0;
    }
    
    section {
        padding: 3rem 0;
    }
}"""
        
        return css
    
    def _generate_js(self, features: List[str]) -> str:
        """
        JavaScript 코드 생성
        """
        js = """// 🍋 LimoneIDE 생성 자바스크립트

// DOM이 로드된 후 실행
document.addEventListener('DOMContentLoaded', function() {
    console.log('LimoneIDE 웹사이트가 로드되었습니다.');
    
    // 모바일 메뉴 토글
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const mainNav = document.querySelector('.main-nav');
    
    if (mobileMenuToggle && mainNav) {
        mobileMenuToggle.addEventListener('click', function() {
            mainNav.classList.toggle('active');
        });
    }
    
    // 스크롤 애니메이션
    const scrollElements = document.querySelectorAll('.service-card, .about-content');
    
    const elementInView = (el, percentageScroll = 100) => {
        const elementTop = el.getBoundingClientRect().top;
        return (
            elementTop <= 
            ((window.innerHeight || document.documentElement.clientHeight) * (percentageScroll/100))
        );
    };
    
    const displayScrollElement = (element) => {
        element.classList.add('scrolled');
    };
    
    const hideScrollElement = (element) => {
        element.classList.remove('scrolled');
    };
    
    const handleScrollAnimation = () => {
        scrollElements.forEach((el) => {
            if (elementInView(el, 80)) {
                displayScrollElement(el);
            } else {
                hideScrollElement(el);
            }
        });
    };
    
    window.addEventListener('scroll', () => {
        handleScrollAnimation();
    });
    
    // 폼 제출 처리
    const contactForm = document.querySelector('.contact-form form');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // 폼 데이터 수집
            const formData = {
                name: document.getElementById('name').value,
                email: document.getElementById('email').value,
                message: document.getElementById('message').value
            };
            
            console.log('폼 제출:', formData);
            
            // 여기에 실제 폼 제출 로직 추가
            alert('메시지가 전송되었습니다. 감사합니다!');
            contactForm.reset();
        });
    }
    
    // 스무스 스크롤
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80,
                    behavior: 'smooth'
                });
                
                // 모바일 메뉴 닫기
                if (mainNav.classList.contains('active')) {
                    mainNav.classList.remove('active');
                }
            }
        });
    });
});"""
        
        return js 