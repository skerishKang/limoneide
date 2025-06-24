# LimoneIDE 프로젝트 복구 및 구조 관리 대화 요약

**작성일**: 2024년 6월 9일  
**문서 버전**: v1.0  
**상태**: 진행 중

---

## 📋 프로젝트 개요

### 프로젝트 목적
LimoneIDE는 AI 음성 자동화 플랫폼으로, 다음과 같은 구성 요소로 이루어져 있습니다:

- **LimoneIDE_Backend**: Python 기반 백엔드 (AI 엔진, 음성 처리, 자동화 워크플로우)
- **LimoneIDE_Mobile**: PWA 모바일 앱 (Alpine.js, FastAPI 백엔드)
- **LimoneIDE_Beta**: React Native 모바일 앱 (Expo, 네이티브 기능)

### 폴더 구조 변경 이력
- `core` → `LimoneIDE_Backend`
- `mobile` → `LimoneIDE_Mobile` 
- `reactnative` → `LimoneIDE_Beta`

---

## 🔄 복구 및 브랜치 관리 과정

### 1. 초기 문제 상황
- GitHub 저장소에 API 키가 노출된 문서 파일들이 존재
- 폴더명 변경과 동시에 실제 개발이 진행되어 구조가 복잡해짐
- master 브랜치에서 많은 폴더/파일이 삭제된 상태

### 2. 복구 전략 수립
- 과거 커밋(`00e5cb9c3697f3a8fc776bcc074c5469dfe48090`)에서 전체 파일 구조 확인
- 복구 브랜치(`recovery-2024-06-09`) 생성
- API 키 노출 문제 해결을 위한 clean-main 브랜치 생성

### 3. 브랜치 관리 과정
```
master (기본) → clean-main (API 키 제거) → master (force push)
recovery-2024-06-09 (전체 복구)
```

### 4. 현재 브랜치 상태
- **master**: API 키가 제거된 깨끗한 상태
- **recovery-2024-06-09**: 전체 파일/폴더가 복구된 상태
- **origin/master**: GitHub 원격 저장소와 동기화됨

---

## 🛠️ 환경 설정 및 의존성 관리

### 1. 가상환경 설정
- Python 가상환경을 `LimoneIDE_Backend` 폴더 내부에 생성
- `requirements.txt` 파일로 의존성 관리
- 주요 패키지: FastAPI, OpenAI, Google API, ChromaDB, gTTS 등

### 2. API 키 관리
- `.env` 파일에 API 키 저장 (Git에서 제외)
- Google OAuth 클라이언트 시크릿 JSON 파일 관리
- 보안을 위한 `.gitignore` 설정

### 3. 개발 환경 구성
- Node.js 패키지 관리 (React Native, PWA)
- Python 백엔드 서버 설정
- 모바일 앱 개발 환경 (Expo, Alpine.js)

---

## 📁 현재 프로젝트 구조

```
LimoneIDE/
├── LimoneIDE_Backend/          # Python 백엔드
│   ├── src/
│   ├── venv/                   # Python 가상환경
│   └── requirements.txt
├── LimoneIDE_Mobile/           # PWA 모바일 앱
├── LimoneIDE_Beta/             # React Native 앱
├── backup/                     # 백업 파일들
├── plan/                       # 프로젝트 계획 문서
├── google_api_key/             # Google API 키 파일
├── venv/                       # 루트 가상환경 (이전)
├── requirements.txt            # 루트 의존성 파일
└── tree.md                     # 프로젝트 구조 문서
```

---

## 🚧 현재 진행 상황

### 완료된 작업
- [x] GitHub 저장소 정리 및 API 키 보안 강화
- [x] 복구 브랜치 생성 및 전체 파일 복구
- [x] 가상환경 설정 및 의존성 설치
- [x] 프로젝트 구조 문서화

### 진행 중인 작업
- [ ] 복구 브랜치에서 폴더명 변경 작업
- [ ] master 브랜치와 recovery 브랜치 통합
- [ ] 개발 환경 최종 설정

### 다음 단계
1. **복구 브랜치 활성화**: `recovery-2024-06-09` 브랜치로 전환
2. **폴더명 변경**: 기존 폴더명을 새로운 명명 규칙에 맞게 변경
3. **코드 통합**: 변경된 구조를 master 브랜치에 반영
4. **개발 시작**: 백엔드 서버 실행 및 테스트

---

## 🔑 주요 API 키 및 설정

### 필요한 API 키
- OpenAI API Key
- Google Gemini API Key
- Telegram Bot Token
- Google OAuth Client Secret

### 환경 변수 설정
```env
OPENAI_API_KEY=your_openai_key
GEMINI_API_KEY=your_gemini_key
TELEGRAM_BOT_TOKEN=your_telegram_token
GOOGLE_CLIENT_SECRET_FILE=path_to_client_secret.json
```

---

## 📝 개발 가이드라인

### 1. 브랜치 전략
- `master`: 안정적인 메인 브랜치
- `development`: 개발 브랜치
- `feature/*`: 기능별 브랜치
- `recovery-*`: 복구용 브랜치

### 2. 커밋 규칙
- 한국어로 커밋 메시지 작성
- 기능별로 명확한 커밋 메시지
- API 키나 민감한 정보는 절대 커밋하지 않음

### 3. 문서화 정책
- 10번 커밋마다 `tree.md` 업데이트
- 중요한 변경사항은 `docs/` 폴더에 문서화
- 프로젝트 계획은 `plan/` 폴더에 저장

---

## ⚠️ 주의사항

### 보안
- API 키는 절대 Git에 커밋하지 않음
- `.env` 파일은 `.gitignore`에 포함
- Google API 키 파일은 별도 폴더에 보관

### 개발 환경
- Python 가상환경 사용 필수
- Node.js 버전 호환성 확인
- 모바일 앱 개발 시 Expo CLI 사용

### 브랜치 관리
- 복구 브랜치는 임시용으로만 사용
- 중요한 변경사항은 별도 브랜치에서 작업
- master 브랜치 병합 전 충분한 테스트 필요

---

## 📞 문제 해결 가이드

### 자주 발생하는 문제
1. **가상환경 활성화 실패**: PowerShell 실행 정책 확인
2. **패키지 설치 오류**: pip 업그레이드 및 캐시 클리어
3. **Git 권한 오류**: `.cursor/rules` 폴더 권한 확인
4. **API 키 오류**: `.env` 파일 경로 및 형식 확인

### 복구 방법
- 브랜치 복구: `git checkout recovery-2024-06-09`
- 파일 복구: `git checkout <commit_hash> -- <file_path>`
- 전체 복구: `git reset --hard <commit_hash>`

---

**문서 작성자**: AI Assistant  
**최종 업데이트**: 2024년 6월 9일  
**다음 검토 예정**: 프로젝트 복구 완료 후 