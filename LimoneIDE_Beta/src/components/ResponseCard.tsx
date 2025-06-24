import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Linking,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';

interface CommandResponse {
  title: string;
  content: string;
  type: string;
  url?: string;
  speak?: string;
}

interface ResponseCardProps {
  response: CommandResponse;
  onClose: () => void;
}

export default function ResponseCard({ response, onClose }: ResponseCardProps) {
  const handleOpenUrl = async () => {
    if (response.url) {
      try {
        await Linking.openURL(response.url);
      } catch (error) {
        console.error('URL 열기 실패:', error);
      }
    }
  };

  const getTypeIcon = (type: string): string => {
    const icons: { [key: string]: string } = {
      website: '🌐',
      email: '📧',
      schedule: '📅',
      document: '📄',
      general: '🎯',
    };
    return icons[type] || icons.general;
  };

  const getTypeColor = (type: string): string => {
    const colors: { [key: string]: string } = {
      website: '#3b82f6',
      email: '#8b5cf6',
      schedule: '#f59e0b',
      document: '#10b981',
      general: '#6b7280',
    };
    return colors[type] || colors.general;
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <View style={styles.titleContainer}>
          <Text style={styles.typeIcon}>{getTypeIcon(response.type)}</Text>
          <Text style={styles.title}>{response.title}</Text>
        </View>
        <TouchableOpacity onPress={onClose} style={styles.closeButton}>
          <Ionicons name="close" size={24} color="#6b7280" />
        </TouchableOpacity>
      </View>
      
      <View style={styles.content}>
        <Text style={styles.contentText}>{response.content}</Text>
      </View>
      
      {response.url && (
        <TouchableOpacity
          style={[styles.urlButton, { backgroundColor: getTypeColor(response.type) }]}
          onPress={handleOpenUrl}
        >
          <Ionicons name="open-outline" size={20} color="#ffffff" />
          <Text style={styles.urlButtonText}>결과 보기</Text>
        </TouchableOpacity>
      )}
      
      <View style={[styles.typeIndicator, { backgroundColor: getTypeColor(response.type) }]}>
        <Text style={styles.typeText}>{response.type}</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#ffffff',
    borderRadius: 16,
    margin: 16,
    padding: 20,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 4,
    },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 6,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  titleContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  typeIcon: {
    fontSize: 24,
    marginRight: 12,
  },
  title: {
    fontSize: 18,
    fontWeight: '600',
    color: '#1e293b',
    flex: 1,
  },
  closeButton: {
    padding: 4,
  },
  content: {
    marginBottom: 16,
  },
  contentText: {
    fontSize: 16,
    color: '#374151',
    lineHeight: 24,
  },
  urlButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 12,
    paddingHorizontal: 20,
    borderRadius: 8,
    marginBottom: 16,
  },
  urlButtonText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: '600',
    marginLeft: 8,
  },
  typeIndicator: {
    alignSelf: 'flex-start',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 16,
  },
  typeText: {
    color: '#ffffff',
    fontSize: 12,
    fontWeight: '600',
    textTransform: 'uppercase',
  },
}); 