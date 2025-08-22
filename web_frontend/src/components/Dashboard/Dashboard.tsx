import React, { useState, useEffect } from 'react';
import { Row, Col, Card, Statistic, Progress, Timeline, List, Tag, Avatar, Button, Space, Typography } from 'antd';
import {
  CodeOutlined,
  BugOutlined,
  SafetyOutlined,
  ThunderboltOutlined,
  CarOutlined,
  ClockCircleOutlined,
  CheckCircleOutlined,
  ExclamationCircleOutlined,
  TrophyOutlined,
  RocketOutlined
} from '@ant-design/icons';
import { LineChart, Line, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { motion } from 'framer-motion';
import './Dashboard.css';

const { Title, Text, Paragraph } = Typography;

interface DashboardProps {
  onNavigate: (key: string) => void;
}

const Dashboard: React.FC<DashboardProps> = ({ onNavigate }) => {
  const [stats, setStats] = useState({
    totalGenerated: 1247,
    totalAnalyzed: 892,
    safetyCompliance: 94,
    activeProjects: 12
  });

  const [recentActivity, setRecentActivity] = useState([
    {
      id: 1,
      type: 'generate',
      title: 'CAN Message Handler Generated',
      description: 'Generated brake system CAN handler for ARM Cortex-M',
      time: '2 minutes ago',
      status: 'success'
    },
    {
      id: 2,
      type: 'analyze',
      title: 'Code Analysis Completed',
      description: 'Analyzed engine control module - 3 warnings found',
      time: '15 minutes ago',
      status: 'warning'
    },
    {
      id: 3,
      type: 'generate',
      title: 'AUTOSAR Component Created',
      description: 'Generated transmission control component',
      time: '1 hour ago',
      status: 'success'
    },
    {
      id: 4,
      type: 'analyze',
      title: 'Safety Analysis Complete',
      description: 'MISRA C compliance check passed',
      time: '2 hours ago',
      status: 'success'
    }
  ]);

  const performanceData = [
    { name: 'Mon', generated: 45, analyzed: 32 },
    { name: 'Tue', generated: 52, analyzed: 41 },
    { name: 'Wed', generated: 38, analyzed: 28 },
    { name: 'Thu', generated: 61, analyzed: 45 },
    { name: 'Fri', generated: 55, analyzed: 38 },
    { name: 'Sat', generated: 28, analyzed: 22 },
    { name: 'Sun', generated: 33, analyzed: 25 }
  ];

  const platformData = [
    { name: 'ARM Cortex-M', value: 45, color: '#1890ff' },
    { name: 'AVR', value: 25, color: '#52c41a' },
    { name: 'x86', value: 20, color: '#faad14' },
    { name: 'RISC-V', value: 10, color: '#722ed1' }
  ];

  const quickActions = [
    {
      title: 'Generate CAN Handler',
      description: 'Create automotive CAN communication code',
      icon: <CarOutlined />,
      color: '#1890ff',
      action: () => onNavigate('generate')
    },
    {
      title: 'Analyze Code',
      description: 'Check embedded constraints and safety',
      icon: <BugOutlined />,
      color: '#52c41a',
      action: () => onNavigate('analyze')
    },
    {
      title: 'AUTOSAR Template',
      description: 'Generate AUTOSAR component',
      icon: <SafetyOutlined />,
      color: '#faad14',
      action: () => onNavigate('templates')
    },
    {
      title: 'State Machine',
      description: 'Create embedded state machine',
      icon: <ThunderboltOutlined />,
      color: '#722ed1',
      action: () => onNavigate('templates')
    }
  ];

  const getActivityIcon = (type: string) => {
    switch (type) {
      case 'generate': return <CodeOutlined style={{ color: '#1890ff' }} />;
      case 'analyze': return <BugOutlined style={{ color: '#52c41a' }} />;
      default: return <ClockCircleOutlined />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'success': return 'success';
      case 'warning': return 'warning';
      case 'error': return 'error';
      default: return 'default';
    }
  };

  return (
    <div className="dashboard">
      {/* Welcome Section */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="welcome-section"
      >
        <Card className="welcome-card">
          <Row align="middle">
            <Col flex="auto">
              <Title level={2} className="welcome-title">
                Welcome back! 👋
              </Title>
              <Paragraph className="welcome-text">
                Your AI co-pilot is ready to help you design embedded software for smart vehicles.
                Generate code, analyze existing implementations, and ensure safety compliance.
              </Paragraph>
            </Col>
            <Col>
              <div className="welcome-stats">
                <Statistic
                  title="Today's Generations"
                  value={23}
                  prefix={<RocketOutlined />}
                  valueStyle={{ color: '#1890ff' }}
                />
              </div>
            </Col>
          </Row>
        </Card>
      </motion.div>

      {/* Statistics Cards */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
      >
        <Row gutter={[24, 24]} className="stats-row">
          <Col xs={24} sm={12} lg={6}>
            <Card className="stat-card">
              <Statistic
                title="Code Generated"
                value={stats.totalGenerated}
                prefix={<CodeOutlined />}
                valueStyle={{ color: '#1890ff' }}
                suffix="files"
              />
              <div className="stat-trend">
                <Text type="success">↗ 12% from last week</Text>
              </div>
            </Card>
          </Col>
          <Col xs={24} sm={12} lg={6}>
            <Card className="stat-card">
              <Statistic
                title="Code Analyzed"
                value={stats.totalAnalyzed}
                prefix={<BugOutlined />}
                valueStyle={{ color: '#52c41a' }}
                suffix="files"
              />
              <div className="stat-trend">
                <Text type="success">↗ 8% from last week</Text>
              </div>
            </Card>
          </Col>
          <Col xs={24} sm={12} lg={6}>
            <Card className="stat-card">
              <Statistic
                title="Safety Compliance"
                value={stats.safetyCompliance}
                prefix={<SafetyOutlined />}
                valueStyle={{ color: '#faad14' }}
                suffix="%"
              />
              <Progress
                percent={stats.safetyCompliance}
                showInfo={false}
                strokeColor="#faad14"
                size="small"
                className="stat-progress"
              />
            </Card>
          </Col>
          <Col xs={24} sm={12} lg={6}>
            <Card className="stat-card">
              <Statistic
                title="Active Projects"
                value={stats.activeProjects}
                prefix={<TrophyOutlined />}
                valueStyle={{ color: '#722ed1' }}
              />
              <div className="stat-trend">
                <Text type="secondary">3 completed today</Text>
              </div>
            </Card>
          </Col>
        </Row>
      </motion.div>

      {/* Charts and Activity */}
      <Row gutter={[24, 24]} className="charts-row">
        <Col xs={24} lg={16}>
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
          >
            <Card title="Weekly Performance" className="chart-card">
              <ResponsiveContainer width="100%" height={300}>
                <AreaChart data={performanceData}>
                  <defs>
                    <linearGradient id="colorGenerated" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#1890ff" stopOpacity={0.8}/>
                      <stop offset="95%" stopColor="#1890ff" stopOpacity={0.1}/>
                    </linearGradient>
                    <linearGradient id="colorAnalyzed" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#52c41a" stopOpacity={0.8}/>
                      <stop offset="95%" stopColor="#52c41a" stopOpacity={0.1}/>
                    </linearGradient>
                  </defs>
                  <XAxis dataKey="name" />
                  <YAxis />
                  <CartesianGrid strokeDasharray="3 3" />
                  <Tooltip />
                  <Area
                    type="monotone"
                    dataKey="generated"
                    stroke="#1890ff"
                    fillOpacity={1}
                    fill="url(#colorGenerated)"
                    name="Generated"
                  />
                  <Area
                    type="monotone"
                    dataKey="analyzed"
                    stroke="#52c41a"
                    fillOpacity={1}
                    fill="url(#colorAnalyzed)"
                    name="Analyzed"
                  />
                </AreaChart>
              </ResponsiveContainer>
            </Card>
          </motion.div>
        </Col>

        <Col xs={24} lg={8}>
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
          >
            <Card title="Platform Distribution" className="chart-card">
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={platformData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={100}
                    paddingAngle={5}
                    dataKey="value"
                  >
                    {platformData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
              <div className="platform-legend">
                {platformData.map((item, index) => (
                  <div key={index} className="legend-item">
                    <div
                      className="legend-color"
                      style={{ backgroundColor: item.color }}
                    />
                    <Text>{item.name}</Text>
                    <Text type="secondary">{item.value}%</Text>
                  </div>
                ))}
              </div>
            </Card>
          </motion.div>
        </Col>
      </Row>

      {/* Quick Actions and Recent Activity */}
      <Row gutter={[24, 24]} className="bottom-row">
        <Col xs={24} lg={12}>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
          >
            <Card title="Quick Actions" className="actions-card">
              <Row gutter={[16, 16]}>
                {quickActions.map((action, index) => (
                  <Col xs={12} key={index}>
                    <Card
                      className="action-card"
                      hoverable
                      onClick={action.action}
                      bodyStyle={{ padding: '16px' }}
                    >
                      <div className="action-content">
                        <div
                          className="action-icon"
                          style={{ color: action.color }}
                        >
                          {action.icon}
                        </div>
                        <div className="action-text">
                          <Text strong className="action-title">
                            {action.title}
                          </Text>
                          <Text type="secondary" className="action-description">
                            {action.description}
                          </Text>
                        </div>
                      </div>
                    </Card>
                  </Col>
                ))}
              </Row>
            </Card>
          </motion.div>
        </Col>

        <Col xs={24} lg={12}>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.5 }}
          >
            <Card title="Recent Activity" className="activity-card">
              <List
                dataSource={recentActivity}
                renderItem={(item) => (
                  <List.Item className="activity-item">
                    <List.Item.Meta
                      avatar={
                        <Avatar
                          icon={getActivityIcon(item.type)}
                          className="activity-avatar"
                        />
                      }
                      title={
                        <div className="activity-header">
                          <Text strong>{item.title}</Text>
                          <Tag color={getStatusColor(item.status)} size="small">
                            {item.status}
                          </Tag>
                        </div>
                      }
                      description={
                        <div className="activity-details">
                          <Text type="secondary">{item.description}</Text>
                          <Text type="secondary" className="activity-time">
                            {item.time}
                          </Text>
                        </div>
                      }
                    />
                  </List.Item>
                )}
              />
            </Card>
          </motion.div>
        </Col>
      </Row>
    </div>
  );
};

export default Dashboard;
