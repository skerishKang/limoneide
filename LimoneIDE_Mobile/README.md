# 🍋 LimoneIDE Mobile PWA

**음성 중심 모바일 자동화 플랫폼**

LimoneIDE의 모바일 인터페이스로, 음성 명령만으로 웹사이트 생성, 이메일 작성, 일정 관리 등을 수행할 수 있습니다.

## 🚀 주요 기능

### ✅ **완성된 기능**
- **음성 인식**: 한국어 음성 명령 인식
- **PWA 지원**: 모바일 앱처럼 설치 가능
- **오프라인 모드**: 네트워크 없이도 기본 기능 사용
- **반응형 디자인**: 모든 모바일 기기 최적화
- **실시간 피드백**: 음성 처리 상태 실시간 표시
- **작업 히스토리**: 최근 명령 기록 및 재실행

### 🔄 **연동 기능**
- **백엔드 API**: LimoneIDE Core와 완전 연동
- **Google 서비스**: Drive, Sites, Gmail 연동
- **RAG 시스템**: 개인화된 AI 응답
- **자동화 워크플로우**: 복잡한 작업 자동화

## 📱 사용법

### 1. **PWA 설치**
1. 모바일 브라우저에서 `http://localhost:3000` 접속
2. "홈 화면에 추가" 또는 "앱 설치" 선택
3. LimoneIDE 앱이 홈 화면에 설치됨

### 2. **음성 명령 사용**
1. 중앙의 🎤 버튼 터치
2. 명령 말하기 (예: "웹사이트 만들어줘")
3. AI가 명령을 처리하고 결과 표시

### 3. **빠른 명령**
- 🌐 **웹사이트 생성**: "웹사이트 만들어줘"
- 📧 **이메일 작성**: "이메일 보내줘"
- 📅 **일정 관리**: "일정 관리해줘"
- 📄 **문서 요약**: "문서 요약해줘"

## 🛠️ 개발 환경 설정

### **필수 요구사항**
- Node.js 16+ (선택사항 - PWA 개발용)
- Python 3.11+ (백엔드용)
- 모바일 브라우저 (Chrome, Safari, Firefox)

### **설치 및 실행**

#### 1. **PWA 실행**
```bash
cd LimoneIDE_Mobile
npm install
npx live-server --port=3000 --open=/
```

#### 2. **백엔드 서버 실행** (선택사항)
```bash
cd LimoneIDE_Mobile
python server.py
```

#### 3. **통합 실행**
```bash
# 터미널 1: PWA 서버
npx live-server --port=3000

# 터미널 2: 백엔드 서버
python server.py
```

## 📁 프로젝트 구조

```
LimoneIDE_Mobile/
├── index.html              # 메인 HTML 파일
├── styles.css              # 모바일 최적화 CSS
├── app.js                  # Alpine.js 애플리케이션
├── server.py               # FastAPI 백엔드 서버
├── sw.js                   # Service Worker (PWA)
├── manifest.json           # PWA 매니페스트
├── package.json            # Node.js 의존성
├── icons/                  # PWA 아이콘들
│   └── icon-192x192.svg    # 메인 아이콘
└── README.md               # 이 파일
```

## 🎨 UI/UX 특징

### **모바일 최적화**
- **터치 친화적**: 큰 버튼과 터치 영역
- **제스처 지원**: 스와이프 네비게이션
- **하단 네비게이션**: 엄지손가락 접근성
- **다크 모드**: 시스템 설정 자동 적용

### **음성 중심 디자인**
- **중앙 마이크 버튼**: 직관적인 음성 명령
- **실시간 피드백**: 음성 인식 상태 표시
- **파형 애니메이션**: 듣는 중 시각적 피드백
- **음성 피드백**: AI 응답 음성 출력

### **접근성**
- **스크린 리더 지원**: ARIA 라벨 및 역할
- **키보드 네비게이션**: 포커스 관리
- **고대비 모드**: 시각 장애인 지원
- **모션 감소**: 민감한 사용자 고려

## 🔧 기술 스택

### **프론트엔드**
- **HTML5**: 시맨틱 마크업
- **CSS3**: 모던 스타일링 (CSS Variables, Grid, Flexbox)
- **Alpine.js**: 경량 반응형 프레임워크
- **Web Speech API**: 음성 인식 및 합성

### **백엔드** (선택사항)
- **FastAPI**: 고성능 Python 웹 프레임워크
- **LimoneIDE Core**: AI 엔진 및 자동화 모듈
- **CORS**: 크로스 오리진 리소스 공유

### **PWA 기능**
- **Service Worker**: 오프라인 캐싱
- **Web App Manifest**: 앱 설치 지원
- **IndexedDB**: 로컬 데이터 저장
- **Push API**: 푸시 알림 (향후 구현)

## 🧪 테스트

### **브라우저 호환성**
- ✅ Chrome 88+
- ✅ Safari 14+
- ✅ Firefox 85+
- ✅ Edge 88+

### **모바일 기기**
- ✅ iOS 14+ (Safari)
- ✅ Android 8+ (Chrome)
- ✅ PWA 설치 지원

### **음성 인식 테스트**
```javascript
// 브라우저 콘솔에서 테스트
if ('webkitSpeechRecognition' in window) {
    console.log('음성 인식 지원됨');
} else {
    console.log('음성 인식 미지원');
}
```

## 🚀 배포

### **정적 호스팅**
```bash
# 빌드
npm run build

# 배포 (예: Netlify, Vercel, GitHub Pages)
```

### **Docker 배포**
```dockerfile
FROM nginx:alpine
COPY . /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## 🔮 향후 계획

### **6단계: 고급 기능**
- [ ] **React Native 앱**: 네이티브 성능
- [ ] **푸시 알림**: 실시간 알림
- [ ] **오프라인 AI**: 로컬 AI 처리
- [ ] **제스처 인식**: 고급 제스처 지원

### **7단계: 확장 기능**
- [ ] **다국어 지원**: 영어, 일본어 등
- [ ] **음성 프로필**: 개인 음성 학습
- [ ] **팀 협업**: 멀티 유저 지원
- [ ] **API 마켓플레이스**: 서드파티 연동

## 🐛 문제 해결

### **음성 인식이 작동하지 않음**
1. HTTPS 환경에서 실행 (로컬에서는 localhost 허용)
2. 마이크 권한 확인
3. 브라우저 호환성 확인

### **PWA 설치가 안됨**
1. Service Worker 등록 확인
2. Manifest 파일 유효성 검사
3. HTTPS 환경 확인

### **백엔드 연결 실패**
1. 서버 실행 상태 확인
2. CORS 설정 확인
3. 포트 충돌 확인

## 📞 지원

- **이슈 리포트**: GitHub Issues
- **문서**: `/docs` 폴더
- **API 문서**: `http://localhost:8000/docs` (FastAPI)

## 📄 라이선스

MIT License - 자유롭게 사용, 수정, 배포 가능

---

**"Think it, Say it, Done it"** - LimoneIDE Mobile로 AI 시대의 새로운 모바일 경험을 만들어보세요! 🍋✨ 