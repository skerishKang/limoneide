#!/usr/bin/env python3
"""
🍋 LimoneIDE 배포 설정 관리
Google App Engine 배포를 위한 설정 및 환경 관리
"""

import os
import json
import logging
from typing import Dict, Any, Optional
from pathlib import Path

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('deployment_config')

class DeploymentConfig:
    """배포 설정 관리 클래스"""
    
    def __init__(self, config_path: str = "deployment_config.json"):
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """설정 파일 로드"""
        default_config = {
            "environment": "development",
            "google_cloud": {
                "project_id": "limoneide-project",
                "region": "us-central1",
                "zone": "us-central1-a"
            },
            "app_engine": {
                "service": "limoneide-backend",
                "version": "v1.0.0",
                "runtime": "python310",
                "instance_class": "F1",
                "automatic_scaling": {
                    "target_cpu_utilization": 0.65,
                    "min_instances": 1,
                    "max_instances": 10
                }
            },
            "database": {
                "cloud_sql_instance": "limoneide-sql",
                "database_name": "limoneide_db",
                "connection_pool_size": 10
            },
            "ai_services": {
                "openai": {
                    "enabled": True,
                    "model": "gpt-4"
                },
                "gemini": {
                    "enabled": True,
                    "model": "gemini-pro"
                },
                "claude": {
                    "enabled": True,
                    "model": "claude-3-sonnet"
                },
                "ollama": {
                    "enabled": False,
                    "model": "llama2"
                }
            },
            "performance": {
                "cache_enabled": True,
                "cache_ttl": 300,
                "max_concurrent_requests": 100,
                "response_timeout": 30
            },
            "security": {
                "cors_enabled": True,
                "allowed_origins": ["https://limoneide.app", "https://www.limoneide.app"],
                "rate_limiting": {
                    "enabled": True,
                    "requests_per_minute": 100
                }
            },
            "monitoring": {
                "prometheus_enabled": True,
                "logging_level": "INFO",
                "health_check_interval": 60
            }
        }
        
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    # 기본 설정과 병합
                    default_config.update(loaded_config)
                    logger.info(f"설정 파일 로드: {self.config_path}")
            except Exception as e:
                logger.warning(f"설정 파일 로드 실패, 기본값 사용: {e}")
        else:
            logger.info("설정 파일이 없어 기본값 사용")
        
        return default_config
    
    def save_config(self):
        """설정 파일 저장"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            logger.info(f"설정 파일 저장: {self.config_path}")
        except Exception as e:
            logger.error(f"설정 파일 저장 실패: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """설정값 조회"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """설정값 설정"""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        logger.info(f"설정 업데이트: {key} = {value}")
    
    def get_environment_config(self, environment: str = None) -> Dict[str, Any]:
        """환경별 설정 반환"""
        if environment is None:
            environment = self.get("environment", "development")
        
        env_config = {
            "development": {
                "debug": True,
                "log_level": "DEBUG",
                "cache_enabled": False,
                "database": {
                    "url": "sqlite:///limoneide_dev.db"
                }
            },
            "staging": {
                "debug": False,
                "log_level": "INFO",
                "cache_enabled": True,
                "database": {
                    "url": "postgresql://user:pass@staging-db/limoneide_staging"
                }
            },
            "production": {
                "debug": False,
                "log_level": "WARNING",
                "cache_enabled": True,
                "database": {
                    "url": "postgresql://user:pass@prod-db/limoneide_prod"
                }
            }
        }
        
        return env_config.get(environment, env_config["development"])
    
    def generate_app_yaml(self, output_path: str = "app.yaml") -> str:
        """App Engine app.yaml 파일 생성"""
        app_config = self.get("app_engine", {})
        
        yaml_content = f"""runtime: {app_config.get('runtime', 'python310')}
service: {app_config.get('service', 'limoneide-backend')}

instance_class: {app_config.get('instance_class', 'F1')}

automatic_scaling:
  target_cpu_utilization: {app_config.get('automatic_scaling', {}).get('target_cpu_utilization', 0.65)}
  min_instances: {app_config.get('automatic_scaling', {}).get('min_instances', 1)}
  max_instances: {app_config.get('automatic_scaling', {}).get('max_instances', 10)}
  target_throughput_utilization: 0.6

