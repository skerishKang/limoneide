import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Switch,
  Alert,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { APIService } from '../services/APIService';
import { VoiceService } from '../services/VoiceService';
import { NotificationService } from '../services/NotificationService';

interface SettingItem {
  id: string;
  title: string;
  subtitle?: string;
  type: 'toggle' | 'button' | 'info';
  value?: boolean;
  onPress?: () => void;
  onToggle?: (value: boolean) => void;
  icon: string;
}

export default function SettingsScreen() {
  const [settings, setSettings] = useState<SettingItem[]>([]);
  const [userInsights, setUserInsights] = useState<any>(null);

  useEffect(() => {
    loadSettings();
    loadUserInsights();
  }, []);

  const loadSettings = () => {
    const defaultSettings: SettingItem[] = [
      {
        id: 'voice',
        title: '음성 인식',
        subtitle: '음성 명령 인식 활성화',
        type: 'toggle',
        value: true,
        icon: 'mic',
        onToggle: (value) => handleVoiceToggle(value),
      },
      {
        id: 'notifications',
        title: '알림',
        subtitle: '푸시 알림 및 로컬 알림',
        type: 'toggle',
        value: true,
        icon: 'notifications',
        onToggle: (value) => handleNotificationToggle(value),
      },
      {
        id: 'haptics',
        title: '햅틱 피드백',
        subtitle: '터치 시 진동 피드백',
        type: 'toggle',
        value: true,
        icon: 'phone-portrait',
        onToggle: (value) => handleHapticsToggle(value),
      },
      {
        id: 'offline',
        title: '오프라인 모드',
        subtitle: '네트워크 없이도 기본 기능 사용',
        type: 'toggle',
        value: true,
        icon: 'cloud-offline',
        onToggle: (value) => handleOfflineToggle(value),
      },
      {
        id: 'api',
        title: 'API 설정',
        subtitle: '백엔드 서버 연결 설정',
        type: 'button',
        icon: 'settings',
        onPress: () => handleAPISettings(),
      },
      {
        id: 'voice_settings',
        title: '음성 설정',
        subtitle: '음성 인식 및 합성 설정',
        type: 'button',
        icon: 'mic-circle',
        onPress: () => handleVoiceSettings(),
      },
      {
        id: 'clear_data',
        title: '데이터 초기화',
        subtitle: '모든 로컬 데이터 삭제',
        type: 'button',
        icon: 'trash',
        onPress: () => handleClearData(),
      },
      {
        id: 'about',
        title: '앱 정보',
        subtitle: 'LimoneIDE v1.0.0',
        type: 'info',
        icon: 'information-circle',
        onPress: () => handleAbout(),
      },
    ];

    setSettings(defaultSettings);
  };

  const loadUserInsights = async () => {
    try {
      const insights = await APIService.getUserInsights();
      setUserInsights(insights);
    } catch (error) {
      console.error('사용자 인사이트 로드 실패:', error);
    }
  };

  const handleVoiceToggle = async (value: boolean) => {
    try {
      if (value) {
        await VoiceService.initialize();
      }
      updateSetting('voice', value);
    } catch (error) {
      Alert.alert('오류', '음성 설정을 변경할 수 없습니다.');
    }
  };

  const handleNotificationToggle = async (value: boolean) => {
    try {
      if (value) {
        await NotificationService.initialize();
      }
      updateSetting('notifications', value);
    } catch (error) {
      Alert.alert('오류', '알림 설정을 변경할 수 없습니다.');
    }
  };

  const handleHapticsToggle = (value: boolean) => {
    updateSetting('haptics', value);
  };

  const handleOfflineToggle = (value: boolean) => {
    updateSetting('offline', value);
  };

  const handleAPISettings = () => {
    Alert.alert(
      'API 설정',
      '백엔드 서버 URL을 변경하시겠습니까?',
      [
        { text: '취소', style: 'cancel' },
        { text: '변경', onPress: () => console.log('API 설정 변경') },
      ]
    );
  };

  const handleVoiceSettings = () => {
    Alert.alert(
      '음성 설정',
      '음성 인식 언어, 속도, 피치 등을 설정할 수 있습니다.',
      [
        { text: '확인' },
      ]
    );
  };

  const handleClearData = () => {
    Alert.alert(
      '데이터 초기화',
      '모든 로컬 데이터가 삭제됩니다. 계속하시겠습니까?',
      [
        { text: '취소', style: 'cancel' },
        {
          text: '삭제',
          style: 'destructive',
          onPress: () => {
            // 실제 데이터 삭제 로직
            Alert.alert('완료', '데이터가 초기화되었습니다.');
          },
        },
      ]
    );
  };

  const handleAbout = () => {
    Alert.alert(
      'LimoneIDE',
      '음성 중심 모바일 자동화 플랫폼\n\n버전: 1.0.0\n개발: LimoneIDE Team\n\n"Think it, Say it, Done it"',
      [{ text: '확인' }]
    );
  };

  const updateSetting = (id: string, value: boolean) => {
    setSettings(prev =>
      prev.map(setting =>
        setting.id === id ? { ...setting, value } : setting
      )
    );
  };

  const renderSettingItem = (item: SettingItem) => (
    <View key={item.id} style={styles.settingItem}>
      <View style={styles.settingHeader}>
        <Ionicons name={item.icon as any} size={24} color="#4ade80" style={styles.settingIcon} />
        <View style={styles.settingInfo}>
          <Text style={styles.settingTitle}>{item.title}</Text>
          {item.subtitle && (
            <Text style={styles.settingSubtitle}>{item.subtitle}</Text>
          )}
        </View>
      </View>
      
      {item.type === 'toggle' && (
        <Switch
          value={item.value}
          onValueChange={item.onToggle}
          trackColor={{ false: '#e5e7eb', true: '#4ade80' }}
          thumbColor="#ffffff"
        />
      )}
      
      {item.type === 'button' && (
        <TouchableOpacity onPress={item.onPress}>
          <Ionicons name="chevron-forward" size={24} color="#9ca3af" />
        </TouchableOpacity>
      )}
      
      {item.type === 'info' && (
        <TouchableOpacity onPress={item.onPress}>
          <Ionicons name="chevron-forward" size={24} color="#9ca3af" />
        </TouchableOpacity>
      )}
    </View>
  );

  const renderUserInsights = () => {
    if (!userInsights) return null;

    return (
      <View style={styles.insightsSection}>
        <Text style={styles.sectionTitle}>사용자 인사이트</Text>
        <View style={styles.insightsCard}>
          <View style={styles.insightItem}>
            <Text style={styles.insightLabel}>총 대화 수</Text>
            <Text style={styles.insightValue}>{userInsights.totalConversations}</Text>
          </View>
          <View style={styles.insightItem}>
            <Text style={styles.insightLabel}>생산성 점수</Text>
            <Text style={styles.insightValue}>{userInsights.productivityScore}/100</Text>
          </View>
          <View style={styles.insightItem}>
            <Text style={styles.insightLabel}>선호 주제</Text>
            <Text style={styles.insightValue}>
              {userInsights.preferredTopics?.join(', ')}
            </Text>
          </View>
        </View>
      </View>
    );
  };

  return (
    <ScrollView style={styles.container} showsVerticalScrollIndicator={false}>
      {renderUserInsights()}
      
      <View style={styles.settingsSection}>
        <Text style={styles.sectionTitle}>설정</Text>
        {settings.map(renderSettingItem)}
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8fafc',
  },
  insightsSection: {
    padding: 16,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#1e293b',
    marginBottom: 16,
  },
  insightsCard: {
    backgroundColor: '#ffffff',
    borderRadius: 12,
    padding: 16,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  insightItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 8,
  },
  insightLabel: {
    fontSize: 14,
    color: '#64748b',
  },
  insightValue: {
    fontSize: 14,
    fontWeight: '600',
    color: '#1e293b',
  },
  settingsSection: {
    padding: 16,
  },
  settingItem: {
    backgroundColor: '#ffffff',
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  settingHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  settingIcon: {
    marginRight: 12,
  },
  settingInfo: {
    flex: 1,
  },
  settingTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#1e293b',
    marginBottom: 4,
  },
  settingSubtitle: {
    fontSize: 14,
    color: '#64748b',
  },
}); 