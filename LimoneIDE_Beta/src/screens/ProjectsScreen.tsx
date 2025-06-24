import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  Alert,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { APIService } from '../services/APIService';

interface Project {
  id: string;
  name: string;
  type: string;
  status: 'active' | 'completed' | 'archived';
  createdAt: string;
  lastModified: string;
  url?: string;
}

export default function ProjectsScreen() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadProjects();
  }, []);

  const loadProjects = async () => {
    try {
      setLoading(true);
      // 실제 구현에서는 API에서 프로젝트 목록 가져오기
      const demoProjects: Project[] = [
        {
          id: '1',
          name: '케이크 쇼핑몰',
          type: 'website',
          status: 'active',
          createdAt: '2025-01-27',
          lastModified: '2025-01-27',
          url: 'https://sites.google.com/view/cake-shop',
        },
        {
          id: '2',
          name: '회사 소개 이메일',
          type: 'email',
          status: 'completed',
          createdAt: '2025-01-26',
          lastModified: '2025-01-26',
        },
        {
          id: '3',
          name: '주간 회의 일정',
          type: 'schedule',
          status: 'active',
          createdAt: '2025-01-25',
          lastModified: '2025-01-25',
        },
      ];
      
      setProjects(demoProjects);
    } catch (error) {
      console.error('프로젝트 로드 실패:', error);
      Alert.alert('오류', '프로젝트 목록을 불러오는데 실패했습니다.');
    } finally {
      setLoading(false);
    }
  };

  const getProjectIcon = (type: string): string => {
    const icons: { [key: string]: string } = {
      website: '🌐',
      email: '📧',
      schedule: '📅',
      document: '📄',
    };
    return icons[type] || '📁';
  };

  const getStatusColor = (status: string): string => {
    const colors: { [key: string]: string } = {
      active: '#22c55e',
      completed: '#3b82f6',
      archived: '#6b7280',
    };
    return colors[status] || '#6b7280';
  };

  const getStatusText = (status: string): string => {
    const texts: { [key: string]: string } = {
      active: '활성',
      completed: '완료',
      archived: '보관',
    };
    return texts[status] || '알 수 없음';
  };

  const handleProjectPress = (project: Project) => {
    if (project.url) {
      Alert.alert(
        '프로젝트 열기',
        `${project.name}을(를) 브라우저에서 열까요?`,
        [
          { text: '취소', style: 'cancel' },
          { text: '열기', onPress: () => console.log('프로젝트 열기:', project.url) },
        ]
      );
    } else {
      Alert.alert('프로젝트 정보', project.name);
    }
  };

  const handleDeleteProject = (project: Project) => {
    Alert.alert(
      '프로젝트 삭제',
      `${project.name}을(를) 삭제하시겠습니까?`,
      [
        { text: '취소', style: 'cancel' },
        {
          text: '삭제',
          style: 'destructive',
          onPress: () => {
            setProjects(prev => prev.filter(p => p.id !== project.id));
          },
        },
      ]
    );
  };

  const renderProjectItem = ({ item }: { item: Project }) => (
    <TouchableOpacity
      style={styles.projectItem}
      onPress={() => handleProjectPress(item)}
    >
      <View style={styles.projectHeader}>
        <View style={styles.projectInfo}>
          <Text style={styles.projectIcon}>{getProjectIcon(item.type)}</Text>
          <View style={styles.projectDetails}>
            <Text style={styles.projectName}>{item.name}</Text>
            <Text style={styles.projectType}>{item.type}</Text>
          </View>
        </View>
        <View style={styles.projectActions}>
          <View style={[styles.statusBadge, { backgroundColor: getStatusColor(item.status) }]}>
            <Text style={styles.statusText}>{getStatusText(item.status)}</Text>
          </View>
          <TouchableOpacity
            style={styles.deleteButton}
            onPress={() => handleDeleteProject(item)}
          >
            <Ionicons name="trash-outline" size={20} color="#ef4444" />
          </TouchableOpacity>
        </View>
      </View>
      <View style={styles.projectFooter}>
        <Text style={styles.projectDate}>
          생성: {new Date(item.createdAt).toLocaleDateString('ko-KR')}
        </Text>
        <Text style={styles.projectDate}>
          수정: {new Date(item.lastModified).toLocaleDateString('ko-KR')}
        </Text>
      </View>
    </TouchableOpacity>
  );

  const renderEmptyState = () => (
    <View style={styles.emptyState}>
      <Ionicons name="folder-outline" size={64} color="#9ca3af" />
      <Text style={styles.emptyStateTitle}>프로젝트가 없습니다</Text>
      <Text style={styles.emptyStateSubtitle}>
        음성 명령으로 첫 번째 프로젝트를 만들어보세요
      </Text>
    </View>
  );

  return (
    <View style={styles.container}>
      <FlatList
        data={projects}
        renderItem={renderProjectItem}
        keyExtractor={(item) => item.id}
        contentContainerStyle={styles.listContainer}
        ListEmptyComponent={renderEmptyState}
        refreshing={loading}
        onRefresh={loadProjects}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8fafc',
  },
  listContainer: {
    padding: 16,
  },
  projectItem: {
    backgroundColor: '#ffffff',
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  projectHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  projectInfo: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  projectIcon: {
    fontSize: 24,
    marginRight: 12,
  },
  projectDetails: {
    flex: 1,
  },
  projectName: {
    fontSize: 16,
    fontWeight: '600',
    color: '#1e293b',
    marginBottom: 4,
  },
  projectType: {
    fontSize: 14,
    color: '#64748b',
    textTransform: 'capitalize',
  },
  projectActions: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  statusBadge: {
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 12,
  },
  statusText: {
    fontSize: 12,
    fontWeight: '600',
    color: '#ffffff',
  },
  deleteButton: {
    padding: 4,
  },
  projectFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    borderTopWidth: 1,
    borderTopColor: '#e2e8f0',
    paddingTop: 12,
  },
  projectDate: {
    fontSize: 12,
    color: '#64748b',
  },
  emptyState: {
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 64,
  },
  emptyStateTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#374151',
    marginTop: 16,
    marginBottom: 8,
  },
  emptyStateSubtitle: {
    fontSize: 14,
    color: '#6b7280',
    textAlign: 'center',
    lineHeight: 20,
  },
}); 