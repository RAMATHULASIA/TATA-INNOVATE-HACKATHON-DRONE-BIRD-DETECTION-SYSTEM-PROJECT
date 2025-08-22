import React, { useState } from 'react';
import { Form, Input, Button, Card, Typography, Divider, Space, Checkbox, Alert } from 'antd';
import { UserOutlined, LockOutlined, MailOutlined, CarOutlined } from '@ant-design/icons';
import { motion } from 'framer-motion';
import { useAuth } from '../../contexts/AuthContext';
import './LoginForm.css';

const { Title, Text, Link } = Typography;

interface LoginFormProps {
  onSwitchToRegister: () => void;
}

const LoginForm: React.FC<LoginFormProps> = ({ onSwitchToRegister }) => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [rememberMe, setRememberMe] = useState(false);
  const { login } = useAuth();

  const handleSubmit = async (values: { email: string; password: string }) => {
    setLoading(true);
    try {
      const success = await login(values.email, values.password);
      if (success && rememberMe) {
        localStorage.setItem('tata-ai-remember', 'true');
      }
    } catch (error) {
      console.error('Login failed:', error);
    } finally {
      setLoading(false);
    }
  };

  const demoCredentials = [
    { email: 'engineer@tata.com', role: 'Engineer', description: 'Full access to generation and analysis' },
    { email: 'admin@tata.com', role: 'Admin', description: 'Administrative access with all features' },
    { email: 'viewer@tata.com', role: 'Viewer', description: 'Read-only access for code analysis' }
  ];

  const fillDemoCredentials = (email: string) => {
    form.setFieldsValue({ email, password: 'tata123' });
  };

  return (
    <div className="login-container">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="login-card-wrapper"
      >
        <Card className="login-card">
          <div className="login-header">
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
              className="login-logo"
            >
              <CarOutlined />
            </motion.div>
            <Title level={2} className="login-title">
              Welcome to TATA AI Co-pilot
            </Title>
            <Text type="secondary" className="login-subtitle">
              Sign in to access your embedded software development workspace
            </Text>
          </div>

          <Form
            form={form}
            name="login"
            onFinish={handleSubmit}
            layout="vertical"
            size="large"
            className="login-form"
          >
            <Form.Item
              name="email"
              label="Email Address"
              rules={[
                { required: true, message: 'Please enter your email' },
                { type: 'email', message: 'Please enter a valid email' }
              ]}
            >
              <Input
                prefix={<MailOutlined />}
                placeholder="your.email@tata.com"
                className="login-input"
              />
            </Form.Item>

            <Form.Item
              name="password"
              label="Password"
              rules={[{ required: true, message: 'Please enter your password' }]}
            >
              <Input.Password
                prefix={<LockOutlined />}
                placeholder="Enter your password"
                className="login-input"
              />
            </Form.Item>

            <Form.Item>
              <div className="login-options">
                <Checkbox
                  checked={rememberMe}
                  onChange={(e) => setRememberMe(e.target.checked)}
                >
                  Remember me
                </Checkbox>
                <Link className="forgot-password">
                  Forgot password?
                </Link>
              </div>
            </Form.Item>

            <Form.Item>
              <Button
                type="primary"
                htmlType="submit"
                loading={loading}
                className="login-button"
                block
              >
                {loading ? 'Signing In...' : 'Sign In'}
              </Button>
            </Form.Item>
          </Form>

          <Divider>
            <Text type="secondary">Demo Accounts</Text>
          </Divider>

          <div className="demo-accounts">
            <Alert
              message="For TATA Innovate Hackathon Demo"
              description="Use any of the demo accounts below with password: tata123"
              type="info"
              showIcon
              className="demo-alert"
            />
            
            <Space direction="vertical" style={{ width: '100%' }}>
              {demoCredentials.map((cred, index) => (
                <motion.div
                  key={cred.email}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.3 + index * 0.1 }}
                >
                  <Card
                    size="small"
                    className="demo-account-card"
                    hoverable
                    onClick={() => fillDemoCredentials(cred.email)}
                  >
                    <div className="demo-account-content">
                      <div className="demo-account-info">
                        <Text strong>{cred.email}</Text>
                        <Text type="secondary" className="demo-role">
                          {cred.role} - {cred.description}
                        </Text>
                      </div>
                      <Button size="small" type="link">
                        Use Account
                      </Button>
                    </div>
                  </Card>
                </motion.div>
              ))}
            </Space>
          </div>

          <Divider />

          <div className="login-footer">
            <Text type="secondary">
              Don't have an account?{' '}
              <Link onClick={onSwitchToRegister} className="register-link">
                Sign up for TATA AI Co-pilot
              </Link>
            </Text>
          </div>

          <div className="hackathon-badge">
            <motion.div
              animate={{ 
                boxShadow: [
                  '0 0 0 0 rgba(27, 79, 114, 0.4)',
                  '0 0 0 10px rgba(27, 79, 114, 0)',
                  '0 0 0 0 rgba(27, 79, 114, 0)'
                ]
              }}
              transition={{ duration: 2, repeat: Infinity }}
              className="hackathon-pulse"
            >
              <Text strong className="hackathon-text">
                🏆 TATA Innovate Hackathon 2024
              </Text>
            </motion.div>
          </div>
        </Card>
      </motion.div>
    </div>
  );
};

export default LoginForm;
