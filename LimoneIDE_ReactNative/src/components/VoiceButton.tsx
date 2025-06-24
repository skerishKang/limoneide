import React from 'react';
import {
  TouchableOpacity,
  StyleSheet,
  Animated,
  View,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';

interface VoiceButtonProps {
  isListening: boolean;
  isProcessing: boolean;
  onPress: () => void;
  pulseAnim: Animated.Value;
}

export default function VoiceButton({
  isListening,
  isProcessing,
  onPress,
  pulseAnim,
}: VoiceButtonProps) {
  const getButtonColor = () => {
    if (isProcessing) return ['#f59e0b', '#d97706'];
    if (isListening) return ['#ef4444', '#dc2626'];
    return ['#4ade80', '#22c55e'];
  };

  const getIcon = () => {
    if (isProcessing) return 'hourglass';
    if (isListening) return 'mic';
    return 'mic-outline';
  };

  const getIconColor = () => {
    if (isProcessing) return '#ffffff';
    if (isListening) return '#ffffff';
    return '#ffffff';
  };

  return (
    <View style={styles.container}>
      <Animated.View
        style={[
          styles.pulseRing,
          {
            transform: [{ scale: pulseAnim }],
            opacity: isListening ? 0.3 : 0,
          },
        ]}
      />
      
      <TouchableOpacity
        style={styles.button}
        onPress={onPress}
        activeOpacity={0.8}
        disabled={isProcessing}
      >
        <LinearGradient
          colors={getButtonColor()}
          style={styles.gradient}
          start={{ x: 0, y: 0 }}
          end={{ x: 1, y: 1 }}
        >
          <Ionicons
            name={getIcon() as any}
            size={32}
            color={getIconColor()}
          />
        </LinearGradient>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    justifyContent: 'center',
    position: 'relative',
  },
  pulseRing: {
    position: 'absolute',
    width: 120,
    height: 120,
    borderRadius: 60,
    backgroundColor: '#4ade80',
  },
  button: {
    width: 80,
    height: 80,
    borderRadius: 40,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 4,
    },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 8,
  },
  gradient: {
    width: '100%',
    height: '100%',
    borderRadius: 40,
    alignItems: 'center',
    justifyContent: 'center',
  },
}); 