import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  Alert,
  Dimensions,
  Animated,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import * as Haptics from 'expo-haptics';
import { VoiceService } from '../services/VoiceService';
import { APIService } from '../services/APIService';
import VoiceButton from '../components/VoiceButton';
import ResponseCard from '../components/ResponseCard';
import QuickCommandButton from '../components/QuickCommandButton';
import TaskHistory from '../components/TaskHistory';

const { width, height } = Dimensions.get('window');

interface CommandResponse {
  title: string;
  content: string;
  type: string;
  url?: string;
  speak?: string;
}

interface Task {
  id: string;
  title: string;
  time: string;
  icon: string;
  command: string;
}

export default function HomeScreen() {
  const [isListening, setIsListening] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [response, setResponse] = useState<CommandResponse | null>(null);
  const [recentTasks, setRecentTasks] = useState<Task[]>([]);
  const [connectionStatus, setConnectionStatus] = useState<'connected' | 'disconnected'>('disconnected');
  
  // 애니메이션 값들
  const pulseAnim = new Animated.Value(1);
  const waveAnim = new Animated.Value(0);

  useEffect(() => {
    // 연결 상태 확인
    checkConnection();
    // 최근 작업 로드
    loadRecentTasks();
  }, []);

  const checkConnection = async () => {
    try {
      const isConnected = await APIService.checkConnection();
      setConnectionStatus(isConnected ? 'connected' : 'disconnected');
    } catch (error) {
      setConnectionStatus('disconnected');
    }
  };

  const loadRecentTasks = async () => {
    try {
      const tasks = await APIService.getRecentTasks();
      setRecentTasks(tasks);
    } catch (error) {
      console.error('최근 작업 로드 실패:', error);
    }
  };

  const handleVoiceCommand = async (command: string) => {
    setIsProcessing(true);
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);

    try {
      // 백엔드 API 호출
      const apiResponse = await APIService.sendVoiceCommand(command);
      setResponse(apiResponse);
      
      // 작업 히스토리에 추가
      const newTask: Task = {
        id: Date.now().toString(),
        title: command,
        time: new Date().toLocaleTimeString('ko-KR'),
        icon: getTaskIcon(apiResponse.type),
        command: command,
      };
      
      setRecentTasks(prev => [newTask, ...prev.slice(0, 4)]);
      
      // 음성 피드백
      if (apiResponse.speak) {
        await VoiceService.speak(apiResponse.speak);
      }
      
      Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
      
    } catch (error) {
      console.error('명령 처리 오류:', error);
      Alert.alert('오류', '명령을 처리하는 중 오류가 발생했습니다.');
      Haptics.notificationAsync(Haptics.NotificationFeedbackType.Error);
    } finally {
      setIsProcessing(false);
    }
  };

  const getTaskIcon = (type: string): string => {
    const icons: { [key: string]: string } = {
      website: '🌐',
      email: '📧',
      schedule: '📅',
      document: '📄',
      general: '🎯',
    };
    return icons[type] || icons.general;
  };

  const handleQuickCommand = (command: string) => {
    handleVoiceCommand(command);
  };

  const handleReplayTask = (task: Task) => {
    handleVoiceCommand(task.command);
  };

  const clearResponse = () => {
    setResponse(null);
  };

  const startListening = async () => {
    try {
      setIsListening(true);
      Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
      
      // 펄스 애니메이션 시작
      Animated.loop(
        Animated.sequence([
          Animated.timing(pulseAnim, {
            toValue: 1.1,
            duration: 1000,
            useNativeDriver: true,
          }),
          Animated.timing(pulseAnim, {
            toValue: 1,
            duration: 1000,
            useNativeDriver: true,
          }),
        ])
      ).start();

      const result = await VoiceService.startListening();
      if (result) {
        handleVoiceCommand(result);
      }
    } catch (error) {
      console.error('음성 인식 오류:', error);
      Alert.alert('오류', '음성 인식에 실패했습니다.');
    } finally {
      setIsListening(false);
      pulseAnim.setValue(1);
    }
  };

  const stopListening = () => {
    VoiceService.stopListening();
    setIsListening(false);
    pulseAnim.setValue(1);
  };

  return (
    <ScrollView style={styles.container} showsVerticalScrollIndicator={false}>
      {/* 상태 표시 */}
      <View style={styles.statusContainer}>
        <View style={[styles.statusIndicator, styles[connectionStatus]]}>
          <Ionicons 
            name={connectionStatus === 'connected' ? 'wifi' : 'wifi-outline'} 
            size={16} 
            color="#ffffff" 
          />
          <Text style={styles.statusText}>
            {connectionStatus === 'connected' ? '연결됨' : '연결 끊김'}
          </Text>
        </View>
      </View>

      {/* 음성 명령 섹션 */}
      <View style={styles.voiceSection}>
        <VoiceButton
          isListening={isListening}
          isProcessing={isProcessing}
          onPress={isListening ? stopListening : startListening}
          pulseAnim={pulseAnim}
        />
        
        {(isListening || isProcessing) && (
          <Text style={styles.statusText}>
            {isListening ? '듣고 있습니다...' : '처리 중...'}
          </Text>
        )}
      </View>

      {/* AI 응답 */}
      {response && (
        <ResponseCard
          response={response}
          onClose={clearResponse}
        />
      )}

      {/* 빠른 명령 */}
      <View style={styles.quickCommandsSection}>
        <Text style={styles.sectionTitle}>빠른 명령</Text>
        <View style={styles.quickCommandsGrid}>
          <QuickCommandButton
            icon="🌐"
            title="웹사이트 생성"
            command="웹사이트 만들어줘"
            onPress={handleQuickCommand}
          />
          <QuickCommandButton
            icon="📧"
            title="이메일 작성"
            command="이메일 보내줘"
            onPress={handleQuickCommand}
          />
          <QuickCommandButton
            icon="📅"
            title="일정 관리"
            command="일정 관리해줘"
            onPress={handleQuickCommand}
          />
          <QuickCommandButton
            icon="📄"
            title="문서 요약"
            command="문서 요약해줘"
            onPress={handleQuickCommand}
          />
        </View>
      </View>

      {/* 최근 작업 */}
      {recentTasks.length > 0 && (
        <TaskHistory
          tasks={recentTasks}
          onReplayTask={handleReplayTask}
        />
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8fafc',
  },
  statusContainer: {
    padding: 16,
    alignItems: 'flex-end',
  },
  statusIndicator: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 20,
    gap: 4,
  },
  connected: {
    backgroundColor: '#22c55e',
  },
  disconnected: {
    backgroundColor: '#ef4444',
  },
  statusText: {
    color: '#ffffff',
    fontSize: 12,
    fontWeight: '600',
  },
  voiceSection: {
    alignItems: 'center',
    paddingVertical: 32,
  },
  quickCommandsSection: {
    padding: 16,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#1e293b',
    marginBottom: 16,
  },
  quickCommandsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 12,
  },
}); 