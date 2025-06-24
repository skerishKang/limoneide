#!/usr/bin/env python3
"""
🍋 LimoneIDE 테스트용 서버
E2E 테스트를 위한 간단한 FastAPI 서버
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List
import uvicorn
import json
from datetime import datetime

app = FastAPI(title="LimoneIDE Test Server", version="1.0.0")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 데이터 모델
class ProjectCreate(BaseModel):
    name: str
    description: str
    template: str = "general"

class VoiceCommand(BaseModel):
    command: str
    language: str = "ko"
    project_id: str = "test-project"

class AIGenerate(BaseModel):
    command: str
    template: str = "general"
    features: List[str] = ["responsive"]
    project_id: str = "test-project"

class DeployRequest(BaseModel):
    project_id: str
    template: str = "general"
    deployment_type: str = "app_engine"

class CloudSQLRequest(BaseModel):
    project_id: str
    instance_name: str
    database_type: str = "mysql"

class BlogTemplateRequest(BaseModel):
    command: str
    features: List[str] = ["blog_posts", "guestbook"]

# 테스트 데이터
test_projects = []
test_guestbook = []
test_deployments = []

@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {"message": "🍋 LimoneIDE Test Server", "status": "running"}

@app.get("/health")
async def health_check():
    """헬스 체크"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

@app.get("/api/health/db")
async def database_health():
    """데이터베이스 헬스 체크"""
    return {
        "status": "connected",
        "database": "test_sqlite",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/auth/google")
async def google_auth():
    """Google OAuth 엔드포인트"""
    return {
        "auth_url": "https://accounts.google.com/oauth/authorize?client_id=test&redirect_uri=http://localhost:8000/auth/google/callback",
        "status": "redirect"
    }

@app.get("/auth/google/callback")
async def google_auth_callback():
    """Google OAuth 콜백"""
    return {
        "status": "success",
        "user": {
            "id": "test_user_123",
            "email": "test@example.com",
            "name": "Test User"
        }
    }

@app.get("/auth/session")
async def session_check():
    """세션 확인"""
    return {
        "authenticated": True,
        "user": {
            "id": "test_user_123",
            "email": "test@example.com"
        }
    }

@app.post("/api/projects")
async def create_project(project: ProjectCreate):
    """프로젝트 생성"""
    project_id = f"project_{len(test_projects) + 1}"
    project_data = {
        "project_id": project_id,
        "name": project.name,
        "description": project.description,
        "template": project.template,
        "created_at": datetime.now().isoformat(),
        "status": "created"
    }
    test_projects.append(project_data)
    
    return {
        "status": "success",
        "project_id": project_id,
        "message": "프로젝트가 성공적으로 생성되었습니다."
    }

@app.post("/api/voice/process")
async def process_voice_command(voice: VoiceCommand):
    """음성 명령 처리"""
    return {
        "status": "success",
        "intent": "create_website",
        "command": voice.command,
        "confidence": 0.95,
        "processed_at": datetime.now().isoformat()
    }

@app.post("/api/ai/generate")
async def generate_ai_code(ai_request: AIGenerate):
    """AI 코드 생성"""
    return {
        "status": "success",
        "files": [
            "index.html",
            "styles.css", 
            "app.js",
            "app.yaml"
        ],
        "generated_at": datetime.now().isoformat(),
        "template": ai_request.template
    }

@app.post("/api/deploy/start")
async def start_deployment(deploy: DeployRequest):
    """배포 시작"""
    deployment_id = f"deploy_{len(test_deployments) + 1}"
    deployment_data = {
        "deployment_id": deployment_id,
        "project_id": deploy.project_id,
        "status": "in_progress",
        "started_at": datetime.now().isoformat()
    }
    test_deployments.append(deployment_data)
    
    return {
        "status": "success",
        "deployment_id": deployment_id,
        "message": "배포가 시작되었습니다."
    }

@app.post("/api/cloudsql/test-connection")
async def test_cloudsql_connection(cloudsql: CloudSQLRequest):
    """Cloud SQL 연결 테스트"""
    return {
        "status": "connected",
        "instance_name": cloudsql.instance_name,
        "database_type": cloudsql.database_type,
        "connection_test": "success"
    }

@app.post("/api/templates/blog")
async def generate_blog_template(blog: BlogTemplateRequest):
    """블로그 템플릿 생성"""
    return {
        "status": "success",
        "files": [
            "index.html",
            "styles.css",
            "app.js",
            "blog_backend.py"
        ],
        "features": blog.features,
        "generated_at": datetime.now().isoformat()
    }

@app.get("/api/guestbook")
async def get_guestbook():
    """방명록 목록 조회"""
    return {
        "entries": test_guestbook,
        "total": len(test_guestbook)
    }

@app.post("/api/guestbook")
async def create_guestbook_entry(entry: Dict[str, Any]):
    """방명록 작성"""
    entry_data = {
        "id": len(test_guestbook) + 1,
        "name": entry.get("name", "Anonymous"),
        "email": entry.get("email", ""),
        "message": entry.get("message", ""),
        "created_at": datetime.now().isoformat()
    }
    test_guestbook.append(entry_data)
    
    return {
        "status": "success",
        "message": "방명록이 등록되었습니다.",
        "entry": entry_data
    }

@app.get("/api/stats")
async def get_stats():
    """통계 정보"""
    return {
        "project_count": len(test_projects),
        "guestbook_count": len(test_guestbook),
        "deployment_count": len(test_deployments),
        "server_uptime": "1 hour"
    }

if __name__ == "__main__":
    print("🍋 LimoneIDE 테스트 서버 시작...")
    print("서버 주소: http://localhost:8000")
    print("API 문서: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000) 