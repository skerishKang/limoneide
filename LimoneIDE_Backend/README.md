# 🍋 LimoneIDE

AI 기반 웹사이트 자동 생성 및 배포 플랫폼

## 📋 프로젝트 개요

LimoneIDE는 사용자의 자연어 명령을 통해 웹사이트를 자동으로 생성하고 Google Cloud Platform에 배포하는 AI 기반 플랫폼입니다.

## ✨ 주요 기능

- 🤖 **AI 기반 웹사이트 생성**: OpenAI, Google Gemini, Anthropic Claude, Ollama 지원
- 🎨 **다양한 템플릿**: 블로그, 이커머스, 포트폴리오, 랜딩 페이지 등
- 🗣️ **음성 명령 지원**: 음성으로 웹사이트 생성 요청
- ☁️ **자동 배포**: Google App Engine 자동 배포
- 🗄️ **데이터베이스 관리**: Cloud SQL 자동 프로비저닝
- 📊 **성능 모니터링**: 실시간 성능 추적 및 최적화

## 🚀 빠른 시작

### 1. 환경 설정

```bash
# 저장소 클론
git clone https://github.com/your-username/LimoneIDE.git
cd LimoneIDE/LimoneIDE_Backend

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

### 2. 환경변수 설정

`.env` 파일을 생성하고 다음 변수들을 설정하세요:

```env
# Google Cloud
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json

# AI 서비스 API 키
OPENAI_API_KEY=your-openai-api-key
GEMINI_API_KEY=your-gemini-api-key
CLAUDE_API_KEY=your-claude-api-key

# 데이터베이스
DATABASE_URL=sqlite:///limoneide.db

# 기타 설정
ENVIRONMENT=development
LOG_LEVEL=INFO
```

### 3. 서버 실행

```bash
# 개발 서버 실행
python main.py

# 또는 uvicorn으로 실행
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4. API 사용 예시

```python
import requests

# 웹사이트 생성 요청
response = requests.post("http://localhost:8000/api/ai/generate", json={
    "command": "블로그 웹사이트를 만들어줘",
    "template": "blog",
    "features": ["blog_posts", "guestbook"]
})

print(response.json())
```

## 📁 프로젝트 구조

```
LimoneIDE_Backend/
├── src/
│   ├── core/              # AI 엔진 및 핵심 기능
│   ├── automation/        # 자동화 및 배포
│   ├── templates/         # 웹사이트 템플릿
│   ├── voice/            # 음성 처리
│   └── rag/              # RAG 시스템
├── docs/                 # 기술 문서
├── tests/                # 테스트 파일
├── main.py              # 메인 애플리케이션
├── requirements.txt     # Python 의존성
└── app.yaml            # App Engine 설정
```

## 🛠️ 기술 스택

### 백엔드
- **언어**: Python 3.10+
- **프레임워크**: FastAPI
- **AI 서비스**: OpenAI, Google Gemini, Anthropic Claude, Ollama
- **데이터베이스**: SQLite (개발), Cloud SQL (프로덕션)
- **캐싱**: Redis
- **모니터링**: Prometheus

### 프론트엔드
- **언어**: TypeScript, React Native
- **PWA**: HTML5, CSS3, JavaScript
- **UI 프레임워크**: React Native Elements

### 클라우드 서비스
- **플랫폼**: Google Cloud Platform
- **컨테이너**: Google App Engine
- **데이터베이스**: Cloud SQL
- **스토리지**: Cloud Storage

## 📊 성능 지표

- **응답시간**: 평균 2.04초
- **처리량**: 15.5 RPS
- **성공률**: 90.9%
- **성능 등급**: B+

## 🔧 개발 가이드

### 새로운 템플릿 추가

1. `src/templates/` 디렉토리에 새 템플릿 파일 생성
2. `TemplateBase` 클래스 상속
3. `generate()` 메서드 구현
4. 템플릿 등록

### AI 서비스 확장

1. `src/core/` 디렉토리에 새 AI 서비스 파일 생성
2. `AIServiceBase` 클래스 상속
3. `generate_response()` 메서드 구현
4. AI 엔진에 등록

### 배포 설정

```bash
# 프로덕션 배포 준비 확인
python production_readiness_check.py

# App Engine 배포
python deploy.py
```

## 🧪 테스트

```bash
# 단위 테스트
python -m pytest tests/

# E2E 테스트
python test_e2e.py

# 성능 테스트
python performance_test.py
```

## 📈 모니터링

- **Prometheus 메트릭**: http://localhost:8001/metrics
- **성능 대시보드**: 성능 테스트 리포트 참조
- **로그**: `logs/` 디렉토리

## 🤝 기여하기

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 📞 지원

- **이슈 리포트**: [GitHub Issues](https://github.com/your-username/LimoneIDE/issues)
- **문서**: [기술 백서](docs/technical_whitepaper.md)
- **성능 리포트**: [성능 테스트 리포트](performance_test_report.md)

## 🏆 성과

- **Sprint 3 완료**: 100%
- **성능 최적화**: B+ 등급 달성
- **E2E 테스트**: 90% 성공률
- **문서화**: 완료

---

**개발팀**: LimoneIDE Development Team  
**최종 업데이트**: 2025년 6월 25일  
**버전**: v1.0.0 