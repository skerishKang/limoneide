#!/usr/bin/env python3
"""
🍋 LimoneIDE E2E 통합 테스트 스크립트 (고급)
전체 시스템의 End-to-End 테스트 및 성능 최적화

작성일: 2025-06-24
버전: 2.0
"""

import asyncio
import time
import json
import requests
import subprocess
import sys
import os
from typing import Dict, List, Any
from datetime import datetime
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('e2e_test.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class E2ETestSuite:
    """
    LimoneIDE E2E 통합 테스트 스위트
    """
    
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.frontend_url = "http://localhost:3000"
        self.test_results = []
        self.performance_metrics = {}
        self.start_time = time.time()
        
    async def run_all_tests(self):
        """모든 E2E 테스트 실행"""
        logger.info("🚀 LimoneIDE E2E 통합 테스트 시작")
        
        try:
            # 1. 시스템 상태 확인
            await self.test_system_status()
            
            # 2. 인증 플로우 테스트
            await self.test_authentication_flow()
            
            # 3. 프로젝트 생성 테스트
            await self.test_project_creation()
            
            # 4. 음성 명령 처리 테스트
            await self.test_voice_command_processing()
            
            # 5. AI 코드 생성 테스트
            await self.test_ai_code_generation()
            
            # 6. 배포 파이프라인 테스트
            await self.test_deployment_pipeline()
            
            # 7. Cloud SQL 연동 테스트
            await self.test_cloudsql_integration()
            
            # 8. 블로그 템플릿 테스트
            await self.test_blog_template()
            
            # 9. 성능 테스트
            await self.test_performance()
            
            # 10. 오류 처리 테스트
            await self.test_error_handling()
            
            # 결과 요약
            await self.generate_test_report()
            
        except Exception as e:
            logger.error(f"E2E 테스트 실행 중 오류 발생: {e}")
            await self.generate_test_report()
    
    async def test_system_status(self):
        """시스템 상태 확인 테스트"""
        logger.info("📊 시스템 상태 확인 테스트 시작")
        
        test_name = "System Status Check"
        start_time = time.time()
        
        try:
            # 백엔드 서버 상태 확인
            backend_response = requests.get(f"{self.base_url}/health", timeout=10)
            backend_status = backend_response.status_code == 200
            
            # 프론트엔드 서버 상태 확인
            frontend_response = requests.get(self.frontend_url, timeout=10)
            frontend_status = frontend_response.status_code == 200
            
            success = backend_status and frontend_status
            duration = time.time() - start_time
            
            self.record_test_result(test_name, success, duration, {
                "backend_status": backend_status,
                "frontend_status": frontend_status
            })
            
            logger.info(f"✅ 시스템 상태 확인 완료: {success}")
            
        except Exception as e:
            self.record_test_result(test_name, False, time.time() - start_time, {"error": str(e)})
            logger.error(f"❌ 시스템 상태 확인 실패: {e}")
    
    async def test_authentication_flow(self):
        """인증 플로우 테스트"""
        logger.info("🔐 인증 플로우 테스트 시작")
        
        test_name = "Authentication Flow"
        start_time = time.time()
        
        try:
            # OAuth 엔드포인트 확인
            oauth_response = requests.get(f"{self.base_url}/auth/google", timeout=10)
            oauth_status = oauth_response.status_code in [200, 302]
            
            success = oauth_status
            duration = time.time() - start_time
            
            self.record_test_result(test_name, success, duration, {
                "oauth_status": oauth_status
            })
            
            logger.info(f"✅ 인증 플로우 테스트 완료: {success}")
            
        except Exception as e:
            self.record_test_result(test_name, False, time.time() - start_time, {"error": str(e)})
            logger.error(f"❌ 인증 플로우 테스트 실패: {e}")
    
    async def test_project_creation(self):
        """프로젝트 생성 테스트"""
        logger.info("🏗️ 프로젝트 생성 테스트 시작")
        
        test_name = "Project Creation"
        start_time = time.time()
        
        try:
            # 프로젝트 생성 API 테스트
            project_data = {
                "name": "test-project-e2e",
                "description": "E2E 테스트용 프로젝트",
                "template": "general"
            }
            
            create_response = requests.post(
                f"{self.base_url}/api/projects",
                json=project_data,
                timeout=30
            )
            
            success = create_response.status_code in [200, 201]
            duration = time.time() - start_time
            
            self.record_test_result(test_name, success, duration, {
                "response_status": create_response.status_code
            })
            
            logger.info(f"✅ 프로젝트 생성 테스트 완료: {success}")
            
        except Exception as e:
            self.record_test_result(test_name, False, time.time() - start_time, {"error": str(e)})
            logger.error(f"❌ 프로젝트 생성 테스트 실패: {e}")
    
    async def test_voice_command_processing(self):
        """음성 명령 처리 테스트"""
        logger.info("🎤 음성 명령 처리 테스트 시작")
        
        test_name = "Voice Command Processing"
        start_time = time.time()
        
        try:
            # 음성 명령 API 테스트
            voice_data = {
                "command": "케이크를 파는 예쁜 쇼핑몰 만들어줘",
                "language": "ko",
                "project_id": "test-project-e2e"
            }
            
            voice_response = requests.post(
                f"{self.base_url}/api/voice/process",
                json=voice_data,
                timeout=30
            )
            
            success = voice_response.status_code in [200, 201]
            duration = time.time() - start_time
            
            self.record_test_result(test_name, success, duration, {
                "response_status": voice_response.status_code
            })
            
            logger.info(f"✅ 음성 명령 처리 테스트 완료: {success}")
            
        except Exception as e:
            self.record_test_result(test_name, False, time.time() - start_time, {"error": str(e)})
            logger.error(f"❌ 음성 명령 처리 테스트 실패: {e}")
    
    async def test_ai_code_generation(self):
        """AI 코드 생성 테스트"""
        logger.info("🤖 AI 코드 생성 테스트 시작")
        
        test_name = "AI Code Generation"
        start_time = time.time()
        
        try:
            # AI 코드 생성 API 테스트
            ai_data = {
                "command": "케이크를 파는 예쁜 쇼핑몰 만들어줘",
                "template": "ecommerce",
                "features": ["responsive", "payment", "inventory"],
                "project_id": "test-project-e2e"
            }
            
            ai_response = requests.post(
                f"{self.base_url}/api/ai/generate",
                json=ai_data,
                timeout=60
            )
            
            success = ai_response.status_code in [200, 201]
            duration = time.time() - start_time
            
            self.record_test_result(test_name, success, duration, {
                "response_status": ai_response.status_code
            })
            
            logger.info(f"✅ AI 코드 생성 테스트 완료: {success}")
            
        except Exception as e:
            self.record_test_result(test_name, False, time.time() - start_time, {"error": str(e)})
            logger.error(f"❌ AI 코드 생성 테스트 실패: {e}")
    
    async def test_deployment_pipeline(self):
        """배포 파이프라인 테스트"""
        logger.info("🚀 배포 파이프라인 테스트 시작")
        
        test_name = "Deployment Pipeline"
        start_time = time.time()
        
        try:
            # 배포 시작 API 테스트
            deploy_data = {
                "project_id": "test-project-e2e",
                "template": "ecommerce",
                "deployment_type": "app_engine"
            }
            
            deploy_response = requests.post(
                f"{self.base_url}/api/deploy/start",
                json=deploy_data,
                timeout=120
            )
            
            success = deploy_response.status_code in [200, 201, 202]
            duration = time.time() - start_time
            
            self.record_test_result(test_name, success, duration, {
                "response_status": deploy_response.status_code
            })
            
            logger.info(f"✅ 배포 파이프라인 테스트 완료: {success}")
            
        except Exception as e:
            self.record_test_result(test_name, False, time.time() - start_time, {"error": str(e)})
            logger.error(f"❌ 배포 파이프라인 테스트 실패: {e}")
    
    async def test_cloudsql_integration(self):
        """Cloud SQL 연동 테스트"""
        logger.info("🗄️ Cloud SQL 연동 테스트 시작")
        
        test_name = "Cloud SQL Integration"
        start_time = time.time()
        
        try:
            # Cloud SQL 연결 테스트
            cloudsql_data = {
                "project_id": "test-project-e2e",
                "instance_name": "test-instance",
                "database_type": "mysql"
            }
            
            cloudsql_response = requests.post(
                f"{self.base_url}/api/cloudsql/test-connection",
                json=cloudsql_data,
                timeout=30
            )
            
            success = cloudsql_response.status_code in [200, 201]
            duration = time.time() - start_time
            
            self.record_test_result(test_name, success, duration, {
                "response_status": cloudsql_response.status_code
            })
            
            logger.info(f"✅ Cloud SQL 연동 테스트 완료: {success}")
            
        except Exception as e:
            self.record_test_result(test_name, False, time.time() - start_time, {"error": str(e)})
            logger.error(f"❌ Cloud SQL 연동 테스트 실패: {e}")
    
    async def test_blog_template(self):
        """블로그 템플릿 테스트"""
        logger.info("📝 블로그 템플릿 테스트 시작")
        
        test_name = "Blog Template"
        start_time = time.time()
        
        try:
            # 블로그 템플릿 생성 테스트
            blog_data = {
                "command": "방명록이 있는 블로그 만들어줘",
                "features": ["blog_posts", "guestbook", "comments"]
            }
            
            blog_response = requests.post(
                f"{self.base_url}/api/templates/blog",
                json=blog_data,
                timeout=30
            )
            
            success = blog_response.status_code in [200, 201]
            duration = time.time() - start_time
            
            self.record_test_result(test_name, success, duration, {
                "response_status": blog_response.status_code
            })
            
            logger.info(f"✅ 블로그 템플릿 테스트 완료: {success}")
            
        except Exception as e:
            self.record_test_result(test_name, False, time.time() - start_time, {"error": str(e)})
            logger.error(f"❌ 블로그 템플릿 테스트 실패: {e}")
    
    async def test_performance(self):
        """성능 테스트"""
        logger.info("⚡ 성능 테스트 시작")
        
        test_name = "Performance Test"
        start_time = time.time()
        
        try:
            # 응답 시간 테스트
            response_times = []
            
            for i in range(5):
                test_start = time.time()
                response = requests.get(f"{self.base_url}/health", timeout=10)
                test_duration = time.time() - test_start
                response_times.append(test_duration)
            
            avg_response_time = sum(response_times) / len(response_times)
            max_response_time = max(response_times)
            
            # 성능 기준: 평균 응답 시간 < 1초
            success = avg_response_time < 1.0
            duration = time.time() - start_time
            
            self.record_test_result(test_name, success, duration, {
                "avg_response_time": avg_response_time,
                "max_response_time": max_response_time,
                "response_times": response_times
            })
            
            logger.info(f"✅ 성능 테스트 완료: {success} (평균 응답시간: {avg_response_time:.3f}s)")
            
        except Exception as e:
            self.record_test_result(test_name, False, time.time() - start_time, {"error": str(e)})
            logger.error(f"❌ 성능 테스트 실패: {e}")
    
    async def test_error_handling(self):
        """오류 처리 테스트"""
        logger.info("🛡️ 오류 처리 테스트 시작")
        
        test_name = "Error Handling"
        start_time = time.time()
        
        try:
            # 잘못된 요청 테스트
            invalid_data = {
                "invalid_field": "invalid_value"
            }
            
            error_response = requests.post(
                f"{self.base_url}/api/projects",
                json=invalid_data,
                timeout=10
            )
            
            # 오류 응답이 적절히 처리되는지 확인
            success = error_response.status_code in [400, 422]
            duration = time.time() - start_time
            
            self.record_test_result(test_name, success, duration, {
                "error_status_code": error_response.status_code
            })
            
            logger.info(f"✅ 오류 처리 테스트 완료: {success}")
            
        except Exception as e:
            self.record_test_result(test_name, False, time.time() - start_time, {"error": str(e)})
            logger.error(f"❌ 오류 처리 테스트 실패: {e}")
    
    def record_test_result(self, test_name: str, success: bool, duration: float, details: Dict[str, Any]):
        """테스트 결과 기록"""
        result = {
            "test_name": test_name,
            "success": success,
            "duration": duration,
            "timestamp": datetime.now().isoformat(),
            "details": details
        }
        self.test_results.append(result)
        
        # 성능 메트릭 저장
        if test_name not in self.performance_metrics:
            self.performance_metrics[test_name] = []
        self.performance_metrics[test_name].append(duration)
    
    async def generate_test_report(self):
        """테스트 리포트 생성"""
        logger.info("📊 테스트 리포트 생성 중...")
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        total_duration = time.time() - self.start_time
        
        # 성능 통계 계산
        performance_stats = {}
        for test_name, durations in self.performance_metrics.items():
            if durations:
                performance_stats[test_name] = {
                    "avg_duration": sum(durations) / len(durations),
                    "min_duration": min(durations),
                    "max_duration": max(durations),
                    "count": len(durations)
                }
        
        report = {
            "test_summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "success_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0,
                "total_duration": total_duration
            },
            "test_results": self.test_results,
            "performance_metrics": performance_stats,
            "timestamp": datetime.now().isoformat(),
            "version": "2.0"
        }
        
        # 리포트 파일 저장
        with open("e2e_test_report.json", "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        # 콘솔 출력
        print("\n" + "="*60)
        print("🍋 LimoneIDE E2E 통합 테스트 리포트")
        print("="*60)
        print(f"총 테스트 수: {total_tests}")
        print(f"성공: {passed_tests}")
        print(f"실패: {failed_tests}")
        print(f"성공률: {report['test_summary']['success_rate']:.1f}%")
        print(f"총 소요시간: {total_duration:.2f}초")
        print("="*60)
        
        # 실패한 테스트 목록
        if failed_tests > 0:
            print("\n❌ 실패한 테스트:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  - {result['test_name']}: {result['details'].get('error', 'Unknown error')}")
        
        # 성능 요약
        print("\n⚡ 성능 요약:")
        for test_name, stats in performance_stats.items():
            print(f"  - {test_name}: 평균 {stats['avg_duration']:.3f}초")
        
        print(f"\n📄 상세 리포트: e2e_test_report.json")
        print("="*60)
        
        logger.info(f"E2E 테스트 완료: {passed_tests}/{total_tests} 성공")

async def main():
    """메인 함수"""
    print("🍋 LimoneIDE E2E 통합 테스트 시작")
    print("="*60)
    
    # 테스트 스위트 실행
    test_suite = E2ETestSuite()
    await test_suite.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main()) 