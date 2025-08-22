import React, { useState, useEffect, useRef } from 'react';
import {
  Row, Col, Card, Button, Input, Select, Form, Space, Typography, Tag, Divider,
  Tabs, Alert, Spin, Tooltip, Progress, Drawer, List, Avatar, Badge, Switch
} from 'antd';
import {
  PlayCircleOutlined, SaveOutlined, CopyOutlined, DownloadOutlined,
  SettingOutlined, HistoryOutlined, BulbOutlined, CodeOutlined,
  CarOutlined, SafetyOutlined, ThunderboltOutlined, RocketOutlined
} from '@ant-design/icons';
import Editor from '@monaco-editor/react';
import { motion, AnimatePresence } from 'framer-motion';
import axios from 'axios';
import './CodeGeneration.css';

const { TextArea } = Input;
const { Option } = Select;
const { TabPane } = Tabs;
const { Title, Text, Paragraph } = Typography;

interface CodeGenerationProps {
  platforms: string[];
  templates: string[];
}

interface GenerationRequest {
  description: string;
  language: string;
  target_platform?: string;
  constraints?: any;
}

interface GenerationResponse {
  generated_code: string;
  explanation: string;
  warnings: string[];
  suggestions: string[];
  metadata: any;
}

const CodeGeneration: React.FC<CodeGenerationProps> = ({ platforms, templates }) => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [generatedCode, setGeneratedCode] = useState('');
  const [results, setResults] = useState<GenerationResponse | null>(null);
  const [settingsVisible, setSettingsVisible] = useState(false);
  const [historyVisible, setHistoryVisible] = useState(false);
  const [editorTheme, setEditorTheme] = useState('vs-dark');
  const [autoSave, setAutoSave] = useState(true);
  const [history, setHistory] = useState<any[]>([]);
  
  const editorRef = useRef<any>(null);

  const quickPrompts = [
    {
      title: 'CAN Message Handler',
      description: 'Create a CAN message transmission function for engine RPM data',
      icon: <CarOutlined />,
      color: '#1890ff',
      platform: 'ARM Cortex-M'
    },
    {
      title: 'AUTOSAR Component',
      description: 'Generate an AUTOSAR software component for brake control system',
      icon: <SafetyOutlined />,
      color: '#52c41a',
      platform: 'ARM Cortex-M'
    },
    {
      title: 'State Machine',
      description: 'Create a finite state machine for engine control with idle, running, and error states',
      icon: <ThunderboltOutlined />,
      color: '#faad14',
      platform: 'ARM Cortex-M'
    },
    {
      title: 'Interrupt Handler',
      description: 'Generate an interrupt service routine for timer-based sensor reading',
      icon: <RocketOutlined />,
      color: '#722ed1',
      platform: 'ARM Cortex-M'
    }
  ];

  const handleGenerate = async (values: any) => {
    setLoading(true);
    try {
      const request: GenerationRequest = {
        description: values.description,
        language: values.language || 'c',
        target_platform: values.target_platform,
        constraints: values.constraints ? JSON.parse(values.constraints) : undefined
      };

      const response = await axios.post('/api/generate', request);
      const result: GenerationResponse = response.data;
      
      setGeneratedCode(result.generated_code);
      setResults(result);
      
      // Add to history
      const historyItem = {
        id: Date.now(),
        timestamp: new Date().toISOString(),
        request,
        result,
        preview: result.generated_code.substring(0, 100) + '...'
      };
      setHistory(prev => [historyItem, ...prev.slice(0, 9)]); // Keep last 10
      
    } catch (error: any) {
      console.error('Generation failed:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleQuickPrompt = (prompt: any) => {
    form.setFieldsValue({
      description: prompt.description,
      target_platform: prompt.platform
    });
  };

  const handleCopyCode = () => {
    navigator.clipboard.writeText(generatedCode);
  };

  const handleDownloadCode = () => {
    const element = document.createElement('a');
    const file = new Blob([generatedCode], { type: 'text/plain' });
    element.href = URL.createObjectURL(file);
    element.download = 'generated_code.c';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  const handleEditorDidMount = (editor: any) => {
    editorRef.current = editor;
  };

  return (
    <div className="code-generation">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="generation-header"
      >
        <Card className="header-card">
          <Row align="middle" justify="space-between">
            <Col>
              <Title level={3} className="header-title">
                <CodeOutlined /> AI Code Generation
              </Title>
              <Text type="secondary">
                Generate automotive embedded software with AI assistance
              </Text>
            </Col>
            <Col>
              <Space>
                <Tooltip title="Generation History">
                  <Button
                    icon={<HistoryOutlined />}
                    onClick={() => setHistoryVisible(true)}
                  >
                    History
                  </Button>
                </Tooltip>
                <Tooltip title="Settings">
                  <Button
                    icon={<SettingOutlined />}
                    onClick={() => setSettingsVisible(true)}
                  />
                </Tooltip>
              </Space>
            </Col>
          </Row>
        </Card>
      </motion.div>

      {/* Quick Prompts */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="quick-prompts"
      >
        <Card title="Quick Start Templates" className="prompts-card">
          <Row gutter={[16, 16]}>
            {quickPrompts.map((prompt, index) => (
              <Col xs={24} sm={12} lg={6} key={index}>
                <motion.div
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                  <Card
                    className="prompt-card"
                    hoverable
                    onClick={() => handleQuickPrompt(prompt)}
                    bodyStyle={{ padding: '16px' }}
                  >
                    <div className="prompt-content">
                      <div
                        className="prompt-icon"
                        style={{ color: prompt.color }}
                      >
                        {prompt.icon}
                      </div>
                      <div className="prompt-text">
                        <Text strong className="prompt-title">
                          {prompt.title}
                        </Text>
                        <Text type="secondary" className="prompt-description">
                          {prompt.description}
                        </Text>
                      </div>
                    </div>
                  </Card>
                </motion.div>
              </Col>
            ))}
          </Row>
        </Card>
      </motion.div>

      {/* Main Content */}
      <Row gutter={[24, 24]} className="main-content">
        {/* Input Panel */}
        <Col xs={24} lg={10}>
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
          >
            <Card title="Generation Request" className="input-card">
              <Form
                form={form}
                layout="vertical"
                onFinish={handleGenerate}
                initialValues={{
                  language: 'c',
                  target_platform: 'ARM Cortex-M'
                }}
              >
                <Form.Item
                  name="description"
                  label="Code Description"
                  rules={[{ required: true, message: 'Please describe the code you want to generate' }]}
                >
                  <TextArea
                    rows={4}
                    placeholder="Describe the embedded software you want to generate (e.g., 'Create a CAN message handler for brake system data with error handling and MISRA C compliance')"
                    className="description-input"
                  />
                </Form.Item>

                <Row gutter={16}>
                  <Col span={12}>
                    <Form.Item name="language" label="Language">
                      <Select>
                        <Option value="c">C</Option>
                        <Option value="cpp">C++</Option>
                      </Select>
                    </Form.Item>
                  </Col>
                  <Col span={12}>
                    <Form.Item name="target_platform" label="Target Platform">
                      <Select placeholder="Select platform" allowClear>
                        {platforms.map(platform => (
                          <Option key={platform} value={platform}>
                            {platform}
                          </Option>
                        ))}
                      </Select>
                    </Form.Item>
                  </Col>
                </Row>

                <Form.Item name="constraints" label="Additional Constraints (JSON)">
                  <TextArea
                    rows={3}
                    placeholder='{"message_id": "0x123", "data_length": 8, "safety_level": "ASIL-B"}'
                    className="constraints-input"
                  />
                </Form.Item>

                <Form.Item>
                  <Button
                    type="primary"
                    htmlType="submit"
                    loading={loading}
                    icon={<PlayCircleOutlined />}
                    size="large"
                    className="generate-btn"
                    block
                  >
                    {loading ? 'Generating Code...' : 'Generate Code'}
                  </Button>
                </Form.Item>
              </Form>

              {loading && (
                <div className="loading-indicator">
                  <Spin size="large" />
                  <div className="loading-text">
                    <Text>AI is analyzing your requirements...</Text>
                    <Progress percent={Math.random() * 100} showInfo={false} />
                  </div>
                </div>
              )}
            </Card>
          </motion.div>
        </Col>

        {/* Output Panel */}
        <Col xs={24} lg={14}>
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3 }}
          >
            <Card
              title="Generated Code"
              className="output-card"
              extra={
                generatedCode && (
                  <Space>
                    <Tooltip title="Copy Code">
                      <Button
                        icon={<CopyOutlined />}
                        onClick={handleCopyCode}
                        size="small"
                      />
                    </Tooltip>
                    <Tooltip title="Download Code">
                      <Button
                        icon={<DownloadOutlined />}
                        onClick={handleDownloadCode}
                        size="small"
                      />
                    </Tooltip>
                    <Tooltip title="Save to Project">
                      <Button
                        icon={<SaveOutlined />}
                        size="small"
                        type="primary"
                      />
                    </Tooltip>
                  </Space>
                )
              }
            >
              <div className="code-editor-container">
                <Editor
                  height="500px"
                  language="c"
                  value={generatedCode}
                  onChange={(value) => setGeneratedCode(value || '')}
                  theme={editorTheme}
                  onMount={handleEditorDidMount}
                  options={{
                    readOnly: false,
                    minimap: { enabled: true },
                    fontSize: 14,
                    lineNumbers: 'on',
                    roundedSelection: false,
                    scrollBeyondLastLine: false,
                    automaticLayout: true,
                    wordWrap: 'on'
                  }}
                />
              </div>
            </Card>
          </motion.div>
        </Col>
      </Row>

      {/* Results Panel */}
      <AnimatePresence>
        {results && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="results-panel"
          >
            <Card title="Analysis Results" className="results-card">
              <Tabs defaultActiveKey="explanation">
                <TabPane tab="Explanation" key="explanation">
                  <div className="explanation-content">
                    <Paragraph>{results.explanation}</Paragraph>
                  </div>
                </TabPane>

                <TabPane
                  tab={
                    <Badge count={results.warnings.length} size="small">
                      <span>Warnings</span>
                    </Badge>
                  }
                  key="warnings"
                >
                  <div className="warnings-content">
                    {results.warnings.length > 0 ? (
                      results.warnings.map((warning, index) => (
                        <Alert
                          key={index}
                          message={warning}
                          type="warning"
                          showIcon
                          className="result-alert"
                        />
                      ))
                    ) : (
                      <div className="no-issues">
                        <Text type="success">✅ No warnings found!</Text>
                      </div>
                    )}
                  </div>
                </TabPane>

                <TabPane
                  tab={
                    <Badge count={results.suggestions.length} size="small">
                      <span>Suggestions</span>
                    </Badge>
                  }
                  key="suggestions"
                >
                  <div className="suggestions-content">
                    {results.suggestions.length > 0 ? (
                      results.suggestions.map((suggestion, index) => (
                        <Alert
                          key={index}
                          message={suggestion}
                          type="info"
                          showIcon
                          icon={<BulbOutlined />}
                          className="result-alert"
                        />
                      ))
                    ) : (
                      <div className="no-issues">
                        <Text>No additional suggestions.</Text>
                      </div>
                    )}
                  </div>
                </TabPane>

                <TabPane tab="Metadata" key="metadata">
                  <div className="metadata-content">
                    {results.metadata && (
                      <div className="metadata-grid">
                        <div className="metadata-item">
                          <Text strong>Language:</Text>
                          <Tag color="blue">{results.metadata.language}</Tag>
                        </div>
                        <div className="metadata-item">
                          <Text strong>Platform:</Text>
                          <Tag color="green">{results.metadata.platform}</Tag>
                        </div>
                        {results.metadata.context && (
                          <div className="metadata-item">
                            <Text strong>ECU Type:</Text>
                            <Tag color="orange">{results.metadata.context.ecu_type}</Tag>
                          </div>
                        )}
                        {results.metadata.context?.safety_level && (
                          <div className="metadata-item">
                            <Text strong>Safety Level:</Text>
                            <Tag color="red">{results.metadata.context.safety_level}</Tag>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                </TabPane>
              </Tabs>
            </Card>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Settings Drawer */}
      <Drawer
        title="Generation Settings"
        placement="right"
        onClose={() => setSettingsVisible(false)}
        open={settingsVisible}
        width={400}
      >
        <div className="settings-content">
          <div className="setting-item">
            <Text strong>Editor Theme</Text>
            <Select
              value={editorTheme}
              onChange={setEditorTheme}
              style={{ width: '100%', marginTop: 8 }}
            >
              <Option value="vs-dark">Dark</Option>
              <Option value="light">Light</Option>
              <Option value="hc-black">High Contrast</Option>
            </Select>
          </div>

          <Divider />

          <div className="setting-item">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <Text strong>Auto Save</Text>
              <Switch checked={autoSave} onChange={setAutoSave} />
            </div>
            <Text type="secondary" style={{ fontSize: 12, marginTop: 4, display: 'block' }}>
              Automatically save generated code to history
            </Text>
          </div>
        </div>
      </Drawer>

      {/* History Drawer */}
      <Drawer
        title="Generation History"
        placement="right"
        onClose={() => setHistoryVisible(false)}
        open={historyVisible}
        width={500}
      >
        <List
          dataSource={history}
          renderItem={(item) => (
            <List.Item
              className="history-item"
              actions={[
                <Button size="small" type="link">
                  Restore
                </Button>
              ]}
            >
              <List.Item.Meta
                avatar={<Avatar icon={<CodeOutlined />} />}
                title={
                  <div>
                    <Text strong>{item.request.description.substring(0, 50)}...</Text>
                    <Tag size="small" style={{ marginLeft: 8 }}>
                      {item.request.language}
                    </Tag>
                  </div>
                }
                description={
                  <div>
                    <Text type="secondary" style={{ fontSize: 12 }}>
                      {new Date(item.timestamp).toLocaleString()}
                    </Text>
                    <div style={{ marginTop: 4 }}>
                      <Text type="secondary" style={{ fontSize: 11 }}>
                        {item.preview}
                      </Text>
                    </div>
                  </div>
                }
              />
            </List.Item>
          )}
        />
      </Drawer>
    </div>
  );
};

export default CodeGeneration;
