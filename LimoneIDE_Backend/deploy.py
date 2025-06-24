#!/usr/bin/env python3
"""
🍋 LimoneIDE Google App Engine 배포 스크립트
자동화된 배포 및 환경 설정
"""

import os
import sys
import subprocess
import logging
import time
from pathlib import Path
from typing import Dict, Any, List, Optional

# 배포 설정 임포트
from deployment_config import deployment_config, validate_deployment_config, generate_app_yaml

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('deploy')

class AppEngineDeployer:
    """Google App Engine 배포 클래스"""
    
    def __init__(self):
        self.config = deployment_config
        self.project_id = self.config.get("google_cloud.project_id")
        self.service = self.config.get("app_engine.service")
        self.version = self.config.get("app_engine.version")
        
    def check_prerequisites(self) -> bool:
        """배포 전제 조건 확인"""
        logger.info("배포 전제 조건 확인 중...")
        
        # 1. gcloud CLI 확인
        try:
            result = subprocess.run(["gcloud", "--version"], capture_output=True, text=True)
            if result.returncode != 0:
                logger.error("gcloud CLI가 설치되지 않았습니다")
                return False
            logger.info("✅ gcloud CLI 확인됨")
        except FileNotFoundError:
            logger.error("gcloud CLI를 찾을 수 없습니다")
            return False
        
        # 2. gcloud 인증 확인
        try:
            result = subprocess.run(["gcloud", "auth", "list", "--filter=status:ACTIVE"], capture_output=True, text=True)
            if "No credentialed accounts" in result.stdout:
                logger.error("gcloud 인증이 필요합니다")
                return False
            logger.info("✅ gcloud 인증 확인됨")
        except Exception as e:
            logger.error(f"gcloud 인증 확인 실패: {e}")
            return False
        
        # 3. 프로젝트 설정 확인
        try:
            result = subprocess.run(["gcloud", "config", "get-value", "project"], capture_output=True, text=True)
            current_project = result.stdout.strip()
            if current_project != self.project_id:
                logger.warning(f"현재 프로젝트 ({current_project})와 설정 프로젝트 ({self.project_id})가 다릅니다")
                # 프로젝트 설정
                subprocess.run(["gcloud", "config", "set", "project", self.project_id], check=True)
                logger.info(f"프로젝트를 {self.project_id}로 설정했습니다")
            else:
                logger.info(f"✅ 프로젝트 설정 확인됨: {self.project_id}")
        except Exception as e:
            logger.error(f"프로젝트 설정 확인 실패: {e}")
            return False
        
        # 4. App Engine API 활성화 확인
        try:
            result = subprocess.run(["gcloud", "services", "list", "--enabled", "--filter=name:appengine.googleapis.com"], capture_output=True, text=True)
            if "appengine.googleapis.com" not in result.stdout:
                logger.info("App Engine API 활성화 중...")
                subprocess.run(["gcloud", "services", "enable", "appengine.googleapis.com"], check=True)
                logger.info("✅ App Engine API 활성화됨")
            else:
                logger.info("✅ App Engine API 확인됨")
        except Exception as e:
            logger.error(f"App Engine API 활성화 실패: {e}")
            return False
        
        return True
    
    def validate_configuration(self) -> bool:
        """배포 설정 유효성 검사"""
        logger.info("배포 설정 유효성 검사 중...")
        
        validation = validate_deployment_config()
        
        if validation["errors"]:
            logger.error("배포 설정 오류:")
            for error in validation["errors"]:
                logger.error(f"  - {error}")
            return False
        
        if validation["warnings"]:
            logger.warning("배포 설정 경고:")
            for warning in validation["warnings"]:
                logger.warning(f"  - {warning}")
        
        logger.info("✅ 배포 설정 유효성 검사 통과")
        return True
    
    def prepare_deployment_files(self) -> bool:
        """배포 파일 준비"""
        logger.info("배포 파일 준비 중...")
        
        try:
            # 1. app.yaml 생성
            app_yaml_path = generate_app_yaml()
            if not app_yaml_path:
                logger.error("app.yaml 생성 실패")
                return False
            logger.info(f"✅ app.yaml 생성됨: {app_yaml_path}")
            
            # 2. requirements.txt 확인
            if not os.path.exists("requirements.txt"):
                logger.error("requirements.txt 파일이 없습니다")
                return False
            logger.info("✅ requirements.txt 확인됨")
            
            # 3. 메인 애플리케이션 파일 확인
            if not os.path.exists("main.py"):
                logger.error("main.py 파일이 없습니다")
                return False
            logger.info("✅ main.py 확인됨")
            
            # 4. .gcloudignore 생성 (필요한 경우)
            gcloudignore_path = ".gcloudignore"
            if not os.path.exists(gcloudignore_path):
                gcloudignore_content = """# .gcloudignore
.git
.gitignore
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.env
*.log
test_*
*_test.py
docs/
*.md
!README.md
"""
                with open(gcloudignore_path, 'w', encoding='utf-8') as f:
                    f.write(gcloudignore_content)
                logger.info("✅ .gcloudignore 생성됨")
            
            return True
            
        except Exception as e:
            logger.error(f"배포 파일 준비 실패: {e}")
            return False
    
    def deploy_to_app_engine(self, promote: bool = True) -> bool:
        """App Engine에 배포"""
        logger.info(f"App Engine에 배포 중... (서비스: {self.service}, 버전: {self.version})")
        
        try:
            # 배포 명령어 구성
            deploy_cmd = [
                "gcloud", "app", "deploy",
                "--project", self.project_id,
                "--version", self.version,
                "--quiet"
            ]
            
            if promote:
                deploy_cmd.append("--promote")
            else:
                deploy_cmd.append("--no-promote")
            
            # 배포 실행
            logger.info(f"배포 명령어: {' '.join(deploy_cmd)}")
            result = subprocess.run(deploy_cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                logger.error(f"배포 실패: {result.stderr}")
                return False
            
            logger.info("✅ 배포 성공!")
            logger.info(f"배포 결과: {result.stdout}")
            
            # 배포 URL 출력
            if promote:
                app_url = f"https://{self.service}-dot-{self.project_id}.appspot.com"
                logger.info(f"애플리케이션 URL: {app_url}")
            
            return True
            
        except Exception as e:
            logger.error(f"배포 중 오류 발생: {e}")
            return False
    
    def verify_deployment(self) -> bool:
        """배포 검증"""
        logger.info("배포 검증 중...")
        
        try:
            # 1. 서비스 상태 확인
            result = subprocess.run([
                "gcloud", "app", "services", "list",
                "--project", self.project_id
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                logger.error("서비스 상태 확인 실패")
                return False
            
            if self.service not in result.stdout:
                logger.error(f"서비스 {self.service}가 배포되지 않았습니다")
                return False
            
            logger.info("✅ 서비스 배포 확인됨")
            
            # 2. 버전 상태 확인
            result = subprocess.run([
                "gcloud", "app", "versions", "list",
                "--service", self.service,
                "--project", self.project_id
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                logger.error("버전 상태 확인 실패")
                return False
            
            if self.version not in result.stdout:
                logger.error(f"버전 {self.version}이 배포되지 않았습니다")
                return False
            
            logger.info("✅ 버전 배포 확인됨")
            
            # 3. 헬스 체크 (선택적)
            app_url = f"https://{self.service}-dot-{self.project_id}.appspot.com/health"
            logger.info(f"헬스 체크 URL: {app_url}")
            
            return True
            
        except Exception as e:
            logger.error(f"배포 검증 실패: {e}")
            return False
    
    def rollback_deployment(self, version: str = None) -> bool:
        """배포 롤백"""
        if version is None:
            version = self.version
        
        logger.info(f"배포 롤백 중... (버전: {version})")
        
        try:
            result = subprocess.run([
                "gcloud", "app", "services", "set-traffic",
                self.service,
                f"--splits={version}=0",
                "--project", self.project_id
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                logger.error(f"롤백 실패: {result.stderr}")
                return False
            
            logger.info("✅ 롤백 성공!")
            return True
            
        except Exception as e:
            logger.error(f"롤백 중 오류 발생: {e}")
            return False
    
    def get_deployment_info(self) -> Dict[str, Any]:
        """배포 정보 조회"""
        try:
            result = subprocess.run([
                "gcloud", "app", "describe",
                "--project", self.project_id
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                return {"error": "배포 정보 조회 실패"}
            
            return {
                "project_id": self.project_id,
                "service": self.service,
                "version": self.version,
                "app_info": result.stdout
            }
            
        except Exception as e:
            return {"error": f"배포 정보 조회 중 오류: {e}"}

def main():
    """메인 배포 함수"""
    logger.info("🍋 LimoneIDE App Engine 배포 시작")
    
    deployer = AppEngineDeployer()
    
    # 1. 전제 조건 확인
    if not deployer.check_prerequisites():
        logger.error("배포 전제 조건 확인 실패")
        sys.exit(1)
    
    # 2. 설정 유효성 검사
    if not deployer.validate_configuration():
        logger.error("배포 설정 유효성 검사 실패")
        sys.exit(1)
    
    # 3. 배포 파일 준비
    if not deployer.prepare_deployment_files():
        logger.error("배포 파일 준비 실패")
        sys.exit(1)
    
    # 4. App Engine 배포
    if not deployer.deploy_to_app_engine():
        logger.error("App Engine 배포 실패")
        sys.exit(1)
    
    # 5. 배포 검증
    if not deployer.verify_deployment():
        logger.error("배포 검증 실패")
        sys.exit(1)
    
    logger.info("🎉 LimoneIDE App Engine 배포 완료!")
    
    # 배포 정보 출력
    deployment_info = deployer.get_deployment_info()
    logger.info(f"배포 정보: {deployment_info}")

if __name__ == "__main__":
    main() 