"""
🍋 LimoneIDE AI Engine
여러 AI 모델을 통합하여 음성 명령 처리, 코드 생성, RAG 시스템 등을 제공
"""

import os
import json
import asyncio
import logging
from typing import Dict, Any, List, Optional, Union
from datetime import datetime

from .ai_openai import OpenAIService
from .ai_gemini import GeminiService
from .ai_claude import ClaudeService
from .ai_ollama import OllamaService
from ..templates.general_template import GeneralTemplate
from ..templates.landing_template import LandingTemplate
from ..templates.blog_template import BlogTemplate
from ..templates.ecommerce_template import EcommerceTemplate
from ..templates.portfolio_template import PortfolioTemplate

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('ai_engine')

class AIEngine:
    """
    LimoneIDE AI 엔진
    - 음성 명령 처리
    - 코드 생성
    - RAG 시스템
    """
    
    def __init__(self):
        """AI 엔진 초기화"""
        self.models = {
            "openai": self._init_openai(),
            "gemini": self._init_gemini(),
            "claude": self._init_claude(),
            "ollama": self._init_ollama()
        }
        self.default_model = "gemini"  # 기본 모델 설정
        
        # AI 서비스 초기화
        self.openai_service = OpenAIService()
        self.gemini_service = GeminiService()
        self.claude_service = ClaudeService()
        self.ollama_service = OllamaService()
        
        # 기본 AI 서비스 설정
        self.default_service = "openai"  # 환경 변수에서 가져올 수 있음
        
        # 웹사이트 템플릿 초기화
        self.templates = {
            "general": GeneralTemplate(),
            "landing": LandingTemplate(),
            "blog": BlogTemplate(),
            "ecommerce": EcommerceTemplate(),
            "portfolio": PortfolioTemplate()
        }
        
        # 명령 히스토리
        self.command_history = []
    
    def _init_openai(self) -> Dict[str, Any]:
        """OpenAI 모델 초기화"""
        api_key = os.environ.get("OPENAI_API_KEY", "")
        return {
            "name": "OpenAI",
            "api_key": api_key,
            "available": bool(api_key),
            "models": ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"]
        }
    
    def _init_gemini(self) -> Dict[str, Any]:
        """Google Gemini 모델 초기화"""
        api_key = os.environ.get("GEMINI_API_KEY", "")
        return {
            "name": "Gemini",
            "api_key": api_key,
            "available": bool(api_key),
            "models": ["gemini-1.5-pro", "gemini-1.0-pro"]
        }
    
    def _init_claude(self) -> Dict[str, Any]:
        """Anthropic Claude 모델 초기화"""
        api_key = os.environ.get("CLAUDE_API_KEY", "")
        return {
            "name": "Claude",
            "api_key": api_key,
            "available": bool(api_key),
            "models": ["claude-3-opus", "claude-3-sonnet"]
        }
    
    def _init_ollama(self) -> Dict[str, Any]:
        """Ollama 로컬 모델 초기화"""
        ollama_host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
        return {
            "name": "Ollama",
            "host": ollama_host,
            "available": True,  # 로컬에서 실행 중인지는 실제 호출 시 확인
            "models": ["llama3", "mistral", "codellama"]
        }
    
    async def process_command(self, command: str) -> Dict[str, Any]:
        """
        음성 명령 처리
        
        Args:
            command: 사용자 음성 명령 텍스트
            
        Returns:
            Dict: 처리 결과
        """
        try:
            logger.info(f"명령 처리 시작: {command[:30]}...")
            
            # 명령 히스토리에 추가
            self.command_history.append({
                "command": command,
                "timestamp": datetime.now().isoformat()
            })
            
            # 기본 AI 서비스로 명령 처리
            if self.default_service == "openai":
                response = await self.openai_service.generate_response(command)
            elif self.default_service == "gemini":
                response = await self.gemini_service.generate_response(command)
            elif self.default_service == "claude":
                response = await self.claude_service.generate_response(command)
            elif self.default_service == "ollama":
                response = await self.ollama_service.generate_response(command)
            else:
                # 기본값으로 OpenAI 사용
                response = await self.openai_service.generate_response(command)
            
            # 응답 포맷팅
            formatted_response = self._format_ai_response(response)
            
            logger.info("명령 처리 완료")
            return formatted_response
            
        except Exception as e:
            logger.error(f"명령 처리 중 오류 발생: {str(e)}")
            return {
                "status": "error",
                "title": "처리 중 오류가 발생했습니다",
                "content": f"죄송합니다. 명령을 처리하는 동안 오류가 발생했습니다: {str(e)}",
                "type": "error"
            }
    
    def _format_ai_response(self, raw_response: str) -> Dict[str, Any]:
        """
        AI 응답 포맷팅
        """
        try:
            # JSON 응답인 경우 파싱
            response_data = json.loads(raw_response)
            return response_data
        except json.JSONDecodeError:
            # 일반 텍스트 응답인 경우 기본 포맷으로 변환
            return {
                "status": "success",
                "title": "AI 응답",
                "content": raw_response,
                "type": "general"
            }
    
    def get_command_history(self) -> List[Dict[str, Any]]:
        """
        명령 히스토리 반환
        """
        return self.command_history
    
    async def generate_website_code(self, command: str, website_type: str = "general", features: List[str] = None) -> Dict[str, str]:
        """
        웹사이트 코드 생성
        
        Args:
            command: 사용자 명령
            website_type: 웹사이트 유형 (general, landing, blog, ecommerce, portfolio)
            features: 웹사이트 기능 목록
            
        Returns:
            Dict: 생성된 웹사이트 코드 (HTML, CSS, JS, app.yaml)
        """
        try:
            logger.info(f"웹사이트 코드 생성 시작: {website_type} 유형")
            
            if features is None:
                features = ["basic_layout"]
            
            # 웹사이트 유형에 따른 템플릿 선택
            template = self.templates.get(website_type, self.templates["general"])
            
            # 템플릿을 통해 코드 생성
            website_code = await template.generate_code(command, features)
            
            # app.yaml 파일 생성
            app_yaml = self._generate_app_yaml(website_type)
            website_code["app_yaml"] = app_yaml
            
            logger.info(f"웹사이트 코드 생성 완료: {website_type} 유형")
            return website_code
            
        except Exception as e:
            logger.error(f"웹사이트 코드 생성 중 오류: {str(e)}")
            # 오류 발생 시 기본 코드 반환
            return self._generate_fallback_website_code(website_type)
    
    def _generate_app_yaml(self, website_type: str) -> str:
        """
        App Engine 배포를 위한 app.yaml 파일 생성
        """
        app_yaml = """runtime: python39
handlers:
- url: /
  static_files: index.html
  upload: index.html

- url: /(.*)
  static_files: \\1
  upload: (.*)
"""
        return app_yaml
    
    def _generate_fallback_website_code(self, website_type: str) -> Dict[str, str]:
        """
        오류 발생 시 기본 웹사이트 코드 생성
        """
        html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LimoneIDE {website_type.capitalize()} 사이트</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header>
        <h1>LimoneIDE {website_type.capitalize()} 사이트</h1>
        <p>AI로 생성된 기본 웹사이트</p>
    </header>
    
    <main>
        <section>
            <h2>환영합니다!</h2>
            <p>이 웹사이트는 LimoneIDE에서 자동 생성되었습니다.</p>
        </section>
    </main>
    
    <footer>
        <p>&copy; 2025 LimoneIDE. All rights reserved.</p>
    </footer>
    
    <script src="app.js"></script>
