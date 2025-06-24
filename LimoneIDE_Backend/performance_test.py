#!/usr/bin/env python3
"""
🍋 LimoneIDE 성능 테스트 스크립트
최적화 전후 성능 비교 및 부하 테스트
"""

import asyncio
import time
import json
import statistics
from typing import List, Dict, Any
import logging
import requests
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('performance_test')

class PerformanceTester:
    """성능 테스트 클래스"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.results = []
        
    async def test_single_request(self, endpoint: str, method: str = "GET", data: Dict = None) -> Dict[str, Any]:
        """단일 요청 테스트"""
        start_time = time.time()
        
        try:
            if method.upper() == "GET":
                response = requests.get(f"{self.base_url}{endpoint}", timeout=30)
            elif method.upper() == "POST":
                response = requests.post(f"{self.base_url}{endpoint}", json=data, timeout=30)
            else:
                raise ValueError(f"지원하지 않는 HTTP 메서드: {method}")
            
            duration = time.time() - start_time
            
            return {
                "endpoint": endpoint,
                "method": method,
                "duration": duration,
                "status_code": response.status_code,
                "success": response.status_code < 400,
                "timestamp": time.time()
            }
            
        except Exception as e:
            duration = time.time() - start_time
            return {
                "endpoint": endpoint,
                "method": method,
                "duration": duration,
                "status_code": 0,
                "success": False,
                "error": str(e),
                "timestamp": time.time()
            }
    
    async def test_endpoint_performance(self, endpoint: str, method: str = "GET", data: Dict = None, iterations: int = 10) -> Dict[str, Any]:
        """엔드포인트 성능 테스트 (여러 번 실행)"""
        logger.info(f"엔드포인트 성능 테스트 시작: {method} {endpoint}")
        
        durations = []
        success_count = 0
        error_count = 0
        
        for i in range(iterations):
            result = await self.test_single_request(endpoint, method, data)
            durations.append(result["duration"])
            
            if result["success"]:
                success_count += 1
            else:
                error_count += 1
                logger.warning(f"요청 실패 ({i+1}/{iterations}): {result.get('error', 'Unknown error')}")
        
        # 통계 계산
        if durations:
            stats = {
                "endpoint": endpoint,
                "method": method,
                "iterations": iterations,
                "success_count": success_count,
                "error_count": error_count,
                "success_rate": success_count / iterations,
                "min_duration": min(durations),
                "max_duration": max(durations),
                "avg_duration": statistics.mean(durations),
                "median_duration": statistics.median(durations),
                "std_duration": statistics.stdev(durations) if len(durations) > 1 else 0,
                "p95_duration": np.percentile(durations, 95),
                "p99_duration": np.percentile(durations, 99),
                "durations": durations
            }
        else:
            stats = {
                "endpoint": endpoint,
                "method": method,
                "iterations": iterations,
                "success_count": 0,
                "error_count": error_count,
                "success_rate": 0,
                "error": "모든 요청 실패"
            }
        
        logger.info(f"성능 테스트 완료: {endpoint} - 평균 {stats.get('avg_duration', 0):.3f}초, 성공률 {stats.get('success_rate', 0)*100:.1f}%")
        return stats
    
    async def test_concurrent_requests(self, endpoint: str, method: str = "GET", data: Dict = None, concurrent_users: int = 10) -> Dict[str, Any]:
        """동시 요청 테스트"""
        logger.info(f"동시 요청 테스트 시작: {concurrent_users}명의 사용자, {method} {endpoint}")
        
        start_time = time.time()
        
        # 동시 요청 실행
        with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            futures = []
            for i in range(concurrent_users):
                future = executor.submit(asyncio.run, self.test_single_request(endpoint, method, data))
                futures.append(future)
            
            # 결과 수집
            results = []
            for future in futures:
                try:
                    result = future.result(timeout=60)
                    results.append(result)
                except Exception as e:
                    results.append({
                        "endpoint": endpoint,
                        "method": method,
                        "duration": 60,
                        "status_code": 0,
                        "success": False,
                        "error": str(e),
                        "timestamp": time.time()
                    })
        
        total_duration = time.time() - start_time
        durations = [r["duration"] for r in results]
        success_count = sum(1 for r in results if r["success"])
        
        stats = {
            "endpoint": endpoint,
            "method": method,
            "concurrent_users": concurrent_users,
            "total_duration": total_duration,
            "success_count": success_count,
            "error_count": len(results) - success_count,
            "success_rate": success_count / len(results),
            "requests_per_second": len(results) / total_duration,
            "min_duration": min(durations) if durations else 0,
            "max_duration": max(durations) if durations else 0,
            "avg_duration": statistics.mean(durations) if durations else 0,
            "median_duration": statistics.median(durations) if durations else 0,
            "p95_duration": np.percentile(durations, 95) if durations else 0,
            "p99_duration": np.percentile(durations, 99) if durations else 0
        }
        
        logger.info(f"동시 요청 테스트 완료: {endpoint} - RPS {stats['requests_per_second']:.2f}, 성공률 {stats['success_rate']*100:.1f}%")
        return stats
    
    async def run_comprehensive_test(self) -> Dict[str, Any]:
        """종합 성능 테스트 실행"""
        logger.info("종합 성능 테스트 시작")
        
        test_scenarios = [
            # 기본 기능 테스트
            {"endpoint": "/health", "method": "GET", "iterations": 20},
            {"endpoint": "/api/health/db", "method": "GET", "iterations": 20},
            {"endpoint": "/auth/session", "method": "GET", "iterations": 20},
            
            # API 기능 테스트
            {"endpoint": "/api/projects", "method": "POST", "data": {"name": "Test Project", "description": "Performance Test"}, "iterations": 10},
            {"endpoint": "/api/voice/process", "method": "POST", "data": {"command": "테스트 명령", "language": "ko"}, "iterations": 10},
            {"endpoint": "/api/ai/generate", "method": "POST", "data": {"command": "간단한 웹사이트 만들어줘", "template": "general"}, "iterations": 10},
            {"endpoint": "/api/deploy/start", "method": "POST", "data": {"project_id": "test-project", "template": "general"}, "iterations": 10},
            {"endpoint": "/api/cloudsql/test-connection", "method": "POST", "data": {"instance_name": "test-instance"}, "iterations": 10},
            {"endpoint": "/api/templates/blog", "method": "POST", "data": {"command": "블로그 만들어줘", "features": ["blog_posts", "guestbook"]}, "iterations": 10},
            {"endpoint": "/api/guestbook", "method": "GET", "iterations": 20},
            {"endpoint": "/api/stats", "method": "GET", "iterations": 20},
        ]
        
        results = {}
        
        # 단일 요청 성능 테스트
        for scenario in test_scenarios:
            endpoint = scenario["endpoint"]
            method = scenario["method"]
            data = scenario.get("data")
            iterations = scenario["iterations"]
            
            result = await self.test_endpoint_performance(endpoint, method, data, iterations)
            results[endpoint] = result
        
        # 동시 요청 테스트 (부하 테스트)
        load_test_scenarios = [
            {"endpoint": "/health", "method": "GET", "concurrent_users": 50},
            {"endpoint": "/api/guestbook", "method": "GET", "concurrent_users": 30},
            {"endpoint": "/api/stats", "method": "GET", "concurrent_users": 20},
        ]
        
        load_results = {}
        for scenario in load_test_scenarios:
            endpoint = scenario["endpoint"]
            method = scenario["method"]
            data = scenario.get("data")
            concurrent_users = scenario["concurrent_users"]
            
            result = await self.test_concurrent_requests(endpoint, method, data, concurrent_users)
            load_results[f"{endpoint}_load_test"] = result
        
        # 종합 결과
        comprehensive_result = {
            "timestamp": time.time(),
            "test_duration": time.time() - time.time(),
            "single_request_tests": results,
            "load_tests": load_results,
            "summary": self._generate_summary(results, load_results)
        }
        
        logger.info("종합 성능 테스트 완료")
        return comprehensive_result
    
    def _generate_summary(self, single_results: Dict, load_results: Dict) -> Dict[str, Any]:
        """테스트 결과 요약 생성"""
        # 단일 요청 통계
        single_durations = []
        single_success_rates = []
        
        for result in single_results.values():
            if "avg_duration" in result:
                single_durations.append(result["avg_duration"])
            if "success_rate" in result:
                single_success_rates.append(result["success_rate"])
        
        # 부하 테스트 통계
        load_rps = []
        load_success_rates = []
        
        for result in load_results.values():
            if "requests_per_second" in result:
                load_rps.append(result["requests_per_second"])
            if "success_rate" in result:
                load_success_rates.append(result["success_rate"])
        
        summary = {
            "single_request": {
                "avg_response_time": statistics.mean(single_durations) if single_durations else 0,
                "min_response_time": min(single_durations) if single_durations else 0,
                "max_response_time": max(single_durations) if single_durations else 0,
                "avg_success_rate": statistics.mean(single_success_rates) if single_success_rates else 0,
                "total_endpoints_tested": len(single_results)
            },
            "load_test": {
                "avg_requests_per_second": statistics.mean(load_rps) if load_rps else 0,
                "max_requests_per_second": max(load_rps) if load_rps else 0,
                "avg_success_rate": statistics.mean(load_success_rates) if load_success_rates else 0,
                "total_load_tests": len(load_results)
            },
            "performance_grade": self._calculate_performance_grade(single_durations, load_rps, single_success_rates)
        }
        
        return summary
    
    def _calculate_performance_grade(self, durations: List[float], rps: List[float], success_rates: List[float]) -> str:
        """성능 등급 계산"""
        if not durations or not rps or not success_rates:
            return "F"
        
        avg_duration = statistics.mean(durations)
        avg_rps = statistics.mean(rps)
        avg_success_rate = statistics.mean(success_rates)
        
        # 점수 계산 (100점 만점)
        duration_score = max(0, 100 - (avg_duration - 1) * 50)  # 1초 이하: 100점, 3초: 0점
        rps_score = min(100, avg_rps * 10)  # 10 RPS: 100점
        success_score = avg_success_rate * 100
        
        total_score = (duration_score * 0.4 + rps_score * 0.3 + success_score * 0.3)
        
        # 등급 결정
        if total_score >= 90:
            return "A+"
        elif total_score >= 80:
            return "A"
        elif total_score >= 70:
            return "B+"
        elif total_score >= 60:
            return "B"
        elif total_score >= 50:
            return "C+"
        elif total_score >= 40:
            return "C"
        else:
            return "F"
    
    def save_results(self, results: Dict[str, Any], filename: str = "performance_test_results.json"):
        """테스트 결과 저장"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        logger.info(f"테스트 결과 저장: {filename}")
    
    def generate_report(self, results: Dict[str, Any], filename: str = "performance_test_report.md"):
        """성능 테스트 리포트 생성"""
        summary = results.get("summary", {})
        
        report = f"""# 🍋 LimoneIDE 성능 테스트 리포트

## 📊 테스트 개요
- **테스트 일시**: {datetime.fromtimestamp(results.get('timestamp', time.time())).strftime('%Y-%m-%d %H:%M:%S')}
- **총 테스트 시간**: {results.get('test_duration', 0):.2f}초
- **성능 등급**: {summary.get('performance_grade', 'N/A')}

## 📈 단일 요청 성능
- **평균 응답시간**: {summary.get('single_request', {}).get('avg_response_time', 0):.3f}초
- **최소 응답시간**: {summary.get('single_request', {}).get('min_response_time', 0):.3f}초
- **최대 응답시간**: {summary.get('single_request', {}).get('max_response_time', 0):.3f}초
- **평균 성공률**: {summary.get('single_request', {}).get('avg_success_rate', 0)*100:.1f}%
- **테스트 엔드포인트 수**: {summary.get('single_request', {}).get('total_endpoints_tested', 0)}개

## 🚀 부하 테스트 성능
- **평균 처리량**: {summary.get('load_test', {}).get('avg_requests_per_second', 0):.2f} RPS
- **최대 처리량**: {summary.get('load_test', {}).get('max_requests_per_second', 0):.2f} RPS
- **평균 성공률**: {summary.get('load_test', {}).get('avg_success_rate', 0)*100:.1f}%
- **부하 테스트 수**: {summary.get('load_test', {}).get('total_load_tests', 0)}개

## 📋 상세 결과

### 단일 요청 테스트
"""
        
        for endpoint, result in results.get("single_request_tests", {}).items():
            report += f"""
#### {endpoint}
- **메서드**: {result.get('method', 'N/A')}
- **평균 응답시간**: {result.get('avg_duration', 0):.3f}초
- **성공률**: {result.get('success_rate', 0)*100:.1f}%
- **테스트 횟수**: {result.get('iterations', 0)}회
"""
        
        report += """
### 부하 테스트
"""
        
        for test_name, result in results.get("load_tests", {}).items():
            report += f"""
#### {test_name}
- **동시 사용자**: {result.get('concurrent_users', 0)}명
- **처리량**: {result.get('requests_per_second', 0):.2f} RPS
- **성공률**: {result.get('success_rate', 0)*100:.1f}%
- **평균 응답시간**: {result.get('avg_duration', 0):.3f}초
"""
        
        report += f"""
## 🎯 권장사항

### 성능 개선 우선순위
1. **응답시간 개선**: 목표 1초 이하
2. **처리량 향상**: 목표 100 RPS 이상
3. **성공률 유지**: 99% 이상

### 최적화 방안
- 캐싱 시스템 도입
- 데이터베이스 쿼리 최적화
- 비동기 처리 개선
- 리소스 사용량 최적화

---
**생성일**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**테스트 도구**: LimoneIDE Performance Tester
"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"성능 테스트 리포트 생성: {filename}")

async def main():
    """메인 함수"""
    logger.info("🍋 LimoneIDE 성능 테스트 시작")
    
    # 성능 테스터 초기화
    tester = PerformanceTester()
    
    try:
        # 종합 성능 테스트 실행
        results = await tester.run_comprehensive_test()
        
        # 결과 저장
        tester.save_results(results, "performance_test_results.json")
        tester.generate_report(results, "performance_test_report.md")
        
        # 결과 요약 출력
        summary = results.get("summary", {})
        logger.info("=" * 50)
        logger.info("성능 테스트 완료!")
        logger.info(f"성능 등급: {summary.get('performance_grade', 'N/A')}")
        logger.info(f"평균 응답시간: {summary.get('single_request', {}).get('avg_response_time', 0):.3f}초")
        logger.info(f"평균 처리량: {summary.get('load_test', {}).get('avg_requests_per_second', 0):.2f} RPS")
        logger.info(f"평균 성공률: {summary.get('single_request', {}).get('avg_success_rate', 0)*100:.1f}%")
        logger.info("=" * 50)
        
    except Exception as e:
        logger.error(f"성능 테스트 중 오류 발생: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main()) 