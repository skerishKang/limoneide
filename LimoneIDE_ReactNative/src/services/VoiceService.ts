import * as Speech from 'expo-speech';
import * as Permissions from 'expo-permissions';
import { Alert } from 'react-native';

class VoiceService {
  private static instance: VoiceService;
  private isInitialized = false;
  private isListening = false;

  static getInstance(): VoiceService {
    if (!VoiceService.instance) {
      VoiceService.instance = new VoiceService();
    }
    return VoiceService.instance;
  }

  async initialize(): Promise<void> {
    if (this.isInitialized) return;

    try {
      // 마이크 권한 요청
      const { status } = await Permissions.askAsync(Permissions.AUDIO_RECORDING);
      
      if (status !== 'granted') {
        Alert.alert(
          '권한 필요',
          '음성 인식을 위해 마이크 권한이 필요합니다.',
          [{ text: '확인' }]
        );
        return;
      }

      this.isInitialized = true;
      console.log('✅ VoiceService 초기화 완료');
    } catch (error) {
      console.error('❌ VoiceService 초기화 실패:', error);
      throw error;
    }
  }

  async startListening(): Promise<string | null> {
    if (!this.isInitialized) {
      await this.initialize();
    }

    if (this.isListening) {
      console.log('이미 음성 인식 중입니다.');
      return null;
    }

    this.isListening = true;

    try {
      // 실제 음성 인식 구현
      // Expo에서는 Web Speech API를 사용하거나 네이티브 모듈을 사용해야 함
      // 여기서는 데모용으로 시뮬레이션
      
      return new Promise((resolve) => {
        setTimeout(() => {
          this.isListening = false;
          // 데모용 응답
          const demoCommands = [
            '웹사이트 만들어줘',
            '이메일 보내줘',
            '일정 관리해줘',
            '문서 요약해줘'
          ];
          const randomCommand = demoCommands[Math.floor(Math.random() * demoCommands.length)];
          resolve(randomCommand);
        }, 3000);
      });
    } catch (error) {
      this.isListening = false;
      console.error('음성 인식 오류:', error);
      throw error;
    }
  }

  stopListening(): void {
    this.isListening = false;
    console.log('음성 인식 중지됨');
  }

  async speak(text: string): Promise<void> {
    try {
      await Speech.speak(text, {
        language: 'ko-KR',
        pitch: 1.0,
        rate: 0.9,
        onDone: () => {
          console.log('음성 합성 완료');
        },
        onError: (error) => {
          console.error('음성 합성 오류:', error);
        },
      });
    } catch (error) {
      console.error('음성 합성 실패:', error);
    }
  }

  async stopSpeaking(): Promise<void> {
    try {
      await Speech.stop();
    } catch (error) {
      console.error('음성 합성 중지 실패:', error);
    }
  }

  isCurrentlyListening(): boolean {
    return this.isListening;
  }

  // 음성 인식 정확도 개선을 위한 설정
  async configureVoiceRecognition(options: {
    language?: string;
    continuous?: boolean;
    interimResults?: boolean;
  }): Promise<void> {
    // 실제 구현에서는 음성 인식 엔진 설정
    console.log('음성 인식 설정:', options);
  }

  // 음성 합성 설정
  async configureSpeechSynthesis(options: {
    voice?: string;
    pitch?: number;
    rate?: number;
    volume?: number;
  }): Promise<void> {
    // 실제 구현에서는 음성 합성 엔진 설정
    console.log('음성 합성 설정:', options);
  }

  // 음성 명령 패턴 학습
  async learnCommandPattern(command: string, response: string): Promise<void> {
    // 실제 구현에서는 사용자 패턴 학습
    console.log('명령 패턴 학습:', { command, response });
  }

  // 음성 품질 분석
  async analyzeVoiceQuality(): Promise<{
    clarity: number;
    volume: number;
    backgroundNoise: number;
  }> {
    // 실제 구현에서는 음성 품질 분석
    return {
      clarity: 0.85,
      volume: 0.9,
      backgroundNoise: 0.1,
    };
  }
}

export const voiceService = VoiceService.getInstance();
export { VoiceService }; 