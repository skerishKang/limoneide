import axios from 'axios';

interface VoiceCommandRequest {
  command: string;
  timestamp: string;
  user_agent?: string;
  user_id?: string;
}

interface CommandResponse {
  title: string;
  content: string;
  type: string;
  url?: string;
  speak?: string;
  steps?: string[];
  metadata?: any;
}

interface Task {
  id: string;
  title: string;
  time: string;
  icon: string;
  command: string;
}

class APIService {
  private static instance: APIService;
  private baseURL: string = 'http://localhost:8000';
  private isConnected: boolean = false;

  static getInstance(): APIService {
    if (!APIService.instance) {
      APIService.instance = new APIService();
    }
    return APIService.instance;
  }

  async checkConnection(): Promise<boolean> {
    try {
      const response = await axios.get(`${this.baseURL}/health`, {
        timeout: 5000,
      });
      this.isConnected = response.status === 200;
      return this.isConnected;
    } catch (error) {
      this.isConnected = false;
      console.log('백엔드 서버 연결 실패, 데모 모드로 전환');
      return false;
    }
  }

  async sendVoiceCommand(command: string): Promise<CommandResponse> {
    try {
      if (!this.isConnected) {
        // 데모 모드
        return this.getDemoResponse(command);
      }

      const request: VoiceCommandRequest = {
        command,
        timestamp: new Date().toISOString(),
        user_agent: 'LimoneIDE-ReactNative/1.0.0',
      };

      const response = await axios.post(`${this.baseURL}/voice-command`, request, {
        timeout: 30000,
      });

      return response.data;
    } catch (error) {
      console.error('API 호출 실패:', error);
      // API 실패 시 데모 모드로 전환
      return this.getDemoResponse(command);
    }
  }

  private getDemoResponse(command: string): CommandResponse {
    // 데모용 응답 생성
    if (command.includes('웹사이트')) {
      return {
        title: '웹사이트 생성 완료',
        content: '요청하신 웹사이트가 성공적으로 생성되었습니다.',
        type: 'website',
        url: 'https://sites.google.com/view/demo-site',
        speak: '웹사이트가 성공적으로 생성되었습니다.',
      };
    } else if (command.includes('이메일')) {
      return {
        title: '이메일 작성 완료',
        content: '이메일이 작성되었습니다. 확인해보세요.',
        type: 'email',
        speak: '이메일이 작성되었습니다.',
      };
    } else if (command.includes('일정')) {
      return {
        title: '일정 관리 완료',
        content: '일정이 성공적으로 관리되었습니다.',
        type: 'schedule',
        speak: '일정이 관리되었습니다.',
      };
    } else if (command.includes('문서')) {
      return {
        title: '문서 요약 완료',
        content: '문서가 성공적으로 요약되었습니다.',
        type: 'document',
        speak: '문서 요약이 완료되었습니다.',
      };
    } else {
      return {
        title: '명령 처리 완료',
        content: `"${command}" 명령이 성공적으로 처리되었습니다.`,
        type: 'general',
        speak: '명령이 처리되었습니다.',
      };
    }
  }

  async getRecentTasks(): Promise<Task[]> {
    try {
      if (!this.isConnected) {
        // 데모 데이터
        return this.getDemoTasks();
      }

      const response = await axios.get(`${this.baseURL}/recent-tasks`);
      return response.data.tasks || [];
    } catch (error) {
      console.error('최근 작업 조회 실패:', error);
      return this.getDemoTasks();
    }
  }

  private getDemoTasks(): Task[] {
    return [
      {
        id: '1',
        title: '웹사이트 만들어줘',
        time: '14:30',
        icon: '🌐',
        command: '웹사이트 만들어줘',
      },
      {
        id: '2',
        title: '이메일 보내줘',
        time: '14:25',
        icon: '📧',
        command: '이메일 보내줘',
      },
      {
        id: '3',
        title: '일정 관리해줘',
        time: '14:20',
        icon: '📅',
        command: '일정 관리해줘',
      },
    ];
  }

  async getUserInsights(): Promise<any> {
    try {
      if (!this.isConnected) {
        return this.getDemoInsights();
      }

      const response = await axios.get(`${this.baseURL}/user-insights`);
      return response.data;
    } catch (error) {
      console.error('사용자 인사이트 조회 실패:', error);
      return this.getDemoInsights();
    }
  }

  private getDemoInsights(): any {
    return {
      totalConversations: 15,
      preferredTopics: ['website', 'email', 'schedule'],
      productivityScore: 85,
      mostUsedCommands: [
        { command: '웹사이트 만들어줘', count: 8 },
        { command: '이메일 보내줘', count: 5 },
        { command: '일정 관리해줘', count: 2 },
      ],
      suggestions: [
        '자주 사용하는 명령을 음성 단축키로 설정해보세요',
        '새로운 자동화 워크플로우를 만들어보세요',
        '프로젝트 템플릿을 활용해보세요',
      ],
    };
  }

  async submitFeedback(feedback: {
    rating: number;
    comment: string;
    command?: string;
  }): Promise<void> {
    try {
      if (!this.isConnected) {
        console.log('데모 모드: 피드백 저장됨', feedback);
        return;
      }

      await axios.post(`${this.baseURL}/feedback`, feedback);
    } catch (error) {
      console.error('피드백 제출 실패:', error);
    }
  }

  // 오프라인 작업 큐 관리
  private offlineQueue: Array<{
    id: string;
    command: string;
    timestamp: string;
  }> = [];

  async addToOfflineQueue(command: string): Promise<void> {
    const offlineTask = {
      id: Date.now().toString(),
      command,
      timestamp: new Date().toISOString(),
    };

    this.offlineQueue.push(offlineTask);
    console.log('오프라인 작업 큐에 추가됨:', offlineTask);
  }

  async processOfflineQueue(): Promise<void> {
    if (this.offlineQueue.length === 0 || !this.isConnected) {
      return;
    }

    console.log('오프라인 작업 큐 처리 중...');
    
    for (const task of this.offlineQueue) {
      try {
        await this.sendVoiceCommand(task.command);
        console.log('오프라인 작업 처리 완료:', task.command);
      } catch (error) {
        console.error('오프라인 작업 처리 실패:', error);
      }
    }

    this.offlineQueue = [];
  }

  // 연결 상태 모니터링
  startConnectionMonitoring(): void {
    setInterval(async () => {
      await this.checkConnection();
    }, 30000); // 30초마다 연결 상태 확인
  }

  getConnectionStatus(): boolean {
    return this.isConnected;
  }

  // API 설정 업데이트
  updateBaseURL(url: string): void {
    this.baseURL = url;
    console.log('API 기본 URL 업데이트:', url);
  }

  // 에러 핸들링
  private handleError(error: any): void {
    if (error.response) {
      console.error('API 응답 오류:', error.response.status, error.response.data);
    } else if (error.request) {
      console.error('네트워크 오류:', error.request);
    } else {
      console.error('요청 설정 오류:', error.message);
    }
  }
}

export const apiService = APIService.getInstance();
export { APIService }; 