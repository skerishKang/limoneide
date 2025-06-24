"""
🍋 LimoneIDE Deployment Manager
Google App Engine 자동 배포 시스템
"""

import os
import asyncio
import logging
import tempfile
import zipfile
import shutil
import uuid
import aiohttp
import time
from typing import Dict, Any, Optional, List
from .google_integration import GoogleIntegration

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('deployment_manager')

class DeploymentManager:
    """
    LimoneIDE 배포 관리자
    - App Engine 자동 배포
    - 도메인 연결
    - SSL 인증서 자동 설정
    """
    
    def __init__(self):
        self.google_integration = GoogleIntegration()
        self.deployment_history = []

    def get_deployment_history(self) -> list:
        """
        배포 히스토리 반환
        """
        return self.deployment_history

    async def deploy_app_engine_app(self, access_token: str, project_id: str, source_code: Dict[str, Any]) -> Dict[str, Any]:
        """
        App Engine에 애플리케이션 배포
        
        Args:
            access_token: Google OAuth 액세스 토큰
            project_id: Google Cloud 프로젝트 ID
            source_code: 배포할 소스 코드 (HTML, CSS, JS 등)
            
        Returns:
            Dict: 배포 결과
        """
        try:
            logger.info(f"App Engine 배포 시작: {project_id}")
            
            # 1. 소스 코드 준비
            temp_dir = await self._prepare_source_code(source_code)
            if not temp_dir:
                return {
                    "status": "error",
                    "message": "소스 코드 준비 중 오류가 발생했습니다."
                }
            
            # 2. 소스 코드 압축
            zip_path = await self._zip_source_code(temp_dir, project_id)
            if not zip_path:
                self._cleanup_temp_files(temp_dir, None)
                return {
                    "status": "error",
                    "message": "소스 코드 압축 중 오류가 발생했습니다."
                }
            
            # 3. Cloud Storage에 업로드
            storage_result = await self._upload_to_storage(access_token, project_id, zip_path)
            if storage_result["status"] != "success":
                self._cleanup_temp_files(temp_dir, zip_path)
                return storage_result
            
            # 4. App Engine에 배포
            deployment_result = await self._deploy_to_app_engine(
                access_token, 
                project_id, 
                storage_result["storage_url"]
            )
            
            # 5. 임시 파일 정리
            self._cleanup_temp_files(temp_dir, zip_path)
            
            if deployment_result["status"] == "success":
                # 배포 정보 저장
                deployment_info = {
                    "project_id": project_id,
                    "app_url": deployment_result["app_url"],
                    "deployment_time": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "status": "success",
                    "source_code": source_code
                }
                self.deployment_history.append(deployment_info)
                
                logger.info(f"App Engine 배포 성공: {deployment_result['app_url']}")
            
            return deployment_result
            
        except Exception as e:
            logger.error(f"App Engine 배포 중 오류: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "message": "App Engine 배포 중 오류가 발생했습니다."
            }

    async def _prepare_source_code(self, source_code: Dict[str, Any]) -> str:
        """
        소스 코드를 임시 디렉토리에 준비
        
        Args:
            source_code: 소스 코드 딕셔너리
            
        Returns:
            str: 임시 디렉토리 경로
        """
        try:
            # 임시 디렉토리 생성
            temp_dir = tempfile.mkdtemp(prefix="limoneide_deploy_")
            logger.info(f"임시 디렉토리 생성: {temp_dir}")
            
            # app.yaml 파일 생성 (App Engine 설정)
            app_yaml_content = """runtime: python39
entrypoint: python main.py

handlers:
- url: /static
  static_dir: static
- url: /.*
  script: auto
"""
            
            with open(os.path.join(temp_dir, "app.yaml"), "w", encoding="utf-8") as f:
                f.write(app_yaml_content)
            
            # main.py 파일 생성 (Flask 앱)
            main_py_content = """from flask import Flask, render_template_string, send_from_directory
import os

app = Flask(__name__)

# HTML 템플릿
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>{{ css }}</style>
</head>
<body>
    {{ html }}
    <script>{{ js }}</script>
</body>
</html>'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE,
        title="LimoneIDE Generated Site",
        html="""",
        css="""",
        js=""""
    )

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
"""
            
            with open(os.path.join(temp_dir, "main.py"), "w", encoding="utf-8") as f:
                f.write(main_py_content)
            
            # requirements.txt 파일 생성
            requirements_content = """Flask==2.3.3
