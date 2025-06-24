"""
🍋 LimoneIDE Backend
AI 기반 음성 자동화 플랫폼 백엔드
"""

import os
import json
import asyncio
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, Request, HTTPException, Depends, Header, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv

from src.core.ai_engine import AIEngine
from src.automation.google_integration import GoogleIntegration
from src.automation.deployment_manager import DeploymentManager
from src.voice.intent_analyzer import IntentAnalyzer

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('limoneide_backend')

# 환경 변수 로드
load_dotenv()

# FastAPI 앱 생성
app = FastAPI(
    title="LimoneIDE Backend",
    description="AI 기반 음성 자동화 플랫폼 백엔드 API",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 배포 시에는 특정 도메인으로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 서비스 인스턴스 초기화
ai_engine = AIEngine()
google_integration = GoogleIntegration()
deployment_manager = DeploymentManager()
intent_analyzer = IntentAnalyzer()

# 요청 모델 정의
class VoiceCommandRequest(BaseModel):
    command: str
    timestamp: Optional[str] = None
    user_agent: Optional[str] = None
    access_token: Optional[str] = None

class AuthCodeRequest(BaseModel):
    code: str

class ProjectRequest(BaseModel):
    project_name: str

class AppEngineRequest(BaseModel):
    project_id: str
    location_id: str = "us-central"

# 헬스 체크 엔드포인트
@app.get("/health-check")
async def health_check():
    logger.info("헬스 체크 요청 처리")
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

# Google OAuth 인증 URL 제공 엔드포인트
@app.get("/auth/google/url")
async def get_google_auth_url():
    try:
        logger.info("Google 인증 URL 요청 처리")
        auth_url = google_integration.get_auth_url()
        return {"status": "success", "auth_url": auth_url}
    except Exception as e:
        logger.error(f"인증 URL 생성 실패: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"인증 URL 생성 실패: {str(e)}"}
        )

# Google OAuth 콜백 처리 엔드포인트
@app.post("/auth/google/callback")
async def google_auth_callback(request: AuthCodeRequest):
    try:
        logger.info("Google 인증 콜백 처리")
        # 인증 코드로 토큰 교환
        token_result = await google_integration.exchange_code_for_token(request.code)
        
        if token_result["status"] == "error":
            logger.error(f"토큰 교환 실패: {token_result['message']}")
            return JSONResponse(
                status_code=400,
                content={"status": "error", "message": token_result["message"]}
            )
        
        # 사용자 정보 가져오기
        user_info_result = await google_integration.get_user_info(token_result["access_token"])
        
        if user_info_result["status"] == "error":
            logger.error(f"사용자 정보 조회 실패: {user_info_result['message']}")
            return JSONResponse(
                status_code=400,
                content={"status": "error", "message": user_info_result["message"]}
            )
        
        logger.info(f"인증 성공: {user_info_result['user_info'].get('email')}")
        return {
            "status": "success",
            "access_token": token_result["access_token"],
            "refresh_token": token_result.get("refresh_token"),
            "expires_in": token_result.get("expires_in"),
            "user_info": user_info_result["user_info"]
        }
    except Exception as e:
        logger.error(f"인증 콜백 처리 실패: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"인증 콜백 처리 실패: {str(e)}"}
        )

# 액세스 토큰 갱신 엔드포인트
@app.post("/auth/refresh-token")
async def refresh_token(refresh_token: str = Body(..., embed=True)):
    try:
        logger.info("토큰 갱신 요청 처리")
        result = await google_integration.refresh_token(refresh_token)
        
        if result["status"] == "error":
            logger.error(f"토큰 갱신 실패: {result['message']}")
            return JSONResponse(
                status_code=400,
                content={"status": "error", "message": result["message"]}
            )
        
        logger.info("토큰 갱신 성공")
        return {
            "status": "success",
            "access_token": result["access_token"],
            "expires_in": result["expires_in"]
        }
    except Exception as e:
        logger.error(f"토큰 갱신 처리 실패: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"토큰 갱신 처리 실패: {str(e)}"}
        )

# 인증 확인 미들웨어
async def verify_token(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        logger.warning("인증 토큰 없음")
        raise HTTPException(
            status_code=401,
            detail="인증 토큰이 필요합니다."
        )
    
    token = authorization.replace("Bearer ", "")
    return token

# 프로젝트 생성 엔드포인트
@app.post("/projects")
async def create_project(
    project_request: ProjectRequest,
    token: str = Depends(verify_token)
):
    try:
        logger.info(f"프로젝트 생성 요청: {project_request.project_name}")
        
        # Google Cloud 프로젝트 생성
        project_result = await google_integration.create_google_cloud_project(token, project_request.project_name)
        
        if project_result["status"] == "error":
            logger.error(f"프로젝트 생성 실패: {project_result['message']}")
            return JSONResponse(
                status_code=400,
                content={"status": "error", "message": project_result["message"]}
            )
        
        # App Engine API 활성화
        api_result = await google_integration.enable_app_engine_api(token, project_result["project_id"])
        
        if api_result["status"] == "error":
            logger.warning(f"App Engine API 활성화 실패: {api_result['message']}")
            # API 활성화 실패해도 프로젝트는 생성되었으므로 경고만 추가
            return {
                "status": "success",
                "project_id": project_result["project_id"],
                "project_name": project_result["project_name"],
                "message": "프로젝트가 생성되었으나 App Engine API 활성화에 실패했습니다.",
                "warning": api_result["message"]
            }
        
        logger.info(f"프로젝트 생성 성공: {project_result['project_id']}")
        return {
            "status": "success",
            "project_id": project_result["project_id"],
            "project_name": project_result["project_name"],
            "message": "프로젝트가 성공적으로 생성되었습니다."
        }
    except Exception as e:
        logger.error(f"프로젝트 생성 처리 실패: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"프로젝트 생성 처리 실패: {str(e)}"}
        )

# App Engine 애플리케이션 생성 엔드포인트
@app.post("/app-engine")
async def create_app_engine(
    app_request: AppEngineRequest,
    token: str = Depends(verify_token)
):
    try:
        logger.info(f"App Engine 애플리케이션 생성 요청: {app_request.project_id} (리전: {app_request.location_id})")
        
        # App Engine 애플리케이션 생성
        result = await google_integration.create_app_engine_app(token, app_request.project_id, app_request.location_id)
        
        if result["status"] == "error":
            logger.error(f"App Engine 애플리케이션 생성 실패: {result['message']}")
            return JSONResponse(
                status_code=400,
                content={"status": "error", "message": result["message"]}
            )
        
        logger.info(f"App Engine 애플리케이션 생성 성공: {app_request.project_id}")
        return {
            "status": "success",
            "project_id": result["project_id"],
            "location_id": result["location_id"],
            "message": "App Engine 애플리케이션이 성공적으로 생성되었습니다.",
            "app_url": f"https://{app_request.project_id}.appspot.com"
        }
    except Exception as e:
        logger.error(f"App Engine 애플리케이션 생성 처리 실패: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"App Engine 애플리케이션 생성 처리 실패: {str(e)}"}
        )

# 음성 명령 처리 엔드포인트
@app.post("/voice-command")
async def process_voice_command(request: VoiceCommandRequest):
    try:
        logger.info(f"음성 명령 처리: {request.command[:30]}...")
        
        # 의도 분석
        intent = intent_analyzer.analyze(request.command)
        logger.info(f"의도 분석 결과: {intent['type']}")
        
        # 웹사이트 생성 의도인 경우 배포 파이프라인 실행
        if intent['type'] == "website_creation":
            # 1. AI 엔진을 통해 웹사이트 코드 생성
            logger.info("AI 엔진을 통해 웹사이트 코드 생성 중...")
            website_type = intent.get("website_type", "general")
            features = intent.get("features", ["basic_layout"])
            
            # 웹사이트 코드 생성 (실제 구현에서는 AI 모델 사용)
            website_code = await ai_engine.generate_website_code(request.command, website_type, features)
            
            # 2. 액세스 토큰이 있는 경우 App Engine 배포 실행
            if request.access_token:
                logger.info("App Engine 배포 시작...")
                
                # 2-1. 프로젝트 생성
                project_name = f"limoneide-{website_type}-site"
                project_result = await google_integration.create_google_cloud_project(
                    request.access_token, 
                    project_name
                )
                
                if project_result["status"] == "error":
                    logger.error(f"프로젝트 생성 실패: {project_result['message']}")
                    return {
                        "status": "partial_success",
                        "title": "웹사이트 코드 생성 완료",
                        "content": f"{website_type.capitalize()} 유형의 웹사이트 코드가 생성되었으나, 배포에 실패했습니다.",
                        "type": "website",
                        "error": project_result["message"],
                        "steps": [
                            "✅ 웹사이트 요구사항 분석 완료",
                            "✅ 디자인 템플릿 선택 완료",
                            "✅ 코드 생성 완료",
                            "❌ 프로젝트 생성 실패"
                        ],
                        "speak": "웹사이트 코드가 생성되었으나, 배포에 실패했습니다."
                    }
                
                # 2-2. App Engine API 활성화
                project_id = project_result["project_id"]
                logger.info(f"App Engine API 활성화 중: {project_id}")
                
                api_result = await google_integration.enable_app_engine_api(
                    request.access_token, 
                    project_id
                )
                
                if api_result["status"] == "error":
                    logger.error(f"App Engine API 활성화 실패: {api_result['message']}")
                    return {
                        "status": "partial_success",
                        "title": "웹사이트 코드 생성 및 프로젝트 생성 완료",
                        "content": f"{website_type.capitalize()} 유형의 웹사이트 코드가 생성되었으나, App Engine API 활성화에 실패했습니다.",
                        "type": "website",
                        "error": api_result["message"],
                        "project_id": project_id,
                        "steps": [
                            "✅ 웹사이트 요구사항 분석 완료",
                            "✅ 디자인 템플릿 선택 완료",
                            "✅ 코드 생성 완료",
                            "✅ 프로젝트 생성 완료",
                            "❌ App Engine API 활성화 실패"
                        ],
                        "speak": "웹사이트 코드와 프로젝트가 생성되었으나, App Engine API 활성화에 실패했습니다."
                    }
                
                # 2-3. App Engine 애플리케이션 생성
                logger.info(f"App Engine 애플리케이션 생성 중: {project_id}")
                
                app_result = await google_integration.create_app_engine_app(
                    request.access_token, 
                    project_id
                )
                
                if app_result["status"] == "error":
                    logger.error(f"App Engine 애플리케이션 생성 실패: {app_result['message']}")
                    return {
                        "status": "partial_success",
                        "title": "웹사이트 코드 생성 및 프로젝트 설정 완료",
                        "content": f"{website_type.capitalize()} 유형의 웹사이트 코드가 생성되었으나, App Engine 애플리케이션 생성에 실패했습니다.",
                        "type": "website",
                        "error": app_result["message"],
                        "project_id": project_id,
                        "steps": [
                            "✅ 웹사이트 요구사항 분석 완료",
                            "✅ 디자인 템플릿 선택 완료",
                            "✅ 코드 생성 완료",
                            "✅ 프로젝트 생성 완료",
                            "✅ App Engine API 활성화 완료",
                            "❌ App Engine 애플리케이션 생성 실패"
                        ],
                        "speak": "웹사이트 코드와 프로젝트 설정이 완료되었으나, App Engine 애플리케이션 생성에 실패했습니다."
                    }
                
                # 2-4. App Engine 배포
                logger.info(f"App Engine 배포 중: {project_id}")
                
                # 웹사이트 코드를 파일 구조로 변환
                source_code = {
                    "index.html": website_code["html"],
                    "styles.css": website_code["css"],
                    "app.js": website_code["js"],
                    "app.yaml": website_code["app_yaml"]
                }
                
                deploy_result = await deployment_manager.deploy_app_engine_app(
                    request.access_token,
                    project_id,
                    source_code
                )
                
                if deploy_result["status"] == "error":
                    logger.error(f"App Engine 배포 실패: {deploy_result['message']}")
                    return {
                        "status": "partial_success",
                        "title": "웹사이트 코드 생성 및 App Engine 설정 완료",
                        "content": f"{website_type.capitalize()} 유형의 웹사이트 코드가 생성되었으나, 배포에 실패했습니다.",
                        "type": "website",
                        "error": deploy_result["message"],
                        "project_id": project_id,
                        "steps": [
                            "✅ 웹사이트 요구사항 분석 완료",
                            "✅ 디자인 템플릿 선택 완료",
                            "✅ 코드 생성 완료",
                            "✅ 프로젝트 생성 완료",
                            "✅ App Engine API 활성화 완료",
                            "✅ App Engine 애플리케이션 생성 완료",
                            "❌ 배포 실패"
                        ],
                        "speak": "웹사이트 코드와 App Engine 설정이 완료되었으나, 배포에 실패했습니다."
                    }
                
                # 2-5. 배포 성공
                logger.info(f"App Engine 배포 성공: {deploy_result['app_url']}")
                return {
                    "status": "success",
                    "title": "웹사이트 생성 및 배포 완료",
                    "content": f"{website_type.capitalize()} 유형의 웹사이트가 성공적으로 생성되고 배포되었습니다.",
                    "type": "website",
                    "url": deploy_result["app_url"],
                    "project_id": project_id,
                    "steps": [
                        "✅ 웹사이트 요구사항 분석 완료",
                        "✅ 디자인 템플릿 선택 완료",
                        "✅ 코드 생성 완료",
                        "✅ 프로젝트 생성 완료",
                        "✅ App Engine API 활성화 완료",
                        "✅ App Engine 애플리케이션 생성 완료",
                        "✅ 배포 완료"
                    ],
                    "speak": f"웹사이트가 성공적으로 생성되고 배포되었습니다. {deploy_result['app_url']}에서 확인하실 수 있습니다."
                }
            else:
                # 액세스 토큰이 없는 경우 코드만 생성
                logger.info("액세스 토큰이 없어 코드만 생성")
                return {
                    "status": "success",
                    "title": "웹사이트 코드 생성 완료",
                    "content": f"{website_type.capitalize()} 유형의 웹사이트 코드가 생성되었습니다.",
                    "type": "website",
                    "steps": [
                        "✅ 웹사이트 요구사항 분석 완료",
                        "✅ 디자인 템플릿 선택 완료",
                        "✅ 코드 생성 완료"
                    ],
                    "speak": "웹사이트 코드가 생성되었습니다."
                }
        else:
            # 다른 의도의 경우 기존 로직 사용
            logger.info(f"일반 명령 처리: {intent['type']}")
            ai_response = await ai_engine.process_command(request.command)
            
            # 대화 내용 저장 (비동기)
            asyncio.create_task(google_integration.save_conversation(
                request.command, 
                json.dumps(ai_response, ensure_ascii=False)
            ))
            
            return ai_response
            
    except Exception as e:
        logger.error(f"명령 처리 실패: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"명령 처리 실패: {str(e)}"}
        )

# 메인 실행 함수
if __name__ == "__main__":
    import uvicorn
    logger.info("LimoneIDE 백엔드 서버 시작")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)