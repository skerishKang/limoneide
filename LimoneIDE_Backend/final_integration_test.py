#!/usr/bin/env python3
"""
🍋 LimoneIDE 최종 통합 테스트
모든 기능의 통합 테스트 및 최종 검증
"""

import asyncio
import time
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('final_integration_test')

class FinalIntegrationTester:
    """최종 통합 테스트 클래스"""
    
    def __init__(self):
        self.test_results = {}
        self.start_time = time.time()
        
    async def test_ai_engine_integration(self) -> Dict[str, Any]:
        """AI 엔진 통합 테스트"""
        logger.info("AI 엔진 통합 테스트 시작")
        
        try:
            from src.core.ai_engine import AIEngine
            
            ai_engine = AIEngine()
            
            # 기본 응답 생성 테스트
            response = await ai_engine.generate_response("안녕하세요", "gemini")
            
            if response and len(response) > 0:
                return {
                    "status": "PASS",
                    "message": "AI 엔진 응답 생성 성공",
                    "response_length": len(response)
                }
            else:
                return {
                    "status": "FAIL",
                    "message": "AI 엔진 응답이 비어있음"
                }
                
        except Exception as e:
            return {
                "status": "FAIL",
                "message": f"AI 엔진 테스트 실패: {e}"
            }
    
    async def test_template_system(self) -> Dict[str, Any]:
        """템플릿 시스템 테스트"""
        logger.info("템플릿 시스템 테스트 시작")
        
        try:
            from src.templates.blog_template import BlogTemplate
            
            template = BlogTemplate()
            result = template.generate({
                "title": "테스트 블로그",
                "description": "통합 테스트용 블로그",
                "features": ["blog_posts", "guestbook"]
            })
            
            if result and "html" in result:
                return {
                    "status": "PASS",
                    "message": "블로그 템플릿 생성 성공",
                    "html_length": len(result["html"])
                }
            else:
                return {
                    "status": "FAIL",
                    "message": "템플릿 생성 결과가 올바르지 않음"
                }
                
        except Exception as e:
            return {
                "status": "FAIL",
                "message": f"템플릿 시스템 테스트 실패: {e}"
            }
    
    async def test_voice_processing(self) -> Dict[str, Any]:
        """음성 처리 시스템 테스트"""
        logger.info("음성 처리 시스템 테스트 시작")
        
        try:
            from src.voice.voice_commands import VoiceCommandProcessor
            
            processor = VoiceCommandProcessor()
            
            # 음성 명령 처리 테스트 (텍스트 기반)
            command = "블로그 웹사이트를 만들어줘"
            result = processor.process_command(command)
            
            if result and "intent" in result:
                return {
                    "status": "PASS",
                    "message": "음성 명령 처리 성공",
                    "intent": result["intent"]
                }
            else:
                return {
                    "status": "FAIL",
                    "message": "음성 명령 처리 결과가 올바르지 않음"
                }
                
        except Exception as e:
            return {
                "status": "FAIL",
                "message": f"음성 처리 시스템 테스트 실패: {e}"
            }
    
    async def test_automation_system(self) -> Dict[str, Any]:
        """자동화 시스템 테스트"""
        logger.info("자동화 시스템 테스트 시작")
        
        try:
            from src.automation.website_builder import WebsiteBuilder
            
            builder = WebsiteBuilder()
            
            # 웹사이트 빌드 테스트
            result = builder.build_website({
                "template": "blog",
                "config": {
                    "title": "테스트 사이트",
                    "description": "통합 테스트용"
                }
            })
            
            if result and "status" in result:
                return {
                    "status": "PASS",
                    "message": "웹사이트 빌드 성공",
                    "build_status": result["status"]
                }
            else:
                return {
                    "status": "FAIL",
                    "message": "웹사이트 빌드 결과가 올바르지 않음"
                }
                
        except Exception as e:
            return {
                "status": "FAIL",
                "message": f"자동화 시스템 테스트 실패: {e}"
            }
    
    async def test_deployment_config(self) -> Dict[str, Any]:
        """배포 설정 테스트"""
        logger.info("배포 설정 테스트 시작")
        
        try:
            from deployment_config import deployment_config, validate_deployment_config
            
            validation = validate_deployment_config()
            
            if validation["valid"]:
                return {
                    "status": "PASS",
                    "message": "배포 설정 유효함",
                    "warnings": validation.get("warnings", [])
                }
            else:
                return {
                    "status": "FAIL",
                    "message": "배포 설정 오류",
                    "errors": validation.get("errors", [])
                }
                
        except Exception as e:
            return {
                "status": "FAIL",
                "message": f"배포 설정 테스트 실패: {e}"
            }
    
    async def test_performance_optimization(self) -> Dict[str, Any]:
        """성능 최적화 테스트"""
        logger.info("성능 최적화 테스트 시작")
        
        try:
            from optimized_ai_engine import OptimizedAIEngine
            
            engine = OptimizedAIEngine()
            
            # 성능 통계 확인
            stats = engine.get_performance_stats()
            
            if stats and "cache_hit_rate" in stats:
                return {
                    "status": "PASS",
                    "message": "성능 최적화 엔진 정상",
                    "cache_hit_rate": stats["cache_hit_rate"],
                    "total_requests": stats["total_requests"]
                }
            else:
                return {
                    "status": "FAIL",
                    "message": "성능 통계를 가져올 수 없음"
                }
                
        except Exception as e:
            return {
                "status": "FAIL",
                "message": f"성능 최적화 테스트 실패: {e}"
            }
    
    async def test_file_structure(self) -> Dict[str, Any]:
        """파일 구조 테스트"""
        logger.info("파일 구조 테스트 시작")
        
        required_files = [
            "main.py",
            "requirements.txt",
            "app.yaml",
            "deployment_config.py",
            "deploy.py",
            "production_readiness_check.py",
            "README.md"
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
                "message": "필수 파일/디렉토리 누락",
                "missing_files": missing_files,
                "missing_dirs": missing_dirs
            }
        
        return {
            "status": "PASS",
            "message": "모든 필수 파일/디렉토리 존재"
        }
    
    async def test_documentation(self) -> Dict[str, Any]:
        """문서화 테스트"""
        logger.info("문서화 테스트 시작")
        
        required_docs = [
            "README.md",
            "docs/technical_whitepaper.md",
            "project_plan.md",
            "performance_test_report.md",
            "production_deployment_guide.md"
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
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """모든 통합 테스트 실행"""
        logger.info("🍋 LimoneIDE 최종 통합 테스트 시작")
        
        test_functions = [
            ("AI 엔진 통합", self.test_ai_engine_integration),
            ("템플릿 시스템", self.test_template_system),
            ("음성 처리", self.test_voice_processing),
            ("자동화 시스템", self.test_automation_system),
            ("배포 설정", self.test_deployment_config),
            ("성능 최적화", self.test_performance_optimization),
            ("파일 구조", self.test_file_structure),
            ("문서화", self.test_documentation)
        ]
        
        for test_name, test_func in test_functions:
            logger.info(f"테스트 실행: {test_name}")
            
            try:
                result = await test_func()
                self.test_results[test_name] = result
                logger.info(f"{test_name}: {result['status']}")
                
            except Exception as e:
                self.test_results[test_name] = {
                    "status": "ERROR",
                    "message": f"테스트 중 오류 발생: {e}"
                }
                logger.error(f"{test_name}: ERROR - {e}")
        
        return self.generate_summary()
    
    def generate_summary(self) -> Dict[str, Any]:
        """테스트 결과 요약"""
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results.values() if result['status'] == 'PASS')
        failed_tests = sum(1 for result in self.test_results.values() if result['status'] == 'FAIL')
        warning_tests = sum(1 for result in self.test_results.values() if result['status'] == 'WARN')
        error_tests = sum(1 for result in self.test_results.values() if result['status'] == 'ERROR')
        
        # 전체 상태 결정
        if failed_tests > 0 or error_tests > 0:
            overall_status = "FAIL"
        elif warning_tests > 0:
            overall_status = "WARN"
        else:
            overall_status = "PASS"
        
        test_duration = time.time() - self.start_time
        
        summary = {
            "overall_status": overall_status,
            "test_duration": test_duration,
            "total_tests": total_tests,
            "passed": passed_tests,
            "failed": failed_tests,
            "warnings": warning_tests,
            "errors": error_tests,
            "success_rate": passed_tests / total_tests if total_tests > 0 else 0,
            "results": self.test_results,
            "timestamp": datetime.now().isoformat()
        }
        
        return summary
    
    def print_report(self, summary: Dict[str, Any]):
        """테스트 결과 리포트 출력"""
        print("\n" + "="*60)
        print("🍋 LimoneIDE 최종 통합 테스트 리포트")
        print("="*60)
        
        print(f"\n📊 전체 상태: {summary['overall_status']}")
        print(f"⏱️  테스트 시간: {summary['test_duration']:.2f}초")
        print(f"📋 총 테스트: {summary['total_tests']}")
        print(f"✅ 통과: {summary['passed']}")
        print(f"❌ 실패: {summary['failed']}")
        print(f"⚠️  경고: {summary['warnings']}")
        print(f"🚨 오류: {summary['errors']}")
        print(f"📈 성공률: {summary['success_rate']*100:.1f}%")
        
        print(f"\n📋 상세 결과:")
        for test_name, result in summary['results'].items():
            status_icon = {
                'PASS': '✅',
                'FAIL': '❌',
                'WARN': '⚠️',
                'ERROR': '🚨'
            }.get(result['status'], '❓')
            
            print(f"{status_icon} {test_name}: {result['status']}")
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
            print("🎉 모든 통합 테스트 통과! 프로젝트 준비 완료!")
        elif summary['overall_status'] == 'WARN':
            print("⚠️  경고 사항이 있지만 프로젝트는 준비되었습니다.")
        else:
            print("❌ 일부 테스트가 실패했습니다. 문제를 해결해 주세요.")

import os

async def main():
    """메인 함수"""
    tester = FinalIntegrationTester()
    summary = await tester.run_all_tests()
    tester.print_report(summary)
    
    # 결과를 파일로 저장
    with open("final_integration_test_results.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    # 종료 코드 설정
    if summary['overall_status'] == 'FAIL':
        sys.exit(1)
    elif summary['overall_status'] == 'WARN':
        sys.exit(2)
    else:
        sys.exit(0)

if __name__ == "__main__":
    import sys
    asyncio.run(main()) 