import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TouchableOpacity,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';

interface Task {
  id: string;
  title: string;
  time: string;
  icon: string;
  command: string;
}

interface TaskHistoryProps {
  tasks: Task[];
  onReplayTask: (task: Task) => void;
}

export default function TaskHistory({ tasks, onReplayTask }: TaskHistoryProps) {
  const renderTaskItem = ({ item }: { item: Task }) => (
    <TouchableOpacity
      style={styles.taskItem}
      onPress={() => onReplayTask(item)}
      activeOpacity={0.8}
    >
      <View style={styles.taskInfo}>
        <Text style={styles.taskIcon}>{item.icon}</Text>
        <View style={styles.taskDetails}>
          <Text style={styles.taskTitle}>{item.title}</Text>
          <Text style={styles.taskTime}>{item.time}</Text>
        </View>
      </View>
      <TouchableOpacity
        style={styles.replayButton}
        onPress={() => onReplayTask(item)}
      >
        <Ionicons name="play" size={16} color="#4ade80" />
      </TouchableOpacity>
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      <Text style={styles.sectionTitle}>최근 작업</Text>
      <FlatList
        data={tasks}
        renderItem={renderTaskItem}
        keyExtractor={(item) => item.id}
        showsVerticalScrollIndicator={false}
        scrollEnabled={false}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 16,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#1e293b',
    marginBottom: 16,
  },
  taskItem: {
    backgroundColor: '#ffffff',
    borderRadius: 12,
    padding: 16,
    marginBottom: 8,
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
  taskInfo: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  taskIcon: {
    fontSize: 20,
    marginRight: 12,
  },
  taskDetails: {
    flex: 1,
  },
  taskTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#1e293b',
    marginBottom: 4,
  },
  taskTime: {
    fontSize: 12,
    color: '#64748b',
  },
  replayButton: {
    padding: 8,
    borderRadius: 20,
    backgroundColor: '#f0fdf4',
  },
}); 