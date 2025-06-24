"""
🍋 LimoneIDE Google Integration
Google 클라우드 서비스 연동 및 App Engine 자동화
"""

from typing import Dict, Any, List, Optional
import json
import os
import time
import uuid
import aiohttp
import asyncio
import logging
from urllib.parse import urlencode
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('google_integration')

class GoogleIntegration:
    """
    LimoneIDE Google 서비스 연동
    - OAuth2.0 인증: 사용자 권한 획득
    - Cloud Resource Manager: 프로젝트 생성 및 관리
    - App Engine: 웹 애플리케이션 자동 배포
    - Cloud SQL: 데이터베이스 자동 생성 및 연결
    """
    def __init__(self, credentials: Dict[str, Any] = None):
        self.credentials = credentials or {}
        self.token_info = {}
        self.services = {
            "drive": GoogleDriveService(),
            "gmail": GmailService(),
            "calendar": CalendarService(),
            "cloud": GoogleCloudService()
        }
        
        # OAuth 설정
        self.client_id = os.environ.get("GOOGLE_CLIENT_ID", "")
        self.client_secret = os.environ.get("GOOGLE_CLIENT_SECRET", "")
        self.redirect_uri = os.environ.get("GOOGLE_REDIRECT_URI", "http://localhost:8000/auth/google/callback")
        
        # 필요한 권한 스코프
        self.scopes = [
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/cloud-platform"  # Google Cloud 리소스 관리 권한
        ]
        
        logger.info("GoogleIntegration 초기화 완료")
    
    def get_auth_url(self) -> str:
        """
        Google OAuth 인증 URL 생성
        
        Returns:
            str: 인증 URL
        """
        if not self.client_id:
            logger.error("Google Client ID가 설정되지 않았습니다.")
            raise Exception("Google Client ID가 설정되지 않았습니다.")
            
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": " ".join(self.scopes),
            "access_type": "offline",  # 리프레시 토큰 요청
            "prompt": "consent"  # 항상 동의 화면 표시
        }
        
        auth_url = f"https://accounts.google.com/o/oauth2/auth?{urlencode(params)}"
        logger.info(f"인증 URL 생성: {auth_url[:50]}...")
        return auth_url
    
    async def exchange_code_for_token(self, code: str) -> Dict[str, Any]:
        """
        인증 코드를 토큰으로 교환
        
        Args:
            code: 인증 코드
            
        Returns:
            Dict: 토큰 정보
        """
        if not self.client_id or not self.client_secret:
            logger.error("Google OAuth 인증 정보가 설정되지 않았습니다.")
            return {"status": "error", "message": "Google OAuth 인증 정보가 설정되지 않았습니다."}
            
        try:
            logger.info("인증 코드를 토큰으로 교환 시도")
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://oauth2.googleapis.com/token",
                    data={
                        "client_id": self.client_id,
                        "client_secret": self.client_secret,
                        "code": code,
                        "redirect_uri": self.redirect_uri,
                        "grant_type": "authorization_code"
                    }
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(f"토큰 교환 실패: {error_text}")
                        return {"status": "error", "message": f"토큰 교환 실패: {error_text}"}
                        
                    token_data = await response.json()
                    self.token_info = token_data
                    logger.info("토큰 교환 성공")
                    return {
                        "status": "success",
                        "access_token": token_data.get("access_token"),
                        "refresh_token": token_data.get("refresh_token"),
                        "expires_in": token_data.get("expires_in")
                    }
        except Exception as e:
            logger.error(f"토큰 교환 중 오류: {str(e)}")
            return {"status": "error", "message": f"토큰 교환 중 오류: {str(e)}"}
    
    async def get_user_info(self, access_token: str) -> Dict[str, Any]:
        """
        사용자 정보 조회
        
        Args:
            access_token: 액세스 토큰
            
        Returns:
            Dict: 사용자 정보
        """
        try:
            logger.info("사용자 정보 조회 시도")
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "https://www.googleapis.com/oauth2/v2/userinfo",
                    headers={"Authorization": f"Bearer {access_token}"}
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(f"사용자 정보 조회 실패: {error_text}")
                        return {"status": "error", "message": f"사용자 정보 조회 실패: {error_text}"}
                        
                    user_data = await response.json()
                    logger.info(f"사용자 정보 조회 성공: {user_data.get('email')}")
                    return {
                        "status": "success",
                        "user_info": {
                            "id": user_data.get("id"),
                            "email": user_data.get("email"),
                            "name": user_data.get("name"),
                            "given_name": user_data.get("given_name"),
                            "family_name": user_data.get("family_name"),
                            "picture": user_data.get("picture")
                        }
                    }
        except Exception as e:
            logger.error(f"사용자 정보 조회 중 오류: {str(e)}")
            return {"status": "error", "message": f"사용자 정보 조회 중 오류: {str(e)}"}
    
    async def create_google_cloud_project(self, access_token: str, project_name: str) -> Dict[str, Any]:
        """
        Google Cloud 프로젝트 생성
        
        Args:
            access_token: 액세스 토큰
            project_name: 프로젝트 이름
            
        Returns:
            Dict: 생성된 프로젝트 정보
        """
        try:
            # 프로젝트 ID 생성 (고유한 ID 필요)
            project_id = f"limoneide-{project_name.lower().replace(' ', '-')}-{uuid.uuid4().hex[:8]}"
            logger.info(f"Google Cloud 프로젝트 생성 시도: {project_id}")
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://cloudresourcemanager.googleapis.com/v1/projects",
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "projectId": project_id,
                        "name": project_name
                    }
                ) as response:
                    if response.status not in [200, 201]:
                        error_text = await response.text()
                        logger.error(f"프로젝트 생성 실패: {error_text}")
                        return {"status": "error", "message": f"프로젝트 생성 실패: {error_text}"}
                    
                    project_data = await response.json()
                    
                    # 프로젝트 생성은 비동기 작업이므로 완료될 때까지 대기
                    operation_name = project_data.get("name")
                    if operation_name:
                        logger.info(f"프로젝트 생성 작업 시작: {operation_name}")
                        await self._wait_for_operation(access_token, operation_name)
                    
                    logger.info(f"프로젝트 생성 성공: {project_id}")
                    return {
                        "status": "success",
                        "project_id": project_id,
                        "project_name": project_name,
                        "message": "프로젝트가 성공적으로 생성되었습니다."
                    }
        except Exception as e:
            logger.error(f"프로젝트 생성 중 오류: {str(e)}")
            return {"status": "error", "message": f"프로젝트 생성 중 오류: {str(e)}"}
    
    async def _wait_for_operation(self, access_token: str, operation_name: str, max_retries: int = 10) -> bool:
        """
        Google Cloud 작업 완료 대기
        
        Args:
            access_token: 액세스 토큰
            operation_name: 작업 이름
            max_retries: 최대 재시도 횟수
            
        Returns:
            bool: 작업 성공 여부
        """
        retries = 0
        
        while retries < max_retries:
            try:
                logger.info(f"작업 상태 확인 중: {operation_name} (시도 {retries+1}/{max_retries})")
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        f"https://cloudresourcemanager.googleapis.com/v1/{operation_name}",
                        headers={"Authorization": f"Bearer {access_token}"}
                    ) as response:
                        if response.status != 200:
                            logger.warning(f"작업 상태 확인 실패: {response.status}")
                            await asyncio.sleep(2)
                            retries += 1
                            continue
                            
                        operation_data = await response.json()
                        if operation_data.get("done", False):
                            if "error" in operation_data:
                                logger.error(f"작업 실패: {operation_data['error']}")
                                return False
                            logger.info(f"작업 성공적으로 완료: {operation_name}")
            return True
                            
                        # 작업이 완료되지 않았으면 대기 후 재시도
                        logger.info("작업이 아직 진행 중, 대기 중...")
                        await asyncio.sleep(2)
                        retries += 1
            except Exception as e:
                logger.error(f"작업 상태 확인 중 오류: {str(e)}")
                await asyncio.sleep(2)
                retries += 1
        
        logger.error(f"최대 재시도 횟수 초과: {operation_name}")
        return False
    
    async def enable_app_engine_api(self, access_token: str, project_id: str) -> Dict[str, Any]:
        """
        App Engine API 활성화
        
        Args:
            access_token: 액세스 토큰
            project_id: 프로젝트 ID
            
        Returns:
            Dict: API 활성화 결과
        """
        try:
            # App Engine Admin API 활성화
            service_name = "appengine.googleapis.com"
            logger.info(f"App Engine API 활성화 시도: {project_id}")
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"https://serviceusage.googleapis.com/v1/projects/{project_id}/services/{service_name}:enable",
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "Content-Type": "application/json"
                    }
                ) as response:
                    if response.status not in [200, 201]:
                        error_text = await response.text()
                        logger.error(f"API 활성화 실패: {error_text}")
                        return {"status": "error", "message": f"API 활성화 실패: {error_text}"}
                    
                    operation_data = await response.json()
                    
                    # API 활성화는 비동기 작업이므로 완료될 때까지 대기
                    operation_name = operation_data.get("name")
                    if operation_name:
                        logger.info(f"API 활성화 작업 시작: {operation_name}")
                        await self._wait_for_service_operation(access_token, operation_name)
                    
                    logger.info(f"App Engine API 활성화 성공: {project_id}")
                    return {
                        "status": "success",
                        "project_id": project_id,
                        "message": "App Engine API가 성공적으로 활성화되었습니다."
                    }
        except Exception as e:
            logger.error(f"API 활성화 중 오류: {str(e)}")
            return {"status": "error", "message": f"API 활성화 중 오류: {str(e)}"}
    
    async def _wait_for_service_operation(self, access_token: str, operation_name: str, max_retries: int = 10) -> bool:
        """
        Google Cloud 서비스 작업 완료 대기
        
        Args:
            access_token: 액세스 토큰
            operation_name: 작업 이름
            max_retries: 최대 재시도 횟수
            
        Returns:
            bool: 작업 성공 여부
        """
        retries = 0
        
        while retries < max_retries:
            try:
                logger.info(f"서비스 작업 상태 확인 중: {operation_name} (시도 {retries+1}/{max_retries})")
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        f"https://serviceusage.googleapis.com/v1/{operation_name}",
                        headers={"Authorization": f"Bearer {access_token}"}
                    ) as response:
                        if response.status != 200:
                            logger.warning(f"서비스 작업 상태 확인 실패: {response.status}")
                            await asyncio.sleep(2)
                            retries += 1
                            continue
                            
                        operation_data = await response.json()
                        if operation_data.get("done", False):
                            if "error" in operation_data:
                                logger.error(f"서비스 작업 실패: {operation_data['error']}")
                                return False
                            logger.info(f"서비스 작업 성공적으로 완료: {operation_name}")
                            return True
                            
                        # 작업이 완료되지 않았으면 대기 후 재시도
                        logger.info("서비스 작업이 아직 진행 중, 대기 중...")
                        await asyncio.sleep(2)
                        retries += 1
            except Exception as e:
                logger.error(f"서비스 작업 상태 확인 중 오류: {str(e)}")
                await asyncio.sleep(2)
                retries += 1
        
        logger.error(f"서비스 작업 최대 재시도 횟수 초과: {operation_name}")
            return False

    async def create_app_engine_app(self, access_token: str, project_id: str, location_id: str = "us-central") -> Dict[str, Any]:
        """
        App Engine 애플리케이션 생성
        
        Args:
            access_token: 액세스 토큰
            project_id: 프로젝트 ID
            location_id: 리전 ID (기본값: us-central)
            
        Returns:
            Dict: App Engine 앱 생성 결과
        """
        try:
            logger.info(f"App Engine 애플리케이션 생성 시도: {project_id} (리전: {location_id})")
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"https://appengine.googleapis.com/v1/apps",
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "id": project_id,
                        "locationId": location_id
                    }
                ) as response:
                    if response.status not in [200, 201, 202]:
                        error_text = await response.text()
                        logger.error(f"App Engine 앱 생성 실패: {error_text}")
                        return {"status": "error", "message": f"App Engine 앱 생성 실패: {error_text}"}
                    
                    app_data = await response.json()
                    
                    # App Engine 앱 생성은 비동기 작업이므로 완료될 때까지 대기
                    operation_name = app_data.get("name")
                    if operation_name:
                        logger.info(f"App Engine 앱 생성 작업 시작: {operation_name}")
                        await self._wait_for_service_operation(access_token, operation_name)
                    
                    logger.info(f"App Engine 앱 생성 성공: {project_id}")
                    return {
                        "status": "success",
                        "project_id": project_id,
                        "location_id": location_id,
                        "message": "App Engine 애플리케이션이 성공적으로 생성되었습니다."
                    }
        except Exception as e:
            logger.error(f"App Engine 앱 생성 중 오류: {str(e)}")
            return {"status": "error", "message": f"App Engine 앱 생성 중 오류: {str(e)}"}
    
    async def deploy_app_engine_app(self, access_token: str, project_id: str, source_code: Dict[str, Any]) -> Dict[str, Any]:
        """
        App Engine에 애플리케이션 배포
        
        Args:
            access_token: 액세스 토큰
            project_id: 프로젝트 ID
            source_code: 소스 코드 정보
            
        Returns:
            Dict: 배포 결과
        """
        # 이 메서드는 Sprint 2에서 구현할 예정
        logger.info("App Engine 배포 기능은 Sprint 2에서 구현 예정")
        return {
            "status": "success",
            "message": "App Engine 배포 기능은 Sprint 2에서 구현 예정입니다."
        }
    
    async def save_conversation(self, command: str, response: str) -> Dict[str, Any]:
        """
        대화 내용 저장
        
        Args:
            command: 사용자 명령
            response: AI 응답
            
        Returns:
            Dict: 저장 결과
        """
        try:
            # 실제 구현에서는 Google Drive 또는 Firestore에 저장
            logger.info(f"대화 내용 저장: {command[:30]}...")
            return {"status": "success", "message": "대화 내용이 저장되었습니다."}
        except Exception as e:
            logger.error(f"대화 내용 저장 중 오류: {str(e)}")
            return {"status": "error", "message": f"대화 내용 저장 중 오류: {str(e)}"}

    async def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        """
        리프레시 토큰을 사용하여 액세스 토큰 갱신
        
        Args:
            refresh_token: 리프레시 토큰
            
        Returns:
            Dict: 갱신된 토큰 정보
        """
        try:
            logger.info("액세스 토큰 갱신 시도")
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://oauth2.googleapis.com/token",
                    data={
                        "client_id": self.client_id,
                        "client_secret": self.client_secret,
                        "refresh_token": refresh_token,
                        "grant_type": "refresh_token"
                    }
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(f"토큰 갱신 실패: {error_text}")
                        return {"status": "error", "message": f"토큰 갱신 실패: {error_text}"}
                        
                    token_data = await response.json()
                    logger.info("토큰 갱신 성공")
                    return {
                        "status": "success",
                        "access_token": token_data.get("access_token"),
                        "expires_in": token_data.get("expires_in")
                    }
        except Exception as e:
            logger.error(f"토큰 갱신 중 오류: {str(e)}")
            return {"status": "error", "message": f"토큰 갱신 중 오류: {str(e)}"}

# 서비스 클래스들 - 프로토타입 구현
class GoogleDriveService:
    """Google Drive 서비스"""
    
    def __init__(self):
        pass
    
    async def upload_file(self, content: str, filename: str) -> Dict[str, Any]:
        # 프로토타입
        return {"status": "success", "message": "파일이 업로드되었습니다."}

class GmailService:
    """Gmail 서비스"""
    
    def __init__(self):
        pass
    
    async def send_email(self, to: str, subject: str, body: str) -> Dict[str, Any]:
        # 프로토타입
        return {"status": "success", "message": "이메일이 전송되었습니다."}

class CalendarService:
    """Google Calendar 서비스"""
    
    def __init__(self):
        pass
    
    async def create_event(self, summary: str, start_time: str, end_time: str) -> Dict[str, Any]:
        # 프로토타입
        return {"status": "success", "message": "일정이 생성되었습니다."}

class GoogleCloudService:
    """Google Cloud 서비스"""
    
    def __init__(self):
        pass
    
    async def list_projects(self, access_token: str) -> Dict[str, Any]:
        # 프로토타입
        return {"status": "success", "projects": []} 