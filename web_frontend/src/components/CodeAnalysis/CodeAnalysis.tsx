import React, { useState, useRef } from 'react';
import {
  Row, Col, Card, Button, Select, Upload, Space, Typography, Tag, Divider,
  Tabs, Alert, Spin, Tooltip, Progress, List, Avatar, Badge, Statistic
} from 'antd';
import {
  BugOutlined, UploadOutlined, PlayCircleOutlined, SafetyOutlined,
  WarningOutlined, CheckCircleOutlined, InfoCircleOutlined, FileTextOutlined,
  MemoryOutlined, ClockCircleOutlined, ShieldOutlined, CodeOutlined
} from '@ant-design/icons';
import Editor from '@monaco-editor/react';
import { motion, AnimatePresence } from 'framer-motion';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer } from 'recharts';
import axios from 'axios';
import './CodeAnalysis.css';

const { Option } = Select;
const { TabPane } = Tabs;
const { Title, Text, Paragraph } = Typography;
const { Dragger } = Upload;

interface CodeAnalysisProps {}

interface AnalysisRequest {
  code: string;
  language: string;
}

interface AnalysisResponse {
  warnings: string[];
  suggestions: string[];
  metrics: any;
  is_valid: boolean;
}

const CodeAnalysis: React.FC<CodeAnalysisProps> = () => {
  const [loading, setLoading] = useState(false);
  const [codeToAnalyze, setCodeToAnalyze] = useState('');
  const [language, setLanguage] = useState('c');
  const [results, setResults] = useState<AnalysisResponse | null>(null);
  const [activeTab, setActiveTab] = useState('warnings');
  
  const editorRef = useRef<any>(null);

  const sampleCodes = [
    {
      title: 'Problematic Brake Control',
      description: 'Code with embedded system issues',
      code: `#include <stdio.h>
#include <stdlib.h>

void brake_control_function() {
    char large_buffer[2000];  // Large stack allocation
    int* sensor_data = malloc(500);  // Dynamic allocation without check
    
    printf("Brake system active\\n");  // Not suitable for embedded
    
    while(1) {  // Infinite loop without yield
        if (sensor_data[100] > 50) {  // Potential buffer overflow
            goto emergency_stop;  // MISRA C violation
        }
    }
    
    emergency_stop:
    // Missing free(sensor_data) - memory leak
    return;
}`,
      issues: ['Memory', 'Safety', 'Real-time']
    },
    {
      title: 'CAN Message Handler',
      description: 'Automotive communication code',
      code: `#include <stdint.h>
#include <stdbool.h>

typedef struct {
    uint32_t id;
    uint8_t dlc;
    uint8_t data[8];
} can_message_t;

bool send_can_message(uint32_t msg_id, uint8_t* data, uint8_t length) {
    can_message_t msg;
    
    if (data == NULL || length > 8) {
        return false;
    }
    
    msg.id = msg_id;
    msg.dlc = length;
    
    for (uint8_t i = 0; i < length; i++) {
        msg.data[i] = data[i];
    }
    
    return can_transmit(&msg);
}`,
      issues: ['Protocol', 'Validation']
    }
  ];

  const handleAnalyze = async () => {
    if (!codeToAnalyze.trim()) {
      return;
    }

    setLoading(true);
    try {
      const request: AnalysisRequest = {
        code: codeToAnalyze,
        language,
      };

      const response = await axios.post('/api/analyze', request);
      const result: AnalysisResponse = response.data;
      
      setResults(result);
      setActiveTab('warnings');
      
    } catch (error: any) {
      console.error('Analysis failed:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSampleLoad = (sample: any) => {
    setCodeToAnalyze(sample.code);
  };

  const handleFileUpload = (file: any) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      const content = e.target?.result as string;
      setCodeToAnalyze(content);
    };
    reader.readAsText(file);
    return false; // Prevent upload
  };

  const getMetricsData = () => {
    if (!results?.metrics) return [];
    
    return [
      { name: 'Stack Usage', value: results.metrics.estimated_stack_usage || 0, color: '#1890ff' },
      { name: 'Dynamic Allocs', value: results.metrics.dynamic_allocations || 0, color: '#ff4d4f' },
      { name: 'Large Arrays', value: results.metrics.large_arrays?.length || 0, color: '#faad14' }
    ];
  };

  const getComplianceData = () => {
    const warnings = results?.warnings.length || 0;
    const total = 10; // Assume 10 total checks
    const passed = total - warnings;
    
    return [
      { name: 'Passed', value: passed, color: '#52c41a' },
      { name: 'Failed', value: warnings, color: '#ff4d4f' }
    ];
  };

  const getSeverityIcon = (type: string) => {
    switch (type) {
      case 'error': return <WarningOutlined style={{ color: '#ff4d4f' }} />;
      case 'warning': return <InfoCircleOutlined style={{ color: '#faad14' }} />;
      case 'info': return <CheckCircleOutlined style={{ color: '#52c41a' }} />;
      default: return <InfoCircleOutlined />;
    }
  };

  return (
    <div className="code-analysis">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="analysis-header"
      >
        <Card className="header-card">
          <Row align="middle" justify="space-between">
            <Col>
              <Title level={3} className="header-title">
                <BugOutlined /> Code Analysis
              </Title>
              <Text type="secondary">
                Analyze embedded software for safety, memory, and real-time constraints
              </Text>
            </Col>
            <Col>
              <Space>
                <Tooltip title="Upload File">
                  <Dragger
                    accept=".c,.cpp,.h,.hpp"
                    beforeUpload={handleFileUpload}
                    showUploadList={false}
                    className="upload-dragger"
                  >
                    <Button icon={<UploadOutlined />}>
                      Upload Code
                    </Button>
                  </Dragger>
                </Tooltip>
              </Space>
            </Col>
          </Row>
        </Card>
      </motion.div>

      {/* Sample Codes */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="sample-codes"
      >
        <Card title="Sample Code for Analysis" className="samples-card">
          <Row gutter={[16, 16]}>
            {sampleCodes.map((sample, index) => (
              <Col xs={24} md={12} key={index}>
                <Card
                  className="sample-card"
                  hoverable
                  onClick={() => handleSampleLoad(sample)}
                  bodyStyle={{ padding: '16px' }}
                >
                  <div className="sample-content">
                    <div className="sample-header">
                      <Text strong className="sample-title">
                        {sample.title}
                      </Text>
                      <div className="sample-issues">
                        {sample.issues.map((issue, idx) => (
                          <Tag key={idx} size="small" color="orange">
                            {issue}
                          </Tag>
                        ))}
                      </div>
                    </div>
                    <Text type="secondary" className="sample-description">
                      {sample.description}
                    </Text>
                  </div>
                </Card>
              </Col>
            ))}
          </Row>
        </Card>
      </motion.div>

      {/* Main Content */}
      <Row gutter={[24, 24]} className="main-content">
        {/* Code Input */}
        <Col xs={24} lg={14}>
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
          >
            <Card title="Code to Analyze" className="input-card">
              <div className="analysis-controls">
                <Space>
                  <Select
                    value={language}
                    onChange={setLanguage}
                    style={{ width: 120 }}
                  >
                    <Option value="c">C</Option>
                    <Option value="cpp">C++</Option>
                  </Select>
                  <Button
                    type="primary"
                    icon={<PlayCircleOutlined />}
                    onClick={handleAnalyze}
                    loading={loading}
                    size="large"
                    className="analyze-btn"
                  >
                    {loading ? 'Analyzing...' : 'Analyze Code'}
                  </Button>
                </Space>
              </div>
              
              <div className="code-editor-container">
                <Editor
                  height="500px"
                  language={language}
                  value={codeToAnalyze}
                  onChange={(value) => setCodeToAnalyze(value || '')}
                  theme="vs-dark"
                  options={{
                    minimap: { enabled: true },
                    fontSize: 14,
                    lineNumbers: 'on',
                    wordWrap: 'on',
                    automaticLayout: true
                  }}
                />
              </div>

              {loading && (
                <div className="loading-indicator">
                  <Spin size="large" />
                  <div className="loading-text">
                    <Text>Analyzing code for embedded constraints...</Text>
                    <Progress percent={Math.random() * 100} showInfo={false} />
                  </div>
                </div>
              )}
            </Card>
          </motion.div>
        </Col>

        {/* Analysis Results */}
        <Col xs={24} lg={10}>
          <AnimatePresence>
            {results && (
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                transition={{ delay: 0.3 }}
              >
                <Card title="Analysis Summary" className="summary-card">
                  <Row gutter={[16, 16]}>
                    <Col span={12}>
                      <Statistic
                        title="Warnings"
                        value={results.warnings.length}
                        prefix={<WarningOutlined />}
                        valueStyle={{ color: results.warnings.length > 0 ? '#faad14' : '#52c41a' }}
                      />
                    </Col>
                    <Col span={12}>
                      <Statistic
                        title="Suggestions"
                        value={results.suggestions.length}
                        prefix={<BugOutlined />}
                        valueStyle={{ color: '#1890ff' }}
                      />
                    </Col>
                    <Col span={24}>
                      <div className="compliance-status">
                        <Text strong>Overall Status: </Text>
                        <Tag
                          color={results.is_valid ? 'success' : 'warning'}
                          icon={results.is_valid ? <CheckCircleOutlined /> : <WarningOutlined />}
                        >
                          {results.is_valid ? 'Compliant' : 'Issues Found'}
                        </Tag>
                      </div>
                    </Col>
                  </Row>

                  {/* Metrics Chart */}
                  {results.metrics && Object.keys(results.metrics).length > 0 && (
                    <div className="metrics-chart">
                      <Title level={5}>Code Metrics</Title>
                      <ResponsiveContainer width="100%" height={200}>
                        <BarChart data={getMetricsData()}>
                          <CartesianGrid strokeDasharray="3 3" />
                          <XAxis dataKey="name" />
                          <YAxis />
                          <RechartsTooltip />
                          <Bar dataKey="value" fill="#1890ff" />
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  )}

                  {/* Compliance Pie Chart */}
                  <div className="compliance-chart">
                    <Title level={5}>Compliance Overview</Title>
                    <ResponsiveContainer width="100%" height={150}>
                      <PieChart>
                        <Pie
                          data={getComplianceData()}
                          cx="50%"
                          cy="50%"
                          innerRadius={40}
                          outerRadius={60}
                          paddingAngle={5}
                          dataKey="value"
                        >
                          {getComplianceData().map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={entry.color} />
                          ))}
                        </Pie>
                        <RechartsTooltip />
                      </PieChart>
                    </ResponsiveContainer>
                  </div>
                </Card>
              </motion.div>
            )}
          </AnimatePresence>
        </Col>
      </Row>

      {/* Detailed Results */}
      <AnimatePresence>
        {results && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="detailed-results"
          >
            <Card title="Detailed Analysis Results" className="results-card">
              <Tabs activeKey={activeTab} onChange={setActiveTab}>
                <TabPane
                  tab={
                    <Badge count={results.warnings.length} size="small">
                      <span><WarningOutlined /> Warnings</span>
                    </Badge>
                  }
                  key="warnings"
                >
                  <div className="warnings-content">
                    {results.warnings.length > 0 ? (
                      <List
                        dataSource={results.warnings}
                        renderItem={(warning, index) => (
                          <List.Item className="warning-item">
                            <List.Item.Meta
                              avatar={
                                <Avatar
                                  icon={<WarningOutlined />}
                                  style={{ backgroundColor: '#faad14' }}
                                />
                              }
                              title={`Warning ${index + 1}`}
                              description={warning}
                            />
                          </List.Item>
                        )}
                      />
                    ) : (
                      <div className="no-issues">
                        <CheckCircleOutlined style={{ fontSize: 48, color: '#52c41a' }} />
                        <Title level={4} style={{ color: '#52c41a', marginTop: 16 }}>
                          No Warnings Found!
                        </Title>
                        <Text type="secondary">
                          Your code passes all embedded system constraint checks.
                        </Text>
                      </div>
                    )}
                  </div>
                </TabPane>

                <TabPane
                  tab={
                    <Badge count={results.suggestions.length} size="small">
                      <span><BugOutlined /> Suggestions</span>
                    </Badge>
                  }
                  key="suggestions"
                >
                  <div className="suggestions-content">
                    {results.suggestions.length > 0 ? (
                      <List
                        dataSource={results.suggestions}
                        renderItem={(suggestion, index) => (
                          <List.Item className="suggestion-item">
                            <List.Item.Meta
                              avatar={
                                <Avatar
                                  icon={<BugOutlined />}
                                  style={{ backgroundColor: '#1890ff' }}
                                />
                              }
                              title={`Suggestion ${index + 1}`}
                              description={suggestion}
                            />
                          </List.Item>
                        )}
                      />
                    ) : (
                      <div className="no-issues">
                        <Text>No additional suggestions available.</Text>
                      </div>
                    )}
                  </div>
                </TabPane>

                <TabPane
                  tab={<span><MemoryOutlined /> Metrics</span>}
                  key="metrics"
                >
                  <div className="metrics-content">
                    {results.metrics && Object.keys(results.metrics).length > 0 ? (
                      <div className="metrics-grid">
                        {Object.entries(results.metrics).map(([key, value]) => (
                          <div key={key} className="metric-card">
                            <div className="metric-header">
                              <Text strong>{key.replace(/_/g, ' ').toUpperCase()}</Text>
                            </div>
                            <div className="metric-value">
                              <Text className="metric-number">
                                {Array.isArray(value) ? value.length : String(value)}
                              </Text>
                              {Array.isArray(value) && value.length > 0 && (
                                <div className="metric-details">
                                  <Text type="secondary" style={{ fontSize: 12 }}>
                                    {value.slice(0, 3).join(', ')}
                                    {value.length > 3 && '...'}
                                  </Text>
                                </div>
                              )}
                            </div>
                          </div>
                        ))}
                      </div>
                    ) : (
                      <div className="no-metrics">
                        <Text>No metrics available for this analysis.</Text>
                      </div>
                    )}
                  </div>
                </TabPane>
              </Tabs>
            </Card>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default CodeAnalysis;
