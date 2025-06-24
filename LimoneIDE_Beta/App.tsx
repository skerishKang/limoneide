import React from 'react';
import { StatusBar } from 'expo-status-bar';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import { Ionicons } from '@expo/vector-icons';

// Screens
import HomeScreen from './src/screens/HomeScreen';
import ProjectsScreen from './src/screens/ProjectsScreen';
import SettingsScreen from './src/screens/SettingsScreen';

// Services
import { VoiceService } from './src/services/VoiceService';
import { NotificationService } from './src/services/NotificationService';

const Tab = createBottomTabNavigator();

export default function App() {
  React.useEffect(() => {
    // 앱 시작 시 서비스 초기화
    initializeServices();
  }, []);

  const initializeServices = async () => {
    try {
      // 음성 서비스 초기화
      await VoiceService.initialize();
      
      // 알림 서비스 초기화
      await NotificationService.initialize();
      
      console.log('✅ LimoneIDE 서비스 초기화 완료');
    } catch (error) {
      console.error('❌ 서비스 초기화 실패:', error);
    }
  };

  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <SafeAreaProvider>
        <NavigationContainer>
          <Tab.Navigator
            screenOptions={({ route }) => ({
              tabBarIcon: ({ focused, color, size }) => {
                let iconName: keyof typeof Ionicons.glyphMap;

                if (route.name === 'Home') {
                  iconName = focused ? 'home' : 'home-outline';
                } else if (route.name === 'Projects') {
                  iconName = focused ? 'folder' : 'folder-outline';
                } else if (route.name === 'Settings') {
                  iconName = focused ? 'settings' : 'settings-outline';
                } else {
                  iconName = 'help-outline';
                }

                return <Ionicons name={iconName} size={size} color={color} />;
              },
              tabBarActiveTintColor: '#4ade80',
              tabBarInactiveTintColor: 'gray',
              tabBarStyle: {
                backgroundColor: '#ffffff',
                borderTopWidth: 1,
                borderTopColor: '#e5e7eb',
                paddingBottom: 5,
                paddingTop: 5,
                height: 60,
              },
              headerStyle: {
                backgroundColor: '#4ade80',
              },
              headerTintColor: '#ffffff',
              headerTitleStyle: {
                fontWeight: 'bold',
              },
            })}
          >
            <Tab.Screen 
              name="Home" 
              component={HomeScreen}
              options={{
                title: 'LimoneIDE',
                headerTitle: () => (
                  <React.Fragment>
                    <Ionicons name="mic" size={24} color="#ffffff" style={{ marginRight: 8 }} />
                    <span style={{ color: '#ffffff', fontWeight: 'bold', fontSize: 18 }}>
                      LimoneIDE
                    </span>
                  </React.Fragment>
                ),
              }}
            />
            <Tab.Screen 
              name="Projects" 
              component={ProjectsScreen}
              options={{ title: '프로젝트' }}
            />
            <Tab.Screen 
              name="Settings" 
              component={SettingsScreen}
              options={{ title: '설정' }}
            />
          </Tab.Navigator>
        </NavigationContainer>
        <StatusBar style="light" />
      </SafeAreaProvider>
    </GestureHandlerRootView>
  );
} 