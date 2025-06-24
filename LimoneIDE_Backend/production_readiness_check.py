#!/usr/bin/env python3
"""
🍋 LimoneIDE 프로덕션 배포 준비 상태 확인
배포 전 최종 점검 및 검증
"""

import os
import sys
import json
import logging
import asyncio
import requests
from typing import Dict, Any, List, Optional
from pathlib import Path

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('production_readiness')

class ProductionReadinessChecker:
    """프로덕션 배포 준비 상태 확인 클래스"""
    
    def __init__(self):
        self.checks = []
        self.results = {}
        
    def add_check(self, name: str, check_func, critical: bool = True):
        """확인 항목 추가"""
        self.checks.append({
            "name": name,
            "function": check_func,
            "critical": critical
        })
    
    def check_file_structure(self) -> Dict[str, Any]:
        """파일 구조 확인"""
        logger.info("파일 구조 확인 중...")
        
        required_files = [
            "main.py",
            "requirements.txt",
            "app.yaml",
            "deployment_config.py",
            "deploy.py"
        ]
        
        required_dirs = [
            "src/core",
            "src/automation",
            "src/templates",
            "src/voice",
            "docs"
        ]
        
        missing_files = []
        missing_dirs = []
        
        for file in required_files:
            if not os.path.exists(file):
                missing_files.append(file)
        
        for dir_path in required_dirs:
            if not os.path.exists(dir_path):
                missing_dirs.append(dir_path)
        
        if missing_files or missing_dirs:
            return {
                "status": "FAIL",
                "message": f"필수 파일/디렉토리 누락",
                "missing_files": missing_files,
                "missing_dirs": missing_dirs
            }
        
        return {
            "status": "PASS",
            "message": "모든 필수 파일/디렉토리 존재"
        }
    
    def check_dependencies(self) -> Dict[str, Any]:
        """의존성 확인"""
        logger.info("의존성 확인 중...")
        
        try:
            with open("requirements.txt", "r", encoding="utf-8") as f:
                requirements = f.read().strip().split("\n")
            
            missing_packages = []
            for req in requirements:
                if req.strip() and not req.startswith("#"):
                    package_name = req.split("==")[0].split(">=")[0].split("<=")[0]
                    try:
                        __import__(package_name.replace("-", "_"))
                    except ImportError:
                        missing_packages.append(package_name)
            
            if missing_packages:
                return {
                    "status": "FAIL",
                    "message": f"누락된 패키지: {', '.join(missing_packages)}"
                }
            
            return {
                "status": "PASS",
                "message": "모든 의존성 패키지 설치됨"
            }
            
        except Exception as e:
            return {
                "status": "FAIL",
                "message": f"의존성 확인 실패: {e}"
            }
    
    def check_environment_variables(self) -> Dict[str, Any]:
        """환경변수 확인"""
        logger.info("환경변수 확인 중...")
        
        required_env_vars = [
            "GOOGLE_CLOUD_PROJECT",
            "OPENAI_API_KEY",
            "GEMINI_API_KEY"
        ]
        
        optional_env_vars = [
            "CLAUDE_API_KEY",
            "OLLAMA_BASE_URL"
        ]
        
        missing_required = []
        missing_optional = []
        
        for var in required_env_vars:
            if not os.getenv(var):
                missing_required.append(var)
        
        for var in optional_env_vars:
            if not os.getenv(var):
                missing_optional.append(var)
        
        if missing_required:
            return {
                "status": "FAIL",
                "message": f"필수 환경변수 누락: {', '.join(missing_required)}"
            }
        
        warnings = []
        if missing_optional:
            warnings.append(f"선택적 환경변수 누락: {', '.join(missing_optional)}")
        
        return {
            "status": "PASS",
            "message": "필수 환경변수 설정됨",
            "warnings": warnings
        }
    
    def check_app_configuration(self) -> Dict[str, Any]:
        """앱 설정 확인"""
        logger.info("앱 설정 확인 중...")
        
        try:
            from deployment_config import deployment_config, validate_deployment_config
            
            validation = validate_deployment_config()
            
            if validation["errors"]:
                return {
                    "status": "FAIL",
                    "message": "배포 설정 오류",
                    "errors": validation["errors"]
                }
            
            warnings = []
            if validation["warnings"]:
                warnings.extend(validation["warnings"])
            
            return {
                "status": "PASS",
                "message": "배포 설정 유효함",
                "warnings": warnings
            }
            
        except Exception as e:
            return {
                "status": "FAIL",
                "message": f"앱 설정 확인 실패: {e}"
            }
    
    async def check_ai_services(self) -> Dict[str, Any]:
        """AI 서비스 연결 확인"""
        logger.info("AI 서비스 연결 확인 중...")
        
        try:
            from src.core.ai_engine import AIEngine
            
            ai_engine = AIEngine()
            services_status = {}
            
            # OpenAI 확인
            if os.getenv("OPENAI_API_KEY"):
                try:
                    response = await ai_engine.generate_response("테스트", "openai")
                    services_status["openai"] = "PASS"
                except Exception as e:
                    services_status["openai"] = f"FAIL: {e}"
            else:
                services_status["openai"] = "SKIP: API 키 없음"
            
            # Gemini 확인
            if os.getenv("GEMINI_API_KEY"):
                try:
                    response = await ai_engine.generate_response("테스트", "gemini")
                    services_status["gemini"] = "PASS"
                except Exception as e:
                    services_status["gemini"] = f"FAIL: {e}"
            else:
                services_status["gemini"] = "SKIP: API 키 없음"
            
            failed_services = [service for service, status in services_status.items() if status.startswith("FAIL")]
            
            if failed_services:
                return {
                    "status": "FAIL",
                    "message": f"AI 서비스 연결 실패: {', '.join(failed_services)}",
                    "services": services_status
                }
            
            return {
                "status": "PASS",
                "message": "AI 서비스 연결 확인됨",
                "services": services_status
            }
            
        except Exception as e:
            return {
                "status": "FAIL",
                "message": f"AI 서비스 확인 실패: {e}"
            }
    
    def check_security(self) -> Dict[str, Any]:
        """보안 설정 확인"""
        logger.info("보안 설정 확인 중...")
        
        security_issues = []
        warnings = []
        
        # 1. .env 파일 확인
        if os.path.exists(".env"):
            warnings.append(".env 파일이 소스 코드에 포함되어 있습니다")
        
        # 2. API 키 노출 확인
        sensitive_files = [
            "main.py",
            "src/core/ai_openai.py",
            "src/core/ai_gemini.py",
            "src/core/ai_claude.py"
        ]
        
        for file_path in sensitive_files:
            if os.path.exists(file_path):
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        if "sk-" in content or "AIza" in content:
                            security_issues.append(f"{file_path}에 API 키가 하드코딩되어 있습니다")
                except Exception:
                    pass
        
        # 3. CORS 설정 확인
        try:
            from deployment_config import get_config
            cors_enabled = get_config("security.cors_enabled", False)
            if not cors_enabled:
                warnings.append("CORS가 비활성화되어 있습니다")
        except Exception:
            warnings.append("CORS 설정을 확인할 수 없습니다")
        
        if security_issues:
            return {
                "status": "FAIL",
                "message": "보안 문제 발견",
                "issues": security_issues,
                "warnings": warnings
            }
        
        return {
            "status": "PASS",
            "message": "보안 설정 확인됨",
            "warnings": warnings
        }
    
    def check_performance(self) -> Dict[str, Any]:
        """성능 설정 확인"""
        logger.info("성능 설정 확인 중...")
        
        try:
            from deployment_config import get_config
            
            performance_issues = []
            warnings = []
            
            # 캐시 설정 확인
            cache_enabled = get_config("performance.cache_enabled", False)
            if not cache_enabled:
                warnings.append("캐시가 비활성화되어 있습니다")
            
            # 동시 요청 제한 확인
            max_requests = get_config("performance.max_concurrent_requests", 100)
            if max_requests > 1000:
                performance_issues.append("최대 동시 요청 수가 너무 높습니다 (1000 이하 권장)")
            
            # 응답 타임아웃 확인
            timeout = get_config("performance.response_timeout", 30)
            if timeout < 10:
                performance_issues.append("응답 타임아웃이 너무 짧습니다 (10초 이상 권장)")
            
            if performance_issues:
                return {
                    "status": "FAIL",
                    "message": "성능 설정 문제",
                    "issues": performance_issues,
                    "warnings": warnings
                }
            
            return {
                "status": "PASS",
                "message": "성능 설정 확인됨",
                "warnings": warnings
            }
            
        except Exception as e:
            return {
                "status": "FAIL",
                "message": f"성능 설정 확인 실패: {e}"
            }
    
    def check_documentation(self) -> Dict[str, Any]:
        """문서화 확인"""
        logger.info("문서화 확인 중...")
        
        required_docs = [
            "README.md",
            "docs/technical_whitepaper.md",
            "project_plan.md",
            "performance_test_report.md"
        ]
        
        missing_docs = []
        for doc in required_docs:
            if not os.path.exists(doc):
                missing_docs.append(doc)
        
        if missing_docs:
            return {
                "status": "WARN",
                "message": f"문서 누락: {', '.join(missing_docs)}"
            }
        
        return {
            "status": "PASS",
            "message": "필수 문서 존재"
        }
    
    async def run_all_checks(self) -> Dict[str, Any]:
        """모든 확인 실행"""
        logger.info("🍋 프로덕션 배포 준비 상태 확인 시작")
        
        # 확인 항목 등록
        self.add_check("파일 구조", self.check_file_structure)
        self.add_check("의존성", self.check_dependencies)
        self.add_check("환경변수", self.check_environment_variables)
        self.add_check("앱 설정", self.check_app_configuration)
        self.add_check("AI 서비스", self.check_ai_services)
        self.add_check("보안", self.check_security)
        self.add_check("성능", self.check_performance)
        self.add_check("문서화", self.check_documentation, critical=False)
        
        # 확인 실행
        for check in self.checks:
            logger.info(f"확인 중: {check['name']}")
            
            try:
                if asyncio.iscoroutinefunction(check['function']):
                    result = await check['function']()
                else:
                    result = check['function']()
                
                self.results[check['name']] = result
                logger.info(f"{check['name']}: {result['status']}")
                
            except Exception as e:
                self.results[check['name']] = {
                    "status": "ERROR",
                    "message": f"확인 중 오류 발생: {e}"
                }
                logger.error(f"{check['name']}: ERROR - {e}")
        
        return self.generate_summary()
    
    def generate_summary(self) -> Dict[str, Any]:
        """확인 결과 요약"""
        total_checks = len(self.checks)
        passed_checks = sum(1 for result in self.results.values() if result['status'] == 'PASS')
        failed_checks = sum(1 for result in self.results.values() if result['status'] == 'FAIL')
        warning_checks = sum(1 for result in self.results.values() if result['status'] == 'WARN')
        error_checks = sum(1 for result in self.results.values() if result['status'] == 'ERROR')
        
        # 크리티컬 실패 확인
        critical_failures = []
        for check in self.checks:
            if check['critical'] and self.results.get(check['name'], {}).get('status') == 'FAIL':
                critical_failures.append(check['name'])
        
        overall_status = "PASS"
        if critical_failures:
            overall_status = "FAIL"
        elif failed_checks > 0:
            overall_status = "WARN"
        
        summary = {
            "overall_status": overall_status,
            "total_checks": total_checks,
            "passed": passed_checks,
            "failed": failed_checks,
            "warnings": warning_checks,
            "errors": error_checks,
            "critical_failures": critical_failures,
            "results": self.results
        }
        
        return summary
    
    def print_report(self, summary: Dict[str, Any]):
        """확인 결과 리포트 출력"""
        print("\n" + "="*60)
        print("🍋 LimoneIDE 프로덕션 배포 준비 상태 확인 리포트")
        print("="*60)
        
        print(f"\n📊 전체 상태: {summary['overall_status']}")
        print(f"📋 총 확인 항목: {summary['total_checks']}")
        print(f"✅ 통과: {summary['passed']}")
        print(f"❌ 실패: {summary['failed']}")
        print(f"⚠️  경고: {summary['warnings']}")
        print(f"🚨 오류: {summary['errors']}")
        
        if summary['critical_failures']:
            print(f"\n🚨 크리티컬 실패 항목:")
            for failure in summary['critical_failures']:
                print(f"  - {failure}")
        
        print(f"\n📋 상세 결과:")
        for check_name, result in summary['results'].items():
            status_icon = {
                'PASS': '✅',
                'FAIL': '❌',
                'WARN': '⚠️',
                'ERROR': '🚨'
            }.get(result['status'], '❓')
            
            print(f"{status_icon} {check_name}: {result['status']}")
            print(f"   {result['message']}")
            
            if 'warnings' in result and result['warnings']:
                for warning in result['warnings']:
                    print(f"   ⚠️  {warning}")
            
            if 'errors' in result and result['errors']:
                for error in result['errors']:
                    print(f"   ❌ {error}")
            
            print()
        
        print("="*60)
        
        if summary['overall_status'] == 'PASS':
            print("🎉 프로덕션 배포 준비 완료!")
        elif summary['overall_status'] == 'WARN':
            print("⚠️  경고 사항이 있지만 배포 가능합니다.")
        else:
            print("❌ 크리티컬 문제가 있어 배포를 중단해야 합니다.")

async def main():
    """메인 함수"""
    checker = ProductionReadinessChecker()
    summary = await checker.run_all_checks()
    checker.print_report(summary)
    
    # 결과를 파일로 저장
    with open("production_readiness_report.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    # 종료 코드 설정
    if summary['overall_status'] == 'FAIL':
        sys.exit(1)
    elif summary['overall_status'] == 'WARN':
        sys.exit(2)
    else:
        sys.exit(0)

if __name__ == "__main__":
    asyncio.run(main()) 