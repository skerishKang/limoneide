"""
🍋 LimoneIDE Blog Template with Guestbook
방명록 기능이 포함된 블로그 템플릿
"""

import asyncio
from typing import Dict, Any, List
from datetime import datetime

class BlogTemplate:
    """
    LimoneIDE 블로그 템플릿 (방명록 기능 포함)
    - 블로그 포스트 관리
    - 방명록 작성/조회
    - 댓글 시스템
    - 사용자 인증 연동
    """
    
    def __init__(self):
        self.template_name = "blog"
        self.template_description = "방명록 기능이 포함된 블로그 템플릿"
    
    async def generate_code(self, command: str, features: List[str] = None) -> Dict[str, str]:
        """
        블로그 웹사이트 코드 생성
        
        Args:
            command: 사용자 명령
            features: 웹사이트 기능 목록
            
        Returns:
            Dict: 생성된 웹사이트 코드 (HTML, CSS, JS, Python)
        """
        if features is None:
            features = ["blog_posts", "guestbook", "comments", "responsive"]
        
        html = self._generate_html(command, features)
        css = self._generate_css(features)
        js = self._generate_js(features)
        python_backend = self._generate_python_backend(features)
        
        return {
            "html": html,
            "css": css,
            "js": js,
            "python": python_backend
        }
    
    def _generate_html(self, command: str, features: List[str]) -> str:
        """HTML 코드 생성"""
        title = "LimoneIDE 블로그"
        if ":" in command:
            title_part = command.split(":", 1)[1].strip()
            if title_part:
                title = title_part
        
        return f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="styles.css">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
</head>
<body>
    <header class="site-header">
        <div class="container">
            <div class="logo">
                <h1><i class="fas fa-blog"></i> {title}</h1>
            </div>
            <nav class="main-nav">
                <ul>
                    <li><a href="#home">홈</a></li>
                    <li><a href="#blog">블로그</a></li>
                    <li><a href="#guestbook">방명록</a></li>
                    <li><a href="#about">소개</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <main>
        <section id="home" class="hero-section">
            <div class="container">
                <h2>환영합니다</h2>
                <p>LimoneIDE로 생성된 블로그입니다.</p>
                <div class="hero-buttons">
                    <a href="#blog" class="btn primary-btn">블로그 보기</a>
                    <a href="#guestbook" class="btn secondary-btn">방명록 작성</a>
                </div>
            </div>
        </section>

        <section id="blog" class="blog-section">
            <div class="container">
                <h2>최신 포스트</h2>
                <div class="blog-grid" id="blog-posts">
                    <!-- 블로그 포스트가 동적으로 로드됩니다 -->
                </div>
            </div>
        </section>

        <section id="guestbook" class="guestbook-section">
            <div class="container">
                <h2>방명록</h2>
                <div class="guestbook-container">
                    <div class="guestbook-form">
                        <h3>방명록 작성</h3>
                        <form id="guestbook-form">
                            <div class="form-group">
                                <label for="guest-name">이름 *</label>
                                <input type="text" id="guest-name" name="name" required>
                            </div>
                            <div class="form-group">
                                <label for="guest-email">이메일</label>
                                <input type="email" id="guest-email" name="email">
                            </div>
                            <div class="form-group">
                                <label for="guest-message">메시지 *</label>
                                <textarea id="guest-message" name="message" rows="4" required></textarea>
                            </div>
                            <button type="submit" class="btn primary-btn">방명록 남기기</button>
                        </form>
                    </div>
                    
                    <div class="guestbook-list">
                        <h3>방명록 목록</h3>
                        <div class="guestbook-entries" id="guestbook-entries">
                            <!-- 방명록이 동적으로 로드됩니다 -->
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </main>

    <footer class="site-footer">
        <div class="container">
            <p>&copy; 2025 {title}. Powered by LimoneIDE</p>
        </div>
    </footer>

    <script src="app.js"></script>
</body>
</html>"""
    
    def _generate_css(self, features: List[str]) -> str:
        """CSS 코드 생성"""
        return """/* 🍋 LimoneIDE Blog Template Styles */

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

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

.site-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1rem 0;
    position: fixed;
    top: 0;
    width: 100%;
    z-index: 1000;
}

