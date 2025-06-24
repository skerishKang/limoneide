# LimoneIDE React Native App

음성 중심 모바일 자동화 플랫폼의 React Native 앱입니다.

## 🚀 주요 기능

### 음성 인식 및 명령
- 실시간 음성 인식
- 자연어 명령 처리
- 음성 피드백
- 명령 히스토리

### 자동화 기능
- 웹사이트 자동 생성
- 이메일 작성 및 전송
- 일정 관리
- 문서 요약

### 모바일 최적화
- 네이티브 성능
- 오프라인 지원
- 푸시 알림
- 햅틱 피드백

## 📱 스크린샷

### 홈 스크린
- 음성 명령 버튼
- 빠른 명령 버튼
- AI 응답 카드
- 작업 히스토리

### 프로젝트 스크린
- 생성된 프로젝트 목록
- 프로젝트 상태 관리
- 프로젝트 삭제

### 설정 스크린
- 앱 설정 관리
- 사용자 인사이트
- API 연결 설정

## 🛠️ 기술 스택

- **React Native** - 크로스 플랫폼 모바일 개발
- **Expo** - 개발 도구 및 서비스
- **TypeScript** - 타입 안전성
- **React Navigation** - 네비게이션
- **Expo Speech** - 음성 합성
- **Expo Notifications** - 푸시 알림
- **Expo Haptics** - 햅틱 피드백

## 📦 설치 및 실행

### 필수 요구사항
- Node.js 18+
- npm 또는 yarn
- Expo CLI
- iOS Simulator 또는 Android Emulator

### 설치
```bash
# 의존성 설치
npm install

# Expo CLI 설치 (전역)
npm install -g @expo/cli
```

### 실행
```bash
# 개발 서버 시작
npm start

# iOS 시뮬레이터에서 실행
npm run ios

# Android 에뮬레이터에서 실행
npm run android

# 웹에서 실행
npm run web
```

## 🔧 개발 환경 설정

### 1. Expo 계정 생성
```bash
expo login
```

### 2. 프로젝트 설정
```bash
# Expo 프로젝트 ID 설정
expo config --project-id your-project-id
```

### 3. 환경 변수 설정
```bash
# .env 파일 생성
cp .env.example .env

# 환경 변수 편집
API_BASE_URL=http://localhost:8000
EXPO_PROJECT_ID=your-project-id
```

## 📁 프로젝트 구조

```
src/
├── components/          # 재사용 가능한 컴포넌트
│   ├── VoiceButton.tsx
│   ├── ResponseCard.tsx
│   ├── QuickCommandButton.tsx
│   └── TaskHistory.tsx
├── screens/            # 화면 컴포넌트
│   ├── HomeScreen.tsx
│   ├── ProjectsScreen.tsx
│   └── SettingsScreen.tsx
├── services/           # 비즈니스 로직
│   ├── VoiceService.ts
│   ├── APIService.ts
│   └── NotificationService.ts
└── utils/              # 유틸리티 함수
    └── constants.ts
```

## 🔌 API 연동

### 백엔드 서버 연결
앱은 LimoneIDE 백엔드 서버와 연동됩니다:

- **음성 명령 처리**: `/voice-command`
- **프로젝트 관리**: `/projects`
- **사용자 인사이트**: `/user-insights`
- **상태 확인**: `/health`

### 오프라인 모드
네트워크 연결이 없을 때는 데모 모드로 동작합니다.

## 🎨 UI/UX 특징

### 디자인 시스템
- **색상**: LimoneIDE 브랜드 컬러 (#4ade80)
- **타이포그래피**: 시스템 폰트 사용
- **아이콘**: Ionicons
- **애니메이션**: React Native Animated

### 접근성
- 음성 명령으로 모든 기능 접근 가능
- 햅틱 피드백으로 시각적 피드백 보완
- 고대비 모드 지원

## 📊 성능 최적화

### 메모리 관리
- 컴포넌트 언마운트 시 리소스 정리
- 이미지 최적화
- 불필요한 리렌더링 방지

### 네트워크 최적화
- API 요청 캐싱
- 오프라인 큐 시스템
- 연결 상태 모니터링

## 🧪 테스트

### 단위 테스트
```bash
npm test
```

### E2E 테스트
```bash
npm run test:e2e
```

### 성능 테스트
```bash
npm run test:performance
```

## 📦 빌드 및 배포

### Android 빌드
```bash
# APK 빌드
expo build:android

# AAB 빌드 (Google Play Store)
expo build:android --type app-bundle
```

### iOS 빌드
```bash
# IPA 빌드
expo build:ios
```

### 웹 빌드
```bash
# 웹 빌드
expo build:web
```

## 🚀 배포

### Expo Application Services (EAS)
```bash
# EAS CLI 설치
npm install -g @expo/eas-cli

# 빌드 설정
eas build:configure

# Android 빌드
eas build --platform android

# iOS 빌드
eas build --platform ios
```

### 스토어 배포
```bash
# Google Play Store
eas submit --platform android

# App Store
eas submit --platform ios
```

## 🔒 보안

### 데이터 보호
- 민감한 정보 암호화
- 안전한 API 통신
- 로컬 데이터 보호

### 권한 관리
- 필요한 권한만 요청
- 권한 사용 목적 명시
- 사용자 동의 기반

## 📈 분석 및 모니터링

### 사용자 분석
- 명령 사용 패턴 분석
- 성능 메트릭 수집
- 오류 추적

### 성능 모니터링
- 앱 시작 시간
- 메모리 사용량
- 네트워크 성능

## 🤝 기여하기

### 개발 가이드라인
1. TypeScript 사용
2. 컴포넌트 단위 테스트 작성
3. 코드 리뷰 필수
4. 커밋 메시지 규칙 준수

### 이슈 리포트
- 버그 리포트는 상세한 재현 단계 포함
- 기능 요청은 사용 사례 명시
- 성능 이슈는 메트릭 포함

## 📄 라이선스

MIT License - 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 👥 팀

- **개발**: LimoneIDE Team
- **디자인**: LimoneIDE Design Team
- **기획**: LimoneIDE Product Team

## 📞 지원

- **이메일**: support@limoneide.com
- **문서**: [docs.limoneide.com](https://docs.limoneide.com)
- **커뮤니티**: [community.limoneide.com](https://community.limoneide.com)

---

**LimoneIDE** - Think it, Say it, Done it! 🚀 