</body>
</html>"""

        css = """/* 기본 스타일 */
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

header {
    background-color: #4ade80;
    color: white;
    text-align: center;
    padding: 2rem 0;
}

main {
    max-width: 1200px;
    margin: 2rem auto;
    padding: 0 1rem;
}

section {
    background-color: white;
    border-radius: 8px;
    padding: 2rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

h1 {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}

h2 {
    font-size: 1.8rem;
    margin-bottom: 1rem;
    color: #333;
}

p {
    margin-bottom: 1rem;
}

footer {
    text-align: center;
    padding: 1.5rem 0;
    background-color: #333;
    color: white;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
    header {
        padding: 1.5rem 0;
    }
    
    h1 {
        font-size: 2rem;
    }
}"""

        js = """// 기본 자바스크립트 코드
document.addEventListener('DOMContentLoaded', function() {
    console.log('웹사이트가 로드되었습니다.');
    
    // 현재 시간 표시
    const now = new Date();
    const timeElement = document.createElement('div');
    timeElement.className = 'time-display';
    timeElement.textContent = `현재 시간: ${now.toLocaleTimeString()}`;
    document.querySelector('header').appendChild(timeElement);
});"""

        app_yaml = self._generate_app_yaml(website_type)

        return {
            "html": html,
            "css": css,
            "js": js,
            "app_yaml": app_yaml
        }
    
    async def generate_code(self, prompt: str, language: str = "python") -> str:
        """
        코드 생성
        
        Args:
            prompt: 코드 생성 프롬프트
            language: 프로그래밍 언어
            
        Returns:
            str: 생성된 코드
        """
        # 실제 구현에서는 AI 모델을 사용하여 코드 생성
        return f"# {prompt}\n\ndef example_function():\n    print('Hello from LimoneIDE!')\n    return True"
    
    async def get_available_models(self) -> Dict[str, List[str]]:
        """
        사용 가능한 AI 모델 목록 반환
        
        Returns:
            Dict: 제공자별 사용 가능한 모델 목록
        """
        result = {}
        
        for provider, info in self.models.items():
            if info["available"]:
                result[provider] = info["models"]
        
        return result 