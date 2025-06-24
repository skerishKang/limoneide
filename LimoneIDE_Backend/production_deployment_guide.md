# 🍋 LimoneIDE 프로덕션 배포 가이드

## 📋 배포 전 체크리스트

### 1. 환경 설정 ✅
- [x] Python 3.10+ 설치
- [x] 가상환경 설정
- [x] 의존성 패키지 설치
- [x] 환경변수 설정

### 2. 보안 설정 ✅
- [x] API 키 환경변수 설정
- [x] .env 파일 .gitignore에 추가
- [x] CORS 설정 확인
- [x] 보안 헤더 설정

### 3. 성능 최적화 ✅
- [x] 성능 테스트 완료 (B+ 등급)
- [x] 캐싱 시스템 구현
- [x] 데이터베이스 최적화
- [x] 응답시간 최적화

### 4. 문서화 ✅
- [x] README.md 생성
- [x] 기술 백서 작성
- [x] API 문서 생성
- [x] 배포 가이드 작성

## 🚀 Google App Engine 배포

### 1. 사전 준비

```bash
# gcloud CLI 설치 확인
gcloud --version

# gcloud 인증
gcloud auth login

# 프로젝트 설정
gcloud config set project limoneide-project

# App Engine API 활성화
gcloud services enable appengine.googleapis.com
```

### 2. 배포 설정

```bash
# 배포 설정 확인
python production_readiness_check.py

# app.yaml 생성
python -c "from deployment_config import generate_app_yaml; generate_app_yaml()"
```

### 3. 배포 실행

```bash
# 자동 배포
python deploy.py

# 또는 수동 배포
gcloud app deploy --project limoneide-project --version v1.0.0 --promote
```

### 4. 배포 확인

```bash
# 서비스 상태 확인
gcloud app services list

# 버전 상태 확인
gcloud app versions list --service limoneide-backend

# 애플리케이션 URL 확인
gcloud app browse
```

## 🔧 환경별 설정

### 개발 환경
```yaml
# app-dev.yaml
runtime: python310
service: limoneide-backend-dev
instance_class: F1

env_variables:
  ENVIRONMENT: "development"
  LOG_LEVEL: "DEBUG"
  CACHE_TTL: "60"
```

### 스테이징 환경
```yaml
# app-staging.yaml
runtime: python310
service: limoneide-backend-staging
instance_class: F2

automatic_scaling:
  target_cpu_utilization: 0.7
  min_instances: 1
  max_instances: 5

env_variables:
  ENVIRONMENT: "staging"
  LOG_LEVEL: "INFO"
  CACHE_TTL: "300"
```

### 프로덕션 환경
```yaml
# app-prod.yaml
runtime: python310
service: limoneide-backend
instance_class: F2

automatic_scaling:
  target_cpu_utilization: 0.65
  min_instances: 2
  max_instances: 10

env_variables:
  ENVIRONMENT: "production"
  LOG_LEVEL: "WARNING"
  CACHE_TTL: "600"
```

## 📊 모니터링 및 로깅

### 1. Cloud Logging 설정

```python
import logging
from google.cloud import logging

# Cloud Logging 클라이언트 설정
client = logging.Client()
client.setup_logging()

# 로그 레벨 설정
logging.getLogger().setLevel(logging.INFO)
```

### 2. 성능 모니터링

```python
# Prometheus 메트릭 설정
from prometheus_client import Counter, Histogram, start_http_server

# 메트릭 정의
REQUEST_COUNT = Counter('limoneide_requests_total', 'Total requests')
REQUEST_DURATION = Histogram('limoneide_request_duration_seconds', 'Request duration')

# 메트릭 서버 시작
start_http_server(8001)
```

### 3. 알림 설정

```yaml
# alerting.yaml
alerts:
  - name: "high_error_rate"
    condition: "error_rate > 0.05"
    notification: "slack://webhook-url"
  
  - name: "high_response_time"
    condition: "response_time > 2.0"
    notification: "email://admin@limoneide.app"
```

## 🔄 CI/CD 파이프라인

### 1. GitHub Actions 설정

```yaml
# .github/workflows/deploy.yml
name: Deploy to App Engine

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python test_e2e.py
        python performance_test.py
    
    - name: Deploy to App Engine
      uses: google-github-actions/deploy-appengine@v1
      with:
        credentials: ${{ secrets.GCP_SA_KEY }}
        project_id: limoneide-project
```

### 2. 배포 단계

1. **코드 커밋** → GitHub 저장소
2. **자동 테스트** → E2E 테스트, 성능 테스트
3. **스테이징 배포** → 테스트 환경
4. **수동 검증** → QA 테스트
5. **프로덕션 배포** → 라이브 환경

## 🛡️ 보안 설정

### 1. IAM 권한 설정

```bash
# 서비스 계정 생성
gcloud iam service-accounts create limoneide-sa \
  --display-name="LimoneIDE Service Account"

# 필요한 권한 부여
gcloud projects add-iam-policy-binding limoneide-project \
  --member="serviceAccount:limoneide-sa@limoneide-project.iam.gserviceaccount.com" \
  --role="roles/appengine.deployer"

gcloud projects add-iam-policy-binding limoneide-project \
  --member="serviceAccount:limoneide-sa@limoneide-project.iam.gserviceaccount.com" \
  --role="roles/cloudsql.client"
```

### 2. 네트워크 보안

```yaml
# app.yaml
vpc_access_connector:
  name: "projects/limoneide-project/locations/us-central1/connectors/limoneide-vpc"

# 방화벽 규칙
gcloud compute firewall-rules create limoneide-allow-app \
  --allow tcp:8000 \
  --source-ranges 0.0.0.0/0 \
  --target-tags limoneide-app
```

## 📈 성능 최적화

### 1. 캐싱 전략

```python
# Redis 캐싱 설정
import redis
from functools import wraps

redis_client = redis.Redis(
    host='localhost',
    port=6379,
    db=0,
    decode_responses=True
)

def cache_result(expire_time=300):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            cached_result = redis_client.get(cache_key)
            
            if cached_result:
                return json.loads(cached_result)
            
            result = await func(*args, **kwargs)
            redis_client.setex(cache_key, expire_time, json.dumps(result))
            return result
        return wrapper
    return decorator
```

### 2. 데이터베이스 최적화

```python
# 연결 풀 설정
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)
```

## 🔍 문제 해결

### 일반적인 문제

1. **배포 실패**
   ```bash
   # 로그 확인
   gcloud app logs tail -s limoneide-backend
   
   # 버전 롤백
   gcloud app services set-traffic limoneide-backend --splits=v1.0.0=0
   ```

2. **성능 문제**
   ```bash
   # 인스턴스 상태 확인
   gcloud app instances list
   
   # 리소스 사용량 확인
   gcloud app describe
   ```

3. **데이터베이스 연결 문제**
   ```bash
   # Cloud SQL 연결 테스트
   python test_cloudsql.py
   
   # 연결 풀 상태 확인
   gcloud sql instances describe limoneide-sql
   ```

## 📞 지원 및 연락처

- **기술 지원**: tech-support@limoneide.app
- **운영 지원**: ops-support@limoneide.app
- **문서**: [기술 문서](docs/)
- **이슈 리포트**: [GitHub Issues](https://github.com/limoneide/issues)

---

**작성일**: 2025년 6월 25일  
**버전**: v1.0.0  
**담당자**: LimoneIDE DevOps Team 