# LimoneIDE 프로젝트 대화 요약 (간단 버전)

## 🎯 현재 상황
- **복구 브랜치**: `recovery-2024-06-09` (전체 파일 복구됨)
- **메인 브랜치**: `master` (API 키 제거된 깨끗한 상태)
- **다음 단계**: 복구 브랜치에서 폴더명 변경 후 master와 통합

## 📁 프로젝트 구조
```
LimoneIDE/
├── LimoneIDE_Backend/     # Python 백엔드 (이전: core)
├── LimoneIDE_Mobile/      # PWA 앱 (이전: mobile)  
├── LimoneIDE_Beta/        # React Native (이전: reactnative)
├── backup/                # 백업 파일들
├── plan/                  # 프로젝트 계획
└── docs/                  # 문서 (새로 생성)
```

## 🔑 주요 설정
- **가상환경**: `LimoneIDE_Backend/venv/`
- **API 키**: `.env` 파일 (Git에서 제외)
- **의존성**: `requirements.txt`

## 🚀 다음 작업
1. `git checkout recovery-2024-06-09`
2. 폴더명 변경 작업
3. master 브랜치와 통합
4. 개발 시작

---
*자세한 내용은 `project_recovery_summary.md` 참조* 