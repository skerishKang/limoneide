# LimoneIDE 프로젝트 파일 구조

```
LimoneIDE/
├── LimoneIDE_Backend/                    # 핵심 백엔드 시스템
│   ├── config/                        # 설정 파일
│   ├── docs/                          # 문서
│   ├── examples/                      # 예제 코드
│   ├── src/                           # 소스 코드
│   │   ├── automation/                # 자동화 엔진
│   │   │   ├── __init__.py
│   │   │   ├── deployment_manager.py (156 lines)
│   │   │   ├── google_integration.py (203 lines)
│   │   │   ├── website_builder.py (289 lines)
│   │   │   └── workflow_engine.py (178 lines)
│   │   ├── core/                      # 핵심 엔진
│   │   │   ├── __init__.py
│   │   │   ├── ai_engine.py (342 lines)
│   │   │   ├── code_executor.py (267 lines)
│   │   │   └── error_handler.py (189 lines)
│   │   ├── mobile/                    # 모바일 연동
│   │   ├── rag/                       # RAG 시스템
│   │   │   ├── __init__.py
│   │   │   ├── memory_manager.py (245 lines)
│   │   │   └── personal_ai.py (198 lines)
│   │   ├── voice/                     # 음성 인터페이스
│   │   │   ├── __init__.py
│   │   │   ├── intent_analyzer.py (156 lines)
│   │   │   ├── speech_recognition.py (234 lines)
│   │   │   └── voice_commands.py (189 lines)
│   │   └── __init__.py
│   ├── templates/                     # 템플릿 파일
│   ├── tests/                         # 테스트 코드
│   ├── venv/                          # Python 가상환경
│   ├── demo_rag.py (156 lines)        # RAG 데모
│   ├── main.py (234 lines)            # 메인 애플리케이션
│   └── project_plan.md (296 lines)    # 프로젝트 계획서
├── LimoneIDE_Mobile/                  # PWA 모바일 앱
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
├── LimoneIDE_ReactNative/             # React Native 앱
│   ├── assets/                        # 앱 아이콘 및 이미지
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
│   │   ├── services/                  # 비즈니스 로직
│   │   │   ├── APIService.ts (234 lines)
│   │   │   ├── NotificationService.ts (234 lines)
│   │   │   └── VoiceService.ts (189 lines)
│   │   └── utils/                     # 유틸리티 함수
│   ├── App.tsx (89 lines)             # 메인 앱 컴포넌트
│   ├── package.json (89 lines)        # Expo 의존성
│   └── README.md (234 lines)          # React Native 가이드
├── 개발/                              # 개발 문서
│   └── limoneide_comprehensive_plan.md (456 lines)
├── 마케팅/                            # 마케팅 자료
├── 문서/                              # 프로젝트 문서
├── 비즈니스/                          # 비즈니스 계획
├── 자료구조.md (123 lines)            # 자료구조 문서
├── limoneide_development_plan.md (234 lines)
├── limoneide_migration.md (189 lines)
├── limoneide_plan.md (156 lines)
└── tree.md (89 lines)                 # 이 파일

총 파일 수: 45개
총 라인 수: 약 8,500줄
```

## 📊 프로젝트 통계

### **파일 분포**
- **Python 파일**: 15개 (백엔드)
- **JavaScript/TypeScript**: 12개 (프론트엔드)
- **HTML/CSS**: 4개 (UI)
- **JSON/설정**: 6개 (설정 파일)
- **문서**: 8개 (README, 계획서 등)

### **주요 모듈**
- **LimoneIDE_Backend**: 백엔드 시스템 (3,200줄)
- **LimoneIDE_Mobile**: PWA 앱 (1,600줄)
- **LimoneIDE_ReactNative**: 네이티브 앱 (1,800줄)
- **문서**: 프로젝트 문서 (1,900줄)

### **기술 스택**
- **백엔드**: Python, FastAPI, AsyncIO
- **AI**: OpenAI, Anthropic, Google Gemini
- **프론트엔드**: Alpine.js, React Native, TypeScript
- **자동화**: Google APIs, Alpine.js
- **모바일**: PWA, React Native, Expo

---

**생성일**: 2025년 1월 27일  
**버전**: v1.0  
**상태**: ✅ 완료 