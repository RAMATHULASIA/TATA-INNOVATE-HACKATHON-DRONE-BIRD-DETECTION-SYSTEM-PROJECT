import React, { useState, useEffect } from 'react';
import { ConfigProvider, notification, Spin } from 'antd';
import { motion, AnimatePresence } from 'framer-motion';
import axios from 'axios';

// Contexts
import { ThemeProvider, useTheme, getAntdThemeConfig } from './contexts/ThemeContext';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import { ProjectProvider } from './contexts/ProjectContext';

// Components
import AppLayout from './components/Layout/AppLayout';
import Dashboard from './components/Dashboard/Dashboard';
import CodeGeneration from './components/CodeGeneration/CodeGeneration';
import CodeAnalysis from './components/CodeAnalysis/CodeAnalysis';
import LoginForm from './components/Auth/LoginForm';
import ThemeCustomizer from './components/Settings/ThemeCustomizer';

import './App.css';

// Types
interface ApiStatus {
  status: 'loading' | 'running' | 'error';
  message: string;
  version?: string;
}

// Main App Component (wrapped with providers)
const AppContent: React.FC = () => {
  const [activeKey, setActiveKey] = useState('dashboard');
  const [apiStatus, setApiStatus] = useState<ApiStatus>({
    status: 'loading',
    message: 'Initializing...'
  });
  const [showRegister, setShowRegister] = useState(false);

  // Available options
  const [platforms, setPlatforms] = useState<string[]>([]);
  const [templates, setTemplates] = useState<string[]>([]);

  // Hooks
  const { isAuthenticated, isLoading: authLoading } = useAuth();
  const { currentTheme, themeConfig, isDarkMode, customColors, fontSize, compactMode } = useTheme();

  useEffect(() => {
    initializeApp();
  }, []);

  const initializeApp = async () => {
    try {
      // Check API status
      await checkApiStatus();

      // Load initial data
      await Promise.all([
        loadPlatforms(),
        loadTemplates()
      ]);

      // Show success notification
      notification.success({
        message: 'AI Co-pilot Ready',
        description: 'All systems initialized successfully',
        placement: 'topRight',
        duration: 3
      });

    } catch (error) {
      console.error('Initialization failed:', error);
      notification.error({
        message: 'Initialization Failed',
        description: 'Some features may not work properly',
        placement: 'topRight'
      });
    }
  };

  const checkApiStatus = async () => {
    try {
      const response = await axios.get('/api/status');
      setApiStatus({
        status: response.data.status === 'running' ? 'running' : 'loading',
        message: response.data.message,
        version: response.data.version
      });
    } catch (error) {
      setApiStatus({
        status: 'error',
        message: 'Failed to connect to API'
      });
    }
  };

  const loadPlatforms = async () => {
    try {
      const response = await axios.get('/api/platforms');
      setPlatforms(response.data.platforms || []);
    } catch (error) {
      console.error('Failed to load platforms:', error);
      setPlatforms(['ARM Cortex-M', 'AVR', 'x86', 'RISC-V']); // Fallback
    }
  };

  const loadTemplates = async () => {
    try {
      const response = await axios.get('/api/templates');
      setTemplates(response.data.templates || []);
    } catch (error) {
      console.error('Failed to load templates:', error);
      setTemplates(['can_driver', 'state_machine', 'interrupt_handler']); // Fallback
    }
  };

  const handleMenuSelect = (key: string) => {
    setActiveKey(key);
  };

  const handleNavigate = (key: string) => {
    setActiveKey(key);
  };

  const renderContent = () => {
    switch (activeKey) {
      case 'dashboard':
        return <Dashboard onNavigate={handleNavigate} />;
      case 'generate':
        return <CodeGeneration platforms={platforms} templates={templates} />;
      case 'analyze':
        return <CodeAnalysis />;
      case 'templates':
        return <div>Templates component coming soon...</div>;
      case 'settings':
        return <ThemeCustomizer />;
      default:
        return <Dashboard onNavigate={handleNavigate} />;
    }
  };

  // Show loading spinner while authenticating
  if (authLoading) {
    return (
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh',
        background: 'linear-gradient(135deg, #1B4F72 0%, #2E86AB 50%, #A23B72 100%)'
      }}>
        <Spin size="large" />
      </div>
    );
  }

  // Show login form if not authenticated
  if (!isAuthenticated) {
    return showRegister ? (
      <div>Register form coming soon...</div>
    ) : (
      <LoginForm onSwitchToRegister={() => setShowRegister(true)} />
    );
  }

  return (
    <ConfigProvider
      theme={getAntdThemeConfig(themeConfig, isDarkMode, customColors, fontSize, compactMode)}
    >
      <div className={`app ${isDarkMode ? 'dark' : 'light'} theme-${currentTheme}`}>
        <AppLayout
          activeKey={activeKey}
          onMenuSelect={handleMenuSelect}
          apiStatus={apiStatus.status}
        >
          <AnimatePresence mode="wait">
            <motion.div
              key={activeKey}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
            >
              {renderContent()}
            </motion.div>
          </AnimatePresence>
        </AppLayout>
      </div>
    </ConfigProvider>
  );
};

// Main App with all providers
const App: React.FC = () => {
  useEffect(() => {
    // Register service worker for PWA functionality
    if ('serviceWorker' in navigator) {
      window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
          .then((registration) => {
            console.log('SW registered: ', registration);
          })
          .catch((registrationError) => {
            console.log('SW registration failed: ', registrationError);
          });
      });
    }

    // Request notification permission
    if ('Notification' in window && Notification.permission === 'default') {
      Notification.requestPermission().then((permission) => {
        if (permission === 'granted') {
          console.log('Notification permission granted');
        }
      });
    }
  }, []);

  return (
    <ThemeProvider>
      <AuthProvider>
        <ProjectProvider>
          <AppContent />
        </ProjectProvider>
      </AuthProvider>
    </ThemeProvider>
  );
};

export default App;
