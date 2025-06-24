// LimoneIDE Test Mobile PWA - Main Application
// Alpine.js 기반 음성 자동화 플랫폼

function limoneideTestApp() {
    return {
        // 상태 관리
        isListening: false,
        isProcessing: false,
        isLoading: false,
        connectionStatus: 'connected',
        connectionStatusText: '연결됨',
        aiResponse: '',
        statusText: '',
        voiceButtonText: '음성 명령',
        loadingText: '처리 중...',
        recentTasks: [],
        toasts: [],
        toastId: 0,
        apiBaseUrl: 'http://localhost:8000',

        // 음성 인식 관련
        recognition: null,
        speechSynthesis: window.speechSynthesis,

        // 초기화
        init() {
            this.initializeSpeechRecognition();
            this.initializeServiceWorker();
            this.loadRecentTasks();
            this.checkConnection();
            
            // 주기적 연결 상태 확인
            setInterval(() => this.checkConnection(), 30000);
        },

        // 음성 인식 초기화
        initializeSpeechRecognition() {
            if ('webkitSpeechRecognition' in window) {
                this.recognition = new webkitSpeechRecognition();
                this.recognition.continuous = false;
                this.recognition.interimResults = false;
                this.recognition.lang = 'ko-KR';
                
                this.recognition.onstart = () => {
                    this.isListening = true;
                    this.statusText = '듣고 있습니다...';
                    this.voiceButtonText = '듣는 중';
                };
                
                this.recognition.onresult = (event) => {
                    const transcript = event.results[0][0].transcript;
                    this.processVoiceCommand(transcript);
                };
                
                this.recognition.onerror = (event) => {
                    console.error('Speech recognition error:', event.error);
                    this.showToast('음성 인식 오류가 발생했습니다.', 'error');
                    this.stopVoiceRecognition();
                };
                
                this.recognition.onend = () => {
                    this.stopVoiceRecognition();
                };
            } else {
                this.showToast('이 브라우저는 음성 인식을 지원하지 않습니다.', 'warning');
            }
        },

        // Service Worker 초기화
        async initializeServiceWorker() {
            if ('serviceWorker' in navigator) {
                try {
                    const registration = await navigator.serviceWorker.register('/sw.js');
                    console.log('Service Worker 등록 성공:', registration);
                } catch (error) {
                    console.error('Service Worker 등록 실패:', error);
                }
            }
        },

        // 음성 명령 토글
        toggleVoiceRecognition() {
            if (this.isListening) {
                this.stopVoiceRecognition();
            } else {
                this.startVoiceRecognition();
            }
        },

        // 음성 인식 시작
        startVoiceRecognition() {
            if (this.recognition) {
                try {
                    this.recognition.start();
                } catch (error) {
                    console.error('음성 인식 시작 실패:', error);
                    this.showToast('음성 인식을 시작할 수 없습니다.', 'error');
                }
            }
        },

        // 음성 인식 중지
        stopVoiceRecognition() {
            if (this.recognition) {
                this.recognition.stop();
            }
            this.isListening = false;
            this.statusText = '';
            this.voiceButtonText = '음성 명령';
        },

        // 음성 명령 처리
        async processVoiceCommand(transcript) {
            this.isProcessing = true;
            this.statusText = '명령을 처리하고 있습니다...';
            this.voiceButtonText = '처리 중';
            
            try {
                // 실제 백엔드 API 호출
                const response = await this.callBackendAPI(transcript);
                
                // 응답 처리
                this.aiResponse = this.formatResponse(response);
                
                // 작업 히스토리에 추가
                this.addToRecentTasks(transcript, response);
                
                // 음성 피드백 (선택적)
                if (response.speak) {
                    this.speakResponse(response.speak);
                }
                
                this.showToast('명령이 성공적으로 처리되었습니다.', 'success');
                
            } catch (error) {
                console.error('API 호출 오류:', error);
                // 백엔드 연결 실패 시 데모 모드로 전환
                const demoResponse = await this.mockBackendCall(transcript);
                this.aiResponse = this.formatResponse(demoResponse);
                this.addToRecentTasks(transcript, demoResponse);
                this.showToast('데모 모드로 실행됨', 'warning');
            } finally {
                this.isProcessing = false;
                this.statusText = '';
                this.voiceButtonText = '음성 명령';
            }
        },

        // 백엔드 API 호출
        async callBackendAPI(command) {
            const response = await fetch(`${this.apiBaseUrl}/voice-command`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    command: command,
                    timestamp: new Date().toISOString(),
                    user_agent: navigator.userAgent
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        },

        // 응답 포맷팅
        formatResponse(response) {
            let formatted = '';
            
            if (response.title) {
                formatted += `<h3>${response.title}</h3>`;
            }
            
            if (response.content) {
                formatted += `<p>${response.content}</p>`;
            }
            
            if (response.url) {
                formatted += `<p><a href="${response.url}" target="_blank" class="response-link">🔗 결과 보기</a></p>`;
            }
            
            if (response.steps && response.steps.length > 0) {
                formatted += '<ul>';
                response.steps.forEach(step => {
                    formatted += `<li>${step}</li>`;
                });
                formatted += '</ul>';
            }
            
            return formatted;
        },

        // 빠른 명령 실행
        async executeQuickCommand(command) {
            this.showToast('명령을 실행하고 있습니다...', 'success');
            await this.processVoiceCommand(command);
        },

        // 작업 히스토리에 추가
        addToRecentTasks(command, response) {
            const task = {
                id: Date.now(),
                title: command,
                time: new Date().toLocaleTimeString('ko-KR'),
                icon: this.getTaskIcon(response.type || 'general'),
                command: command,
                response: response
            };
            
            this.recentTasks.unshift(task);
            
            // 최대 10개까지만 유지
            if (this.recentTasks.length > 10) {
                this.recentTasks = this.recentTasks.slice(0, 10);
            }
            
            // 로컬 스토리지에 저장
            this.saveRecentTasks();
        },

        // 작업 아이콘 가져오기
        getTaskIcon(type) {
            const icons = {
                website: '🌐',
                email: '📧',
                schedule: '📅',
                document: '📄',
                automation: '⚙️',
                general: '🎯'
            };
            return icons[type] || icons.general;
        },

        // 작업 재실행
        async replayTask(task) {
            this.showToast('작업을 재실행하고 있습니다...', 'success');
            await this.processVoiceCommand(task.command);
        },

        // 응답 지우기
        clearResponse() {
            this.aiResponse = '';
        },

        // 음성 피드백
        speakResponse(text) {
            if (this.speechSynthesis) {
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.lang = 'ko-KR';
                utterance.rate = 0.9;
                this.speechSynthesis.speak(utterance);
            }
        },

        // 연결 상태 확인
        async checkConnection() {
            try {
                const response = await fetch(`${this.apiBaseUrl}/health`, {
                    method: 'GET',
                    timeout: 5000
                });
                
                if (response.ok) {
                    this.connectionStatus = 'connected';
                    this.connectionStatusText = '연결됨';
                } else {
                    throw new Error('서버 응답 오류');
                }
            } catch (error) {
                this.connectionStatus = 'disconnected';
                this.connectionStatusText = '연결 끊김';
            }
        },

        // 최근 작업 로드
        loadRecentTasks() {
            try {
                const saved = localStorage.getItem('limoneide_recent_tasks');
                if (saved) {
                    this.recentTasks = JSON.parse(saved);
                }
            } catch (error) {
                console.error('최근 작업 로드 실패:', error);
            }
        },

        // 최근 작업 저장
        saveRecentTasks() {
            try {
                localStorage.setItem('limoneide_recent_tasks', JSON.stringify(this.recentTasks));
            } catch (error) {
                console.error('최근 작업 저장 실패:', error);
            }
        },

        // 토스트 메시지 표시
        showToast(message, type = 'success') {
            const toast = {
                id: ++this.toastId,
                message: message,
                type: type,
                visible: true,
                icon: this.getToastIcon(type)
            };
            
            this.toasts.push(toast);
            
            // 3초 후 자동 제거
            setTimeout(() => {
                toast.visible = false;
                setTimeout(() => {
                    this.toasts = this.toasts.filter(t => t.id !== toast.id);
                }, 300);
            }, 3000);
        },

        // 토스트 아이콘 가져오기
        getToastIcon(type) {
            const icons = {
                success: '✅',
                error: '❌',
                warning: '⚠️'
            };
            return icons[type] || icons.success;
        },

        // 네비게이션
        showHome() {
            this.showToast('홈 화면으로 이동합니다.', 'success');
        },

        showProjects() {
            this.showToast('프로젝트 목록을 불러오는 중...', 'success');
            // 프로젝트 목록 로직 구현 예정
        },

        showSettings() {
            this.showToast('설정 화면으로 이동합니다.', 'success');
            // 설정 화면 로직 구현 예정
        },

        // 로딩 상태 관리
        setLoading(loading, text = '처리 중...') {
            this.isLoading = loading;
            this.loadingText = text;
        },

        // 오프라인 모드 처리
        handleOfflineMode() {
            this.showToast('오프라인 모드로 전환되었습니다.', 'warning');
            // 오프라인 작업 큐에 저장
            this.saveOfflineTask();
        },

        // 오프라인 작업 저장
        saveOfflineTask() {
            // IndexedDB에 오프라인 작업 저장
            if ('indexedDB' in window) {
                // IndexedDB 로직 구현 예정
                console.log('오프라인 작업 저장됨');
            }
        },

        // 제스처 인식 (터치 이벤트)
        handleTouchStart(event) {
            this.touchStartX = event.touches[0].clientX;
            this.touchStartY = event.touches[0].clientY;
        },

        handleTouchEnd(event) {
            if (!this.touchStartX || !this.touchStartY) return;
            
            const touchEndX = event.changedTouches[0].clientX;
            const touchEndY = event.changedTouches[0].clientY;
            
            const deltaX = touchEndX - this.touchStartX;
            const deltaY = touchEndY - this.touchStartY;
            
            // 스와이프 제스처 인식
            if (Math.abs(deltaX) > Math.abs(deltaY)) {
                if (deltaX > 50) {
                    // 오른쪽 스와이프
                    this.showToast('오른쪽 스와이프 감지', 'success');
                } else if (deltaX < -50) {
                    // 왼쪽 스와이프
                    this.showToast('왼쪽 스와이프 감지', 'success');
                }
            } else {
                if (deltaY > 50) {
                    // 아래쪽 스와이프
                    this.showToast('아래쪽 스와이프 감지', 'success');
                } else if (deltaY < -50) {
                    // 위쪽 스와이프
                    this.showToast('위쪽 스와이프 감지', 'success');
                }
            }
            
            this.touchStartX = null;
            this.touchStartY = null;
        },

        async mockBackendCall(command) {
            // 데모용 응답
            await new Promise(resolve => setTimeout(resolve, 2000));
            
            if (command.includes('웹사이트')) {
                return {
                    title: '웹사이트 생성 완료',
                    content: '요청하신 웹사이트가 성공적으로 생성되었습니다.',
                    url: 'https://sites.google.com/view/demo-site',
                    type: 'website'
                };
            } else if (command.includes('이메일')) {
                return {
                    title: '이메일 작성 완료',
                    content: '이메일이 작성되었습니다. 확인해보세요.',
                    type: 'email'
                };
            } else if (command.includes('일정')) {
                return {
                    title: '일정 관리 완료',
                    content: '일정이 성공적으로 관리되었습니다.',
                    type: 'schedule'
                };
            } else {
                return {
                    title: '명령 처리 완료',
                    content: `"${command}" 명령이 성공적으로 처리되었습니다.`,
                    type: 'general'
                };
            }
        }
    };
}

// 전역 함수로 등록
window.limoneideTestApp = limoneideTestApp;

// PWA 설치 프롬프트
let deferredPrompt;

window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
    
    // 설치 버튼 표시 로직
    console.log('PWA 설치 가능');
});

// 앱 설치 완료 이벤트
window.addEventListener('appinstalled', () => {
    console.log('PWA가 성공적으로 설치되었습니다.');
    deferredPrompt = null;
});

// 온라인/오프라인 상태 감지
window.addEventListener('online', () => {
    console.log('온라인 상태로 전환');
    // 온라인 상태 복구 로직
});

window.addEventListener('offline', () => {
    console.log('오프라인 상태로 전환');
    // 오프라인 모드 활성화
});

// 페이지 가시성 변경 감지
document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        console.log('페이지가 숨겨짐');
        // 백그라운드 작업 정리
    } else {
        console.log('페이지가 다시 보임');
        // 포그라운드 작업 재개
    }
}); 