gunicorn==21.2.0
"""
            
            with open(os.path.join(temp_dir, "requirements.txt"), "w", encoding="utf-8") as f:
                f.write(requirements_content)
            
            # static 디렉토리 생성
            static_dir = os.path.join(temp_dir, "static")
            os.makedirs(static_dir, exist_ok=True)
            
            # 소스 코드 파일들 생성
            if "html" in source_code:
                with open(os.path.join(static_dir, "index.html"), "w", encoding="utf-8") as f:
                    f.write(source_code["html"])
            
            if "css" in source_code:
                with open(os.path.join(static_dir, "style.css"), "w", encoding="utf-8") as f:
                    f.write(source_code["css"])
            
            if "js" in source_code:
                with open(os.path.join(static_dir, "script.js"), "w", encoding="utf-8") as f:
                    f.write(source_code["js"])
            
            logger.info("소스 코드 준비 완료")
            return temp_dir
            
        except Exception as e:
            logger.error(f"소스 코드 준비 중 오류: {str(e)}")
            return None

    async def _zip_source_code(self, source_dir: str, project_id: str) -> str:
        """
        소스 코드를 ZIP 파일로 압축
        
        Args:
            source_dir: 소스 코드 디렉토리
            project_id: 프로젝트 ID
            
        Returns:
            str: ZIP 파일 경로
        """
        try:
            zip_path = os.path.join(tempfile.gettempdir(), f"limoneide_{project_id}_{uuid.uuid4().hex[:8]}.zip")
            
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(source_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, source_dir)
                        zipf.write(file_path, arcname)
            
            logger.info(f"소스 코드 압축 완료: {zip_path}")
            return zip_path
            
        except Exception as e:
            logger.error(f"소스 코드 압축 중 오류: {str(e)}")
            return None

    async def _upload_to_storage(self, access_token: str, project_id: str, zip_path: str) -> Dict[str, Any]:
        """
        ZIP 파일을 Cloud Storage에 업로드
        
        Args:
            access_token: 액세스 토큰
            project_id: 프로젝트 ID
            zip_path: ZIP 파일 경로
            
        Returns:
            Dict: 업로드 결과
        """
        try:
            # Cloud Storage 버킷 이름 생성
            bucket_name = f"limoneide-deploy-{project_id}"
            
            # 1. Cloud Storage API 활성화
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"https://storage.googleapis.com/storage/v1/b",
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "name": bucket_name,
                        "location": "US"
                    }
                ) as response:
                    if response.status not in [200, 201, 409]:  # 409는 이미 존재하는 경우
                        error_text = await response.text()
                        logger.warning(f"버킷 생성 실패 (무시): {error_text}")
            
            # 2. 파일 업로드
            object_name = f"source-{uuid.uuid4().hex[:8]}.zip"
            
            with open(zip_path, 'rb') as f:
                file_content = f.read()
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"https://storage.googleapis.com/upload/storage/v1/b/{bucket_name}/o",
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "Content-Type": "application/zip"
                    },
                    params={"name": object_name},
                    data=file_content
                ) as response:
                    if response.status not in [200, 201]:
                        error_text = await response.text()
                        logger.error(f"파일 업로드 실패: {error_text}")
                        return {
                            "status": "error",
                            "message": f"파일 업로드 실패: {error_text}"
                        }
                    
                    upload_data = await response.json()
                    storage_url = f"gs://{bucket_name}/{object_name}"
                    
                    logger.info(f"파일 업로드 성공: {storage_url}")
                    return {
                        "status": "success",
                        "storage_url": storage_url,
                        "bucket_name": bucket_name,
                        "object_name": object_name
                    }
                    
        except Exception as e:
            logger.error(f"Storage 업로드 중 오류: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "message": "Storage 업로드 중 오류가 발생했습니다."
            }

    async def _deploy_to_app_engine(self, access_token: str, project_id: str, storage_url: str) -> Dict[str, Any]:
        """
        App Engine에 애플리케이션 배포
        
        Args:
            access_token: 액세스 토큰
            project_id: 프로젝트 ID
            storage_url: Storage URL
            
        Returns:
            Dict: 배포 결과
        """
        try:
            # App Engine Admin API를 통한 배포
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"https://appengine.googleapis.com/v1/apps/{project_id}/versions",
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "id": f"v1-{uuid.uuid4().hex[:8]}",
                        "sourceUrl": storage_url,
                        "runtime": "python39"
                    }
                ) as response:
                    if response.status not in [200, 201]:
                        error_text = await response.text()
                        logger.error(f"App Engine 배포 실패: {error_text}")
                        return {
                            "status": "error",
                            "message": f"App Engine 배포 실패: {error_text}"
                        }
                    
                    deployment_data = await response.json()
                    operation_name = deployment_data.get("name")
                    
                    # 배포 완료 대기
                    if operation_name:
                        success = await self._wait_for_deployment(access_token, operation_name)
                        if success:
                            app_url = f"https://{project_id}.appspot.com"
                            logger.info(f"App Engine 배포 성공: {app_url}")
                            return {
                                "status": "success",
                                "app_url": app_url,
                                "project_id": project_id,
                                "message": f"애플리케이션이 성공적으로 배포되었습니다: {app_url}"
                            }
                        else:
                            return {
                                "status": "error",
                                "message": "배포 작업이 실패했습니다."
                            }
                    else:
                        return {
                            "status": "error",
                            "message": "배포 작업 이름을 받지 못했습니다."
                        }
                        
        except Exception as e:
            logger.error(f"App Engine 배포 중 오류: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "message": "App Engine 배포 중 오류가 발생했습니다."
            }

    async def _wait_for_deployment(self, access_token: str, operation_name: str, max_retries: int = 20) -> bool:
        """
        배포 작업 완료 대기
        
        Args:
            access_token: 액세스 토큰
            operation_name: 작업 이름
            max_retries: 최대 재시도 횟수
            
        Returns:
            bool: 성공 여부
        """
        try:
            for i in range(max_retries):
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        f"https://appengine.googleapis.com/v1/{operation_name}",
                        headers={"Authorization": f"Bearer {access_token}"}
                    ) as response:
                        if response.status == 200:
                            operation_data = await response.json()
                            done = operation_data.get("done", False)
                            
                            if done:
                                error = operation_data.get("error")
                                if error:
                                    logger.error(f"배포 작업 실패: {error}")
                                    return False
                                else:
                                    logger.info("배포 작업 완료")
                                    return True
                        
                # 10초 대기 후 재시도
                await asyncio.sleep(10)
                logger.info(f"배포 작업 대기 중... ({i+1}/{max_retries})")
            
            logger.error("배포 작업 시간 초과")
            return False
            
        except Exception as e:
            logger.error(f"배포 작업 대기 중 오류: {str(e)}")
            return False

    def _cleanup_temp_files(self, temp_dir: str, zip_path: str) -> None:
        """
        임시 파일 정리
        
        Args:
            temp_dir: 임시 디렉토리
            zip_path: ZIP 파일 경로
        """
        try:
            if temp_dir and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
                logger.info(f"임시 디렉토리 삭제: {temp_dir}")
            
            if zip_path and os.path.exists(zip_path):
                os.remove(zip_path)
                logger.info(f"ZIP 파일 삭제: {zip_path}")
                
        except Exception as e:
            logger.warning(f"임시 파일 정리 중 오류: {str(e)}") 