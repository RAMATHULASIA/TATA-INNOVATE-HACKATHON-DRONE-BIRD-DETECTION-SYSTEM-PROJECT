import React, { useState, useEffect } from 'react';
import { Layout, Menu, Avatar, Dropdown, Badge, Button, Space, Typography, Tooltip } from 'antd';
import {
  CodeOutlined,
  AnalysisOutlined,
  DashboardOutlined,
  SettingOutlined,
  UserOutlined,
  BellOutlined,
  MenuFoldOutlined,
  MenuUnfoldOutlined,
  CarOutlined,
  ThunderboltOutlined,
  SafetyOutlined
} from '@ant-design/icons';
import { motion } from 'framer-motion';
import './AppLayout.css';

const { Header, Sider, Content } = Layout;
const { Title, Text } = Typography;

interface AppLayoutProps {
  children: React.ReactNode;
  activeKey: string;
  onMenuSelect: (key: string) => void;
  apiStatus: 'loading' | 'running' | 'error';
}

const AppLayout: React.FC<AppLayoutProps> = ({ children, activeKey, onMenuSelect, apiStatus }) => {
  const [collapsed, setCollapsed] = useState(false);
  const [notifications, setNotifications] = useState(3);

  const menuItems = [
    {
      key: 'dashboard',
      icon: <DashboardOutlined />,
      label: 'Dashboard',
      description: 'Overview and metrics'
    },
    {
      key: 'generate',
      icon: <CodeOutlined />,
      label: 'Code Generation',
      description: 'AI-powered code creation'
    },
    {
      key: 'analyze',
      icon: <AnalysisOutlined />,
      label: 'Code Analysis',
      description: 'Embedded systems analysis'
    },
    {
      key: 'templates',
      icon: <ThunderboltOutlined />,
      label: 'Templates',
      description: 'Pre-built code patterns'
    },
    {
      key: 'settings',
      icon: <SettingOutlined />,
      label: 'Settings',
      description: 'Configuration and preferences'
    }
  ];

  const userMenuItems = [
    {
      key: 'profile',
      label: 'Profile Settings',
      icon: <UserOutlined />
    },
    {
      key: 'preferences',
      label: 'Preferences',
      icon: <SettingOutlined />
    },
    {
      type: 'divider' as const
    },
    {
      key: 'logout',
      label: 'Sign Out',
      icon: <UserOutlined />
    }
  ];

  const getStatusColor = () => {
    switch (apiStatus) {
      case 'running': return '#52c41a';
      case 'error': return '#ff4d4f';
      case 'loading': return '#1890ff';
      default: return '#d9d9d9';
    }
  };

  const getStatusText = () => {
    switch (apiStatus) {
      case 'running': return 'Online';
      case 'error': return 'Offline';
      case 'loading': return 'Connecting...';
      default: return 'Unknown';
    }
  };

  return (
    <Layout className="app-layout">
      <Sider
        trigger={null}
        collapsible
        collapsed={collapsed}
        className="app-sider"
        width={280}
        collapsedWidth={80}
      >
        <motion.div
          className="logo-container"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <CarOutlined className="logo-icon" />
          {!collapsed && (
            <div className="logo-text">
              <Title level={4} className="logo-title">AI Co-pilot</Title>
              <Text className="logo-subtitle">Embedded Design</Text>
            </div>
          )}
        </motion.div>

        <Menu
          theme="dark"
          mode="inline"
          selectedKeys={[activeKey]}
          className="app-menu"
          onClick={({ key }) => onMenuSelect(key)}
        >
          {menuItems.map((item, index) => (
            <Menu.Item key={item.key} icon={item.icon} className="menu-item">
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.3, delay: index * 0.1 }}
              >
                <div className="menu-content">
                  <span className="menu-label">{item.label}</span>
                  {!collapsed && (
                    <Text className="menu-description">{item.description}</Text>
                  )}
                </div>
              </motion.div>
            </Menu.Item>
          ))}
        </Menu>

        <div className="sider-footer">
          <div className="status-indicator">
            <div 
              className="status-dot" 
              style={{ backgroundColor: getStatusColor() }}
            />
            {!collapsed && (
              <Text className="status-text">{getStatusText()}</Text>
            )}
          </div>
        </div>
      </Sider>

      <Layout className="site-layout">
        <Header className="app-header">
          <div className="header-left">
            <Button
              type="text"
              icon={collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
              onClick={() => setCollapsed(!collapsed)}
              className="collapse-btn"
            />
            
            <div className="header-title">
              <Title level={3} className="page-title">
                {menuItems.find(item => item.key === activeKey)?.label || 'Dashboard'}
              </Title>
              <Text className="page-subtitle">
                {menuItems.find(item => item.key === activeKey)?.description}
              </Text>
            </div>
          </div>

          <div className="header-right">
            <Space size="middle">
              <Tooltip title="Safety Level: ASIL-B">
                <Badge dot color="orange">
                  <SafetyOutlined className="header-icon" />
                </Badge>
              </Tooltip>

              <Tooltip title="Notifications">
                <Badge count={notifications} size="small">
                  <BellOutlined className="header-icon" />
                </Badge>
              </Tooltip>

              <Dropdown menu={{ items: userMenuItems }} placement="bottomRight">
                <div className="user-profile">
                  <Avatar icon={<UserOutlined />} />
                  <div className="user-info">
                    <Text strong>Developer</Text>
                    <Text type="secondary">Embedded Engineer</Text>
                  </div>
                </div>
              </Dropdown>
            </Space>
          </div>
        </Header>

        <Content className="app-content">
          <motion.div
            key={activeKey}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            className="content-wrapper"
          >
            {children}
          </motion.div>
        </Content>
      </Layout>
    </Layout>
  );
};

export default AppLayout;
