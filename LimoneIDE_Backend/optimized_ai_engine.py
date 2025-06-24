#!/usr/bin/env python3
"""
🍋 LimoneIDE 최적화된 AI 엔진
성능 최적화 및 캐싱 시스템이 적용된 AI 엔진
"""

import os
import json
import asyncio
import logging
import time
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
from functools import lru_cache, wraps
import hashlib

# 성능 모니터링
from prometheus_client import Counter, Histogram, start_http_server

# AI 서비스 임포트
from .ai_openai import OpenAIService
from .ai_gemini import GeminiService
from .ai_claude import ClaudeService
from .ai_ollama import OllamaService

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('optimized_ai_engine')

# Prometheus 메트릭
REQUEST_COUNT = Counter('ai_engine_requests_total', 'Total AI engine requests', ['service'])
REQUEST_DURATION = Histogram('ai_engine_request_duration_seconds', 'AI request duration', ['service'])
CACHE_HIT_COUNT = Counter('ai_engine_cache_hits_total', 'Total cache hits')
CACHE_MISS_COUNT = Counter('ai_engine_cache_misses_total', 'Total cache misses')

class PerformanceLogger:
    """성능 로깅 클래스"""
    
    def __init__(self):
        self.logger = logging.getLogger('performance')
    
    def log_request(self, service: str, duration: float, success: bool, cache_hit: bool = False):
        """요청 성능 로깅"""
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'service': service,
            'duration': duration,
            'success': success,
            'cache_hit': cache_hit
        }
        self.logger.info(json.dumps(log_data))

class CacheManager:
    """캐시 관리 클래스"""
    
    def __init__(self):
        self.cache = {}
        self.max_size = 1000
        self.ttl = 300  # 5분
    
    def _generate_key(self, prompt: str, service: str, model: str) -> str:
        """캐시 키 생성"""
        content = f"{prompt}:{service}:{model}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def get(self, prompt: str, service: str, model: str) -> Optional[str]:
        """캐시에서 값 조회"""
        key = self._generate_key(prompt, service, model)
        
        if key in self.cache:
            cached_data = self.cache[key]
            if time.time() - cached_data['timestamp'] < self.ttl:
                CACHE_HIT_COUNT.inc()
                return cached_data['response']
            else:
                # TTL 만료
                del self.cache[key]
        
        CACHE_MISS_COUNT.inc()
        return None
    
    def set(self, prompt: str, service: str, model: str, response: str):
        """캐시에 값 저장"""
        key = self._generate_key(prompt, service, model)
        
        # 캐시 크기 제한
        if len(self.cache) >= self.max_size:
            # 가장 오래된 항목 제거
            oldest_key = min(self.cache.keys(), key=lambda k: self.cache[k]['timestamp'])
            del self.cache[oldest_key]
        
        self.cache[key] = {
            'response': response,
            'timestamp': time.time()
        }