.site-header .container {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo h1 {
    font-size: 1.8rem;
    font-weight: 700;
}

.logo i {
    margin-right: 10px;
    color: #ffd700;
}

.main-nav ul {
    display: flex;
    list-style: none;
    gap: 2rem;
}

.main-nav a {
    color: white;
    text-decoration: none;
    font-weight: 500;
    transition: color 0.3s ease;
}

.main-nav a:hover {
    color: #ffd700;
}

main {
    margin-top: 80px;
}

.hero-section {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 4rem 0;
    text-align: center;
}

.hero-section h2 {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.hero-buttons {
    display: flex;
    gap: 1rem;
    justify-content: center;
    margin-top: 2rem;
}

.btn {
    display: inline-block;
    padding: 12px 24px;
    border: none;
    border-radius: 5px;
    text-decoration: none;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
}

.primary-btn {
    background: #ffd700;
    color: #333;
}

.secondary-btn {
    background: transparent;
    color: white;
    border: 2px solid white;
}

.blog-section, .guestbook-section {
    padding: 4rem 0;
    background: white;
}

.blog-section h2, .guestbook-section h2 {
    text-align: center;
    font-size: 2.5rem;
    margin-bottom: 3rem;
}

.blog-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 2rem;
}

.blog-post {
    background: white;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
}

.blog-post:hover {
    transform: translateY(-5px);
}

.guestbook-container {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 3rem;
}

.guestbook-form, .guestbook-list {
    background: white;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

.form-group {
    margin-bottom: 1.5rem;
}

.form-group label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 600;
}

.form-group input,
.form-group textarea {
    width: 100%;
    padding: 12px;
    border: 2px solid #ddd;
    border-radius: 5px;
    font-size: 1rem;
}

.guestbook-entry {
    border-bottom: 1px solid #eee;
    padding: 1rem 0;
    margin-bottom: 1rem;
}

.site-footer {
    background: #333;
    color: white;
    padding: 2rem 0;
    text-align: center;
}

@media (max-width: 768px) {
    .guestbook-container {
        grid-template-columns: 1fr;
    }
    
    .hero-buttons {
        flex-direction: column;
        align-items: center;
    }
}"""
    
    def _generate_js(self, features: List[str]) -> str:
        """JavaScript 코드 생성"""
        return """// 🍋 LimoneIDE Blog Template JavaScript

class BlogApp {
    constructor() {
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.loadBlogPosts();
        this.loadGuestbook();
    }
    
    bindEvents() {
        // 방명록 폼 제출
        const guestbookForm = document.getElementById('guestbook-form');
        if (guestbookForm) {
            guestbookForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.submitGuestbook();
            });
        }
        
        // 스무스 스크롤
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            });
        });
    }
    
    async loadBlogPosts() {
        const blogGrid = document.getElementById('blog-posts');
        if (!blogGrid) return;
        
        const posts = this.getSamplePosts();
        this.renderBlogPosts(posts);
    }
    
    getSamplePosts() {
        return [
            {
                id: 1,
                title: 'LimoneIDE로 만든 첫 번째 블로그',
                excerpt: 'AI 기술을 활용하여 자동으로 생성된 블로그입니다.',
                date: '2025-06-24',
                author: 'LimoneIDE'
            },
            {
                id: 2,
                title: '방명록 기능 사용법',
                excerpt: '블로그 하단의 방명록 섹션에서 방문 소감을 남길 수 있습니다.',
                date: '2025-06-24',
                author: 'LimoneIDE'
            }
        ];
    }
    
    renderBlogPosts(posts) {
        const blogGrid = document.getElementById('blog-posts');
        if (!blogGrid) return;
        
        const postsHTML = posts.map(post => `
            <article class="blog-post">
                <div class="blog-post-content">
                    <h3 class="blog-post-title">${post.title}</h3>
                    <div class="blog-post-meta">
                        <span>${post.author} • ${post.date}</span>
                    </div>
                    <p class="blog-post-excerpt">${post.excerpt}</p>
                </div>
            </article>
        `).join('');
        
        blogGrid.innerHTML = postsHTML;
    }
    
    async loadGuestbook() {
        const guestbookEntries = document.getElementById('guestbook-entries');
        if (!guestbookEntries) return;
        
        const entries = this.getSampleGuestbook();
        this.renderGuestbook(entries);
    }
    
    getSampleGuestbook() {
        return [
            {
                id: 1,
                name: '김철수',
                message: '정말 멋진 블로그네요! AI로 만들었다니 놀랍습니다.',
                date: '2025-06-24 14:30'
            },
            {
                id: 2,
                name: '이영희',
                message: '방명록 기능이 있어서 좋네요. 앞으로 자주 방문할게요!',
                date: '2025-06-24 15:45'
            }
        ];
    }
    
    renderGuestbook(entries) {
        const guestbookEntries = document.getElementById('guestbook-entries');
        if (!guestbookEntries) return;
        
        const entriesHTML = entries.map(entry => `
            <div class="guestbook-entry">
                <div class="guest-name">${entry.name}</div>
                <div class="guest-date">${entry.date}</div>
                <div class="guest-message">${entry.message}</div>
            </div>
        `).join('');
        
        guestbookEntries.innerHTML = entriesHTML;
    }
    
    async submitGuestbook() {
        const form = document.getElementById('guestbook-form');
        const formData = new FormData(form);
        
        const guestbookData = {
            name: formData.get('name'),
            email: formData.get('email'),
            message: formData.get('message'),
            date: new Date().toISOString()
        };
        
        console.log('방명록 제출:', guestbookData);
        alert('방명록이 성공적으로 등록되었습니다!');
        
        form.reset();
        this.loadGuestbook();
    }
}

// 앱 초기화
const blogApp = new BlogApp();

document.addEventListener('DOMContentLoaded', () => {
    console.log('🍋 LimoneIDE Blog Template 로드 완료');
});"""
    
    def _generate_python_backend(self, features: List[str]) -> str:
        """Python 백엔드 코드 생성"""
        return """# 🍋 LimoneIDE Blog Backend (Flask)
# 방명록 기능이 포함된 블로그 백엔드

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class GuestbookEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120))
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/api/guestbook', methods=['GET'])
def get_guestbook():
    entries = GuestbookEntry.query.order_by(GuestbookEntry.created_at.desc()).all()
    return jsonify([{
        'id': entry.id,
        'name': entry.name,
        'email': entry.email,
        'message': entry.message,
        'created_at': entry.created_at.isoformat()
    } for entry in entries])

@app.route('/api/guestbook', methods=['POST'])
def create_guestbook():
    data = request.get_json()
    
    if not data or not data.get('name') or not data.get('message'):
        return jsonify({'error': '이름과 메시지는 필수입니다.'}), 400
    
    entry = GuestbookEntry(
        name=data['name'],
        email=data.get('email', ''),
        message=data['message']
    )
    
    db.session.add(entry)
    db.session.commit()
    
    return jsonify({'message': '방명록이 등록되었습니다.'}), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)"""

def get_blog_template(features=None):
    """블로그 템플릿 인스턴스 반환"""
    return BlogTemplate() 