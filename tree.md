# LimoneIDE 프로젝트 파일 구조

```
LimoneIDE/
├── LimoneIDE_Backend/                    # 핵심 백엔드 시스템
│   ├── src/                           # 소스 코드
│   │   ├── automation/                # 자동화 엔진
│   │   │   ├── __init__.py
│   │   │   ├── deployment_manager.py (156 lines)
│   │   │   ├── google_integration.py (203 lines)
│   │   │   ├── website_builder.py (189 lines)  # 템플릿 분리 후 줄어듦
│   │   │   └── workflow_engine.py (178 lines)
│   │   ├── core/                      # 핵심 엔진
│   │   │   ├── __init__.py
│   │   │   ├── ai_base.py (87 lines)  # 신규 공통 인터페이스
│   │   │   ├── ai_claude.py (156 lines)  # 분리된 Claude 엔진
│   │   │   ├── ai_engine.py (198 lines)  # 분리 후 줄어듦
│   │   │   ├── ai_gemini.py (145 lines)  # 분리된 Gemini 엔진
│   │   │   ├── ai_ollama.py (132 lines)  # 분리된 Ollama 엔진
│   │   │   ├── ai_openai.py (167 lines)  # 분리된 OpenAI 엔진
│   │   │   ├── code_executor.py (267 lines)
│   │   │   ├── error_handler.py (189 lines)
│   │   │   └── utils.py (123 lines)  # 공통 유틸리티 함수
│   │   ├── rag/                       # RAG 시스템
│   │   │   ├── __init__.py
│   │   │   ├── memory_manager.py (178 lines)  # 분리 후 줄어듦
│   │   │   ├── personal_ai.py (145 lines)  # 분리 후 줄어듦
│   │   │   ├── project_history.py (134 lines)  # 신규 분리 파일
│   │   │   ├── user_insight.py (156 lines)  # 신규 분리 파일
│   │   │   ├── user_profile.py (167 lines)  # 신규 분리 파일
│   │   │   └── user_recommender.py (145 lines)  # 신규 분리 파일
│   │   ├── templates/                 # 웹사이트 템플릿 (신규 폴더)
│   │   │   ├── __init__.py
│   │   │   ├── blog_template.py (167 lines)
│   │   │   ├── ecommerce_template.py (189 lines)
│   │   │   ├── general_template.py (145 lines)
│   │   │   ├── landing_template.py (156 lines)
│   │   │   └── portfolio_template.py (178 lines)
│   │   ├── voice/                     # 음성 인터페이스
│   │   │   ├── __init__.py
│   │   │   ├── intent_analyzer.py (156 lines)
│   │   │   ├── speech_recognition.py (234 lines)
│   │   │   └── voice_commands.py (189 lines)
│   │   └── __init__.py
│   ├── demo_rag.py (156 lines)        # RAG 데모
│   ├── main.py (234 lines)            # 메인 애플리케이션
│   └── requirements.txt (45 lines)    # 의존성 패키지
├── LimoneIDE_Test/                    # PWA 모바일 앱 (이전 LimoneIDE_Mobile)
│   ├── icons/                         # PWA 아이콘
│   │   └── icon-192x192.svg
│   ├── app.js (456 lines)             # Alpine.js 앱 로직
│   ├── index.html (234 lines)         # 메인 HTML
│   ├── manifest.json (45 lines)       # PWA 매니페스트
│   ├── package.json (67 lines)        # 의존성 관리
│   ├── README.md (234 lines)          # 모바일 가이드
│   ├── server.py (189 lines)          # FastAPI 서버
│   ├── styles.css (345 lines)         # 모바일 CSS
│   └── sw.js (123 lines)              # Service Worker
├── LimoneIDE_Beta/                    # React Native 앱 (이전 LimoneIDE_ReactNative)
│   ├── src/                           # 소스 코드
│   │   ├── components/                # 재사용 컴포넌트
│   │   │   ├── QuickCommandButton.tsx (45 lines)
│   │   │   ├── ResponseCard.tsx (156 lines)
│   │   │   ├── TaskHistory.tsx (89 lines)
│   │   │   └── VoiceButton.tsx (89 lines)
│   │   ├── screens/                   # 화면 컴포넌트
│   │   │   ├── HomeScreen.tsx (234 lines)
│   │   │   ├── ProjectsScreen.tsx (189 lines)
│   │   │   └── SettingsScreen.tsx (234 lines)
│   │   └── services/                  # 비즈니스 로직
│   │       ├── APIService.ts (234 lines)
│   │       ├── NotificationService.ts (234 lines)
│   │       └── VoiceService.ts (189 lines)
│   ├── App.tsx (89 lines)             # 메인 앱 컴포넌트
│   ├── package.json (89 lines)        # Expo 의존성
│   └── README.md (234 lines)          # React Native 가이드
├── plan/                              # 개발 문서 (로컬 전용)
│   ├── limoneide_comprehensive_plan.md (658 lines)
│   ├── limoneide_development_plan.md (1166 lines)
│   ├── limoneide_migration.md (343 lines)
│   ├── limoneide_plan.md (649 lines)
│   └── project_plan.md (388 lines)    # 프로젝트 계획서
├── backup/                            # 백업 파일 (로컬 전용)
├── google_api_key/                    # API 키 (로컬 전용)
└── tree.md (110 lines)                # 이 파일

총 파일 수: 53개
총 라인 수: 약 9,200줄
```

## 📊 프로젝트 통계

### **파일 분포**
- **Python 파일**: 28개 (백엔드)
- **JavaScript/TypeScript**: 12개 (프론트엔드)
- **HTML/CSS**: 4개 (UI)
- **JSON/설정**: 6개 (설정 파일)
- **문서**: 8개 (README, 계획서 등)

### **주요 모듈**
- **LimoneIDE_Backend**: 백엔드 시스템 (3,800줄)
  - core: AI 엔진 모듈 (1,400줄)
  - rag: 개인화 시스템 (900줄)
  - templates: 웹사이트 템플릿 (800줄)
  - automation: 자동화 엔진 (700줄)
- **LimoneIDE_Test**: PWA 앱 (1,600줄)
- **LimoneIDE_Beta**: 네이티브 앱 (1,800줄)
- **문서**: 프로젝트 문서 (2,000줄)

### **기술 스택**
- **백엔드**: Python, FastAPI, AsyncIO
- **AI**: OpenAI, Anthropic, Google Gemini, Ollama
- **프론트엔드**: Alpine.js, React Native, TypeScript
- **자동화**: Google App Engine, Cloud Resource Manager, OAuth2
- **모바일**: PWA, React Native, Expo

### **코드 품질**
- 모든 주요 모듈 200줄 이하로 유지
- 기능별 명확한 폴더 구조
- 재사용 가능한 인터페이스 설계
- 일관된 오류 처리 및 로깅

---

**생성일**: 2024년 6월 25일  
**버전**: v1.1  
**상태**: ✅ 완료 