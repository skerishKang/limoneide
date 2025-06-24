import * as Notifications from 'expo-notifications';
import * as Permissions from 'expo-permissions';
import { Platform } from 'react-native';

interface NotificationData {
  title: string;
  body: string;
  data?: any;
  sound?: boolean;
  priority?: 'default' | 'normal' | 'high';
}

class NotificationService {
  private static instance: NotificationService;
  private isInitialized = false;
  private expoPushToken: string | null = null;

  static getInstance(): NotificationService {
    if (!NotificationService.instance) {
      NotificationService.instance = new NotificationService();
    }
    return NotificationService.instance;
  }

  async initialize(): Promise<void> {
    if (this.isInitialized) return;

    try {
      // 알림 권한 요청
      const { status: existingStatus } = await Notifications.getPermissionsAsync();
      let finalStatus = existingStatus;
      
      if (existingStatus !== 'granted') {
        const { status } = await Notifications.requestPermissionsAsync();
        finalStatus = status;
      }
      
      if (finalStatus !== 'granted') {
        console.log('알림 권한이 거부되었습니다.');
        return;
      }

      // 알림 핸들러 설정
      Notifications.setNotificationHandler({
        handleNotification: async () => ({
          shouldShowAlert: true,
          shouldPlaySound: true,
          shouldSetBadge: false,
        }),
      });

      // Expo 푸시 토큰 가져오기
      if (Platform.OS !== 'web') {
        const token = await Notifications.getExpoPushTokenAsync({
          projectId: 'your-project-id', // Expo 프로젝트 ID
        });
        this.expoPushToken = token.data;
        console.log('Expo 푸시 토큰:', this.expoPushToken);
      }

      this.isInitialized = true;
      console.log('✅ NotificationService 초기화 완료');
    } catch (error) {
      console.error('❌ NotificationService 초기화 실패:', error);
      throw error;
    }
  }

  async scheduleLocalNotification(notification: NotificationData, trigger?: any): Promise<string> {
    if (!this.isInitialized) {
      await this.initialize();
    }

    try {
      const notificationId = await Notifications.scheduleNotificationAsync({
        content: {
          title: notification.title,
          body: notification.body,
          data: notification.data || {},
          sound: notification.sound !== false,
          priority: notification.priority || 'default',
        },
        trigger: trigger || null, // 즉시 알림
      });

      console.log('로컬 알림 예약됨:', notificationId);
      return notificationId;
    } catch (error) {
      console.error('로컬 알림 예약 실패:', error);
      throw error;
    }
  }

  async sendImmediateNotification(notification: NotificationData): Promise<string> {
    return this.scheduleLocalNotification(notification);
  }

  async sendDelayedNotification(notification: NotificationData, delaySeconds: number): Promise<string> {
    return this.scheduleLocalNotification(notification, {
      seconds: delaySeconds,
    });
  }

  async sendScheduledNotification(notification: NotificationData, date: Date): Promise<string> {
    return this.scheduleLocalNotification(notification, {
      date: date,
    });
  }

  async sendRepeatingNotification(notification: NotificationData, intervalSeconds: number): Promise<string> {
    return this.scheduleLocalNotification(notification, {
      seconds: intervalSeconds,
      repeats: true,
    });
  }

  async cancelNotification(notificationId: string): Promise<void> {
    try {
      await Notifications.cancelScheduledNotificationAsync(notificationId);
      console.log('알림 취소됨:', notificationId);
    } catch (error) {
      console.error('알림 취소 실패:', error);
    }
  }

  async cancelAllNotifications(): Promise<void> {
    try {
      await Notifications.cancelAllScheduledNotificationsAsync();
      console.log('모든 알림 취소됨');
    } catch (error) {
      console.error('모든 알림 취소 실패:', error);
    }
  }

  async getScheduledNotifications(): Promise<Notifications.NotificationRequest[]> {
    try {
      const notifications = await Notifications.getAllScheduledNotificationsAsync();
      return notifications;
    } catch (error) {
      console.error('예약된 알림 조회 실패:', error);
      return [];
    }
  }

  // 음성 명령 완료 알림
  async sendCommandCompletionNotification(command: string, result: string): Promise<void> {
    const notification: NotificationData = {
      title: '명령 완료',
      body: `"${command}" 명령이 성공적으로 처리되었습니다.`,
      data: { command, result },
      sound: true,
      priority: 'high',
    };

    await this.sendImmediateNotification(notification);
  }

  // 웹사이트 생성 완료 알림
  async sendWebsiteCreationNotification(url: string): Promise<void> {
    const notification: NotificationData = {
      title: '웹사이트 생성 완료',
      body: '요청하신 웹사이트가 성공적으로 생성되었습니다.',
      data: { url },
      sound: true,
      priority: 'high',
    };

    await this.sendImmediateNotification(notification);
  }

  // 일정 알림
  async sendScheduleReminderNotification(title: string, time: string): Promise<void> {
    const notification: NotificationData = {
      title: '일정 알림',
      body: `${title} - ${time}`,
      data: { title, time },
      sound: true,
      priority: 'high',
    };

    await this.sendImmediateNotification(notification);
  }

  // 오프라인 모드 알림
  async sendOfflineModeNotification(): Promise<void> {
    const notification: NotificationData = {
      title: '오프라인 모드',
      body: '네트워크 연결이 끊어져 오프라인 모드로 전환되었습니다.',
      data: { mode: 'offline' },
      sound: false,
      priority: 'normal',
    };

    await this.sendImmediateNotification(notification);
  }

  // 연결 복구 알림
  async sendConnectionRestoredNotification(): Promise<void> {
    const notification: NotificationData = {
      title: '연결 복구',
      body: '네트워크 연결이 복구되어 온라인 모드로 전환되었습니다.',
      data: { mode: 'online' },
      sound: true,
      priority: 'normal',
    };

    await this.sendImmediateNotification(notification);
  }

  // 사용자 인사이트 알림
  async sendInsightNotification(insight: string): Promise<void> {
    const notification: NotificationData = {
      title: 'AI 인사이트',
      body: insight,
      data: { type: 'insight' },
      sound: false,
      priority: 'normal',
    };

    await this.sendImmediateNotification(notification);
  }

  // 푸시 알림 전송 (서버에서)
  async sendPushNotification(userIds: string[], notification: NotificationData): Promise<void> {
    if (!this.expoPushToken) {
      console.log('푸시 토큰이 없습니다.');
      return;
    }

    try {
      // 실제 구현에서는 서버 API를 통해 푸시 알림 전송
      console.log('푸시 알림 전송:', { userIds, notification });
    } catch (error) {
      console.error('푸시 알림 전송 실패:', error);
    }
  }

  // 알림 설정 관리
  async updateNotificationSettings(settings: {
    sound?: boolean;
    vibration?: boolean;
    badge?: boolean;
    priority?: 'default' | 'normal' | 'high';
  }): Promise<void> {
    // 실제 구현에서는 알림 설정 업데이트
    console.log('알림 설정 업데이트:', settings);
  }

  // 알림 통계
  async getNotificationStats(): Promise<{
    totalSent: number;
    totalReceived: number;
    successRate: number;
  }> {
    // 실제 구현에서는 알림 통계 수집
    return {
      totalSent: 0,
      totalReceived: 0,
      successRate: 0,
    };
  }

  getExpoPushToken(): string | null {
    return this.expoPushToken;
  }

  isServiceInitialized(): boolean {
    return this.isInitialized;
  }
}

export const notificationService = NotificationService.getInstance();
export { NotificationService }; 