env_variables:
  ENVIRONMENT: "{self.get('environment', 'development')}"
  LOG_LEVEL: "{self.get('monitoring.logging_level', 'INFO')}"
  CACHE_TTL: "{self.get('performance.cache_ttl', 300)}"
  MAX_CONCURRENT_REQUESTS: "{self.get('performance.max_concurrent_requests', 100)}"

handlers:
  - url: /static
    static_dir: static
    secure: always

  - url: /api/.*
    script: auto
    secure: always

  - url: /.*
    script: auto
    secure: always

inbound_services:
  - warmup

basic_scaling:
  max_instances: {app_config.get('automatic_scaling', {}).get('max_instances', 10)}
  idle_timeout: 10m

resources:
  cpu: 1
  memory_gb: 0.5
  disk_size_gb: 10

beta_settings:
  cloud_sql_instances: "{self.get('google_cloud.project_id', 'limoneide-project')}:{self.get('google_cloud.region', 'us-central1')}:{self.get('database.cloud_sql_instance', 'limoneide-sql')}"

vpc_access_connector:
  name: "projects/{self.get('google_cloud.project_id', 'limoneide-project')}/locations/{self.get('google_cloud.region', 'us-central1')}/connectors/limoneide-vpc"
"""
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(yaml_content)
            logger.info(f"app.yaml 파일 생성: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"app.yaml 파일 생성 실패: {e}")
            return ""
    
    def validate_config(self) -> Dict[str, Any]:
        """설정 유효성 검사"""
        errors = []
        warnings = []
        
        # 필수 설정 검사
        required_fields = [
            "google_cloud.project_id",
            "app_engine.service",
            "database.cloud_sql_instance"
        ]
        
        for field in required_fields:
            if not self.get(field):
                errors.append(f"필수 설정 누락: {field}")
        
        # 성능 설정 검사
        cache_ttl = self.get("performance.cache_ttl", 300)
        if cache_ttl < 60:
            warnings.append("캐시 TTL이 너무 짧습니다 (60초 이상 권장)")
        
        max_requests = self.get("performance.max_concurrent_requests", 100)
        if max_requests > 1000:
            warnings.append("최대 동시 요청 수가 너무 높습니다 (1000 이하 권장)")
        
        # AI 서비스 설정 검사
        ai_services = self.get("ai_services", {})
        enabled_services = [service for service, config in ai_services.items() if config.get("enabled", False)]
        
        if not enabled_services:
            errors.append("최소 하나의 AI 서비스가 활성화되어야 합니다")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }
    
    def get_deployment_summary(self) -> Dict[str, Any]:
        """배포 요약 정보 반환"""
        validation = self.validate_config()
        
        return {
            "environment": self.get("environment", "development"),
            "project_id": self.get("google_cloud.project_id"),
            "service": self.get("app_engine.service"),
            "version": self.get("app_engine.version"),
            "runtime": self.get("app_engine.runtime"),
            "ai_services": [service for service, config in self.get("ai_services", {}).items() if config.get("enabled", False)],
            "performance": {
                "cache_enabled": self.get("performance.cache_enabled", False),
                "max_concurrent_requests": self.get("performance.max_concurrent_requests", 100)
            },
            "validation": validation
        }

# 전역 인스턴스
deployment_config = DeploymentConfig()

# 편의 함수들
def get_config(key: str, default: Any = None) -> Any:
    """설정값 조회 (편의 함수)"""
    return deployment_config.get(key, default)

def set_config(key: str, value: Any):
    """설정값 설정 (편의 함수)"""
    deployment_config.set(key, value)

def validate_deployment_config() -> Dict[str, Any]:
    """배포 설정 유효성 검사 (편의 함수)"""
    return deployment_config.validate_config()

def generate_app_yaml(output_path: str = "app.yaml") -> str:
    """App Engine app.yaml 생성 (편의 함수)"""
    return deployment_config.generate_app_yaml(output_path) 