def measure_performance(func):
    """성능 측정 데코레이터"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        service = kwargs.get('service', 'unknown')
        
        try:
            result = await func(*args, **kwargs)
            duration = time.time() - start_time
            REQUEST_COUNT.labels(service=service).inc()
            REQUEST_DURATION.labels(service=service).observe(duration)
            return result
        except Exception as e:
            duration = time.time() - start_time
            REQUEST_COUNT.labels(service=service).inc()
            REQUEST_DURATION.labels(service=service).observe(duration)
            raise e
    
    return wrapper

class OptimizedAIEngine:
    """
    최적화된 LimoneIDE AI 엔진
    - 캐싱 시스템
    - 병렬 처리
    - 성능 모니터링
    - 오류 처리
    """
    
    def __init__(self):
        """AI 엔진 초기화"""
        self.cache_manager = CacheManager()
        self.performance_logger = PerformanceLogger()
        
        # AI 서비스 초기화
        self.services = {
            "openai": OpenAIService(),
            "gemini": GeminiService(),
            "claude": ClaudeService(),
            "ollama": OllamaService()
        }
        
        # 기본 서비스 설정
        self.default_service = "gemini"  # 가장 빠른 서비스
        
        # 성능 메트릭 서버 시작
        try:
            start_http_server(8001)
            logger.info("Prometheus 메트릭 서버 시작: http://localhost:8001")
        except Exception as e:
            logger.warning(f"메트릭 서버 시작 실패: {e}")
    
    @measure_performance
    async def generate_response(self, prompt: str, service: str = None, model: str = None, use_cache: bool = True) -> str:
        """
        최적화된 AI 응답 생성
        
        Args:
            prompt: 사용자 입력 프롬프트
            service: 사용할 AI 서비스 (openai, gemini, claude, ollama)
            model: 사용할 모델명
            use_cache: 캐싱 사용 여부
            
        Returns:
            str: AI 응답
        """
        if service is None:
            service = self.default_service
        
        # 캐시 확인
        if use_cache:
            cached_response = self.cache_manager.get(prompt, service, model or "default")
            if cached_response:
                self.performance_logger.log_request(service, 0.0, True, cache_hit=True)
                return cached_response
        
        start_time = time.time()
        
        try:
            # AI 서비스 호출
            ai_service = self.services.get(service)
            if not ai_service:
                raise ValueError(f"지원하지 않는 AI 서비스: {service}")
            
            response = await ai_service.generate_response(prompt, model or "default")
            
            # 캐시 저장
            if use_cache:
                self.cache_manager.set(prompt, service, model or "default", response)
            
            duration = time.time() - start_time
            self.performance_logger.log_request(service, duration, True, cache_hit=False)
            
            return response
            
        except Exception as e:
            duration = time.time() - start_time
            self.performance_logger.log_request(service, duration, False, cache_hit=False)
            logger.error(f"AI 응답 생성 실패 ({service}): {e}")
            return f"죄송합니다. 응답 생성 중 오류가 발생했습니다: {str(e)}"
    
    @measure_performance
    async def generate_code(self, prompt: str, language: str = "python", service: str = None) -> str:
        """
        최적화된 코드 생성
        
        Args:
            prompt: 코드 생성 요청
            language: 프로그래밍 언어
            service: 사용할 AI 서비스
            
        Returns:
            str: 생성된 코드
        """
        if service is None:
            service = self.default_service
        
        # 코드 생성 전용 프롬프트
        code_prompt = f"다음 요청에 따라 {language} 코드를 생성해주세요. 코드만 응답하고 설명은 포함하지 마세요:\n\n{prompt}"
        
        return await self.generate_response(code_prompt, service, use_cache=True)
    
    @measure_performance
    async def batch_generate_responses(self, prompts: List[str], service: str = None) -> List[str]:
        """
        배치 처리로 여러 응답 생성
        
        Args:
            prompts: 프롬프트 목록
            service: 사용할 AI 서비스
            
        Returns:
            List[str]: 응답 목록
        """
        if service is None:
            service = self.default_service
        
        # 병렬 처리로 여러 요청 동시 실행
        tasks = [self.generate_response(prompt, service) for prompt in prompts]
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 예외 처리
        processed_responses = []
        for i, response in enumerate(responses):
            if isinstance(response, Exception):
                logger.error(f"배치 처리 중 오류 (프롬프트 {i}): {response}")
                processed_responses.append(f"오류 발생: {str(response)}")
            else:
                processed_responses.append(response)
        
        return processed_responses
    
    async def get_available_models(self) -> Dict[str, List[str]]:
        """
        사용 가능한 모델 목록 반환
        """
        models = {}
        for service_name, service in self.services.items():
            try:
                if hasattr(service, 'get_available_models'):
                    models[service_name] = await service.get_available_models()
                else:
                    models[service_name] = ["default"]
            except Exception as e:
                logger.error(f"모델 목록 조회 실패 ({service_name}): {e}")
                models[service_name] = []
        
        return models
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """
        성능 통계 반환
        """
        return {
            "cache_hits": CACHE_HIT_COUNT._value.get(),
            "cache_misses": CACHE_MISS_COUNT._value.get(),
            "cache_hit_rate": CACHE_HIT_COUNT._value.get() / (CACHE_HIT_COUNT._value.get() + CACHE_MISS_COUNT._value.get()) if (CACHE_HIT_COUNT._value.get() + CACHE_MISS_COUNT._value.get()) > 0 else 0,
            "total_requests": sum(REQUEST_COUNT._metrics.values()),
            "cache_size": len(self.cache_manager.cache),
            "timestamp": datetime.now().isoformat()
        }
    
    def clear_cache(self):
        """캐시 초기화"""
        self.cache_manager.cache.clear()
        logger.info("AI 엔진 캐시 초기화 완료")
    
    async def health_check(self) -> Dict[str, Any]:
        """
        AI 엔진 상태 확인
        """
        health_status = {
            "status": "healthy",
            "services": {},
            "cache": {
                "size": len(self.cache_manager.cache),
                "max_size": self.cache_manager.max_size
            },
            "performance": self.get_performance_stats(),
            "timestamp": datetime.now().isoformat()
        }
        
        # 각 서비스 상태 확인
        for service_name, service in self.services.items():
            try:
                if hasattr(service, 'is_available'):
                    health_status["services"][service_name] = {
                        "available": service.is_available(),
                        "status": "healthy" if service.is_available() else "unavailable"
                    }
                else:
                    health_status["services"][service_name] = {
                        "available": True,
                        "status": "unknown"
                    }
            except Exception as e:
                health_status["services"][service_name] = {
                    "available": False,
                    "status": f"error: {str(e)}"
                }
        
        return health_status

# 전역 인스턴스
optimized_ai_engine = OptimizedAIEngine()

# 편의 함수들
async def generate_ai_response(prompt: str, service: str = None) -> str:
    """AI 응답 생성 (편의 함수)"""
    return await optimized_ai_engine.generate_response(prompt, service)

async def generate_code(prompt: str, language: str = "python", service: str = None) -> str:
    """코드 생성 (편의 함수)"""
    return await optimized_ai_engine.generate_code(prompt, language, service)

async def get_ai_health() -> Dict[str, Any]:
    """AI 엔진 상태 확인 (편의 함수)"""
    return await optimized_ai_engine.health_check() 