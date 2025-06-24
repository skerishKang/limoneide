#!/usr/bin/env python3
"""
🍋 LimoneIDE 간단한 테스트 서버
E2E 테스트를 위한 기본 HTTP 서버
"""

import json
import time
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading

class LimoneIDETestHandler(BaseHTTPRequestHandler):
    """LimoneIDE 테스트용 HTTP 핸들러"""
    
    def __init__(self, *args, **kwargs):
        self.test_data = {
            "projects": [],
            "guestbook": [],
            "deployments": []
        }
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """GET 요청 처리"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {
                "message": "🍋 LimoneIDE Test Server",
                "status": "running",
                "timestamp": datetime.now().isoformat()
            }
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode())
            
        elif path == "/health":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "version": "1.0.0"
            }
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode())
            
        elif path == "/api/health/db":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {
                "status": "connected",
                "database": "test_sqlite",
                "timestamp": datetime.now().isoformat()
            }
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode())
            
        elif path == "/auth/google":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {
                "auth_url": "https://accounts.google.com/oauth/authorize?client_id=test&redirect_uri=http://localhost:8000/auth/google/callback",
                "status": "redirect"
            }
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode())
            
        elif path == "/auth/session":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {
                "authenticated": True,
                "user": {
                    "id": "test_user_123",
                    "email": "test@example.com"
                }
            }
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode())
            
        elif path == "/api/guestbook":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {
                "entries": self.test_data["guestbook"],
                "total": len(self.test_data["guestbook"])
            }
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode())
            
        elif path == "/api/stats":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {
                "project_count": len(self.test_data["projects"]),
                "guestbook_count": len(self.test_data["guestbook"]),
                "deployment_count": len(self.test_data["deployments"]),
                "server_uptime": "1 hour"
            }
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode())
            
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {"error": "Not found", "path": path}
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode())
    
    def do_POST(self):
        """POST 요청 처리"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # 요청 본문 읽기
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
        except:
            data = {}
        
        if path == "/api/projects":
            project_id = f"project_{len(self.test_data['projects']) + 1}"
            project_data = {
                "project_id": project_id,
                "name": data.get("name", "Test Project"),
                "description": data.get("description", "Test Description"),
                "template": data.get("template", "general"),
                "created_at": datetime.now().isoformat(),
                "status": "created"
            }
            self.test_data["projects"].append(project_data)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {
                "status": "success",
                "project_id": project_id,
                "message": "프로젝트가 성공적으로 생성되었습니다."
            }
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode())
            
        elif path == "/api/voice/process":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {
                "status": "success",
                "intent": "create_website",
                "command": data.get("command", "테스트 명령"),
                "confidence": 0.95,
                "processed_at": datetime.now().isoformat()
            }
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode())
            
        elif path == "/api/ai/generate":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {
                "status": "success",
                "files": [
                    "index.html",
                    "styles.css", 
                    "app.js",
                    "app.yaml"
                ],
                "generated_at": datetime.now().isoformat(),
                "template": data.get("template", "general")
            }
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode())
            
        elif path == "/api/deploy/start":
            deployment_id = f"deploy_{len(self.test_data['deployments']) + 1}"
            deployment_data = {
                "deployment_id": deployment_id,
                "project_id": data.get("project_id", "test-project"),
                "status": "in_progress",
                "started_at": datetime.now().isoformat()
            }
            self.test_data["deployments"].append(deployment_data)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {
                "status": "success",
                "deployment_id": deployment_id,
                "message": "배포가 시작되었습니다."
            }
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode())
            
        elif path == "/api/cloudsql/test-connection":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {
                "status": "connected",
                "instance_name": data.get("instance_name", "test-instance"),
                "database_type": data.get("database_type", "mysql"),
                "connection_test": "success"
            }
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode())
            
        elif path == "/api/templates/blog":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {
                "status": "success",
                "files": [
                    "index.html",
                    "styles.css",
                    "app.js",
                    "blog_backend.py"
                ],
                "features": data.get("features", ["blog_posts", "guestbook"]),
                "generated_at": datetime.now().isoformat()
            }
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode())
            
        elif path == "/api/guestbook":
            entry_data = {
                "id": len(self.test_data["guestbook"]) + 1,
                "name": data.get("name", "Anonymous"),
                "email": data.get("email", ""),
                "message": data.get("message", ""),
                "created_at": datetime.now().isoformat()
            }
            self.test_data["guestbook"].append(entry_data)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {
                "status": "success",
                "message": "방명록이 등록되었습니다.",
                "entry": entry_data
            }
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode())
            
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {"error": "Not found", "path": path}
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode())
    
    def do_OPTIONS(self):
        """CORS preflight 요청 처리"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def log_message(self, format, *args):
        """로그 메시지 출력"""
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {format % args}")

def run_server(port=8000):
    """서버 실행"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, LimoneIDETestHandler)
    print(f"🍋 LimoneIDE 테스트 서버 시작...")
    print(f"서버 주소: http://localhost:{port}")
    print(f"API 문서: http://localhost:{port}/health")
    print("서버를 중지하려면 Ctrl+C를 누르세요.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n서버를 종료합니다...")
        httpd.server_close()

if __name__ == "__main__":
    run_server() 