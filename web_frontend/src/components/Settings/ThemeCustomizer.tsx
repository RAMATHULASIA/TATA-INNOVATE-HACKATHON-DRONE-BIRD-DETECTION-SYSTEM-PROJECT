import React, { useState } from 'react';
import {
  Card, Row, Col, Select, Switch, Slider, ColorPicker, Button, Space, Typography,
  Divider, Radio, Tooltip, Badge, Alert, Tabs
} from 'antd';
import {
  BgColorsOutlined, FontSizeOutlined, LayoutOutlined, PaletteOutlined,
  MoonOutlined, SunOutlined, CompressOutlined, ExpandOutlined,
  ReloadOutlined, SaveOutlined, EyeOutlined
} from '@ant-design/icons';
import { motion } from 'framer-motion';
import { useTheme, TATA_THEMES, ThemeType } from '../../contexts/ThemeContext';
import './ThemeCustomizer.css';

const { Title, Text } = Typography;
const { TabPane } = Tabs;

const ThemeCustomizer: React.FC = () => {
  const {
    currentTheme,
    themeConfig,
    setTheme,
    isDarkMode,
    toggleDarkMode,
    customColors,
    updateCustomColors,
    fontSize,
    setFontSize,
    compactMode,
    setCompactMode
  } = useTheme();

  const [previewMode, setPreviewMode] = useState(false);
  const [tempColors, setTempColors] = useState(customColors);

  const handleThemeChange = (newTheme: ThemeType) => {
    setTheme(newTheme);
  };

  const handleColorChange = (colorKey: string, color: any) => {
    const newColors = {
      ...tempColors,
      [colorKey]: typeof color === 'string' ? color : color.toHexString()
    };
    setTempColors(newColors);
    
    if (previewMode) {
      updateCustomColors(newColors);
    }
  };

  const applyColors = () => {
    updateCustomColors(tempColors);
  };

  const resetColors = () => {
    setTempColors({});
    updateCustomColors({});
  };

  const exportTheme = () => {
    const themeData = {
      theme: currentTheme,
      isDarkMode,
      customColors,
      fontSize,
      compactMode,
      exportedAt: new Date().toISOString()
    };
    
    const blob = new Blob([JSON.stringify(themeData, null, 2)], {
      type: 'application/json'
    });
    
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `tata-theme-${currentTheme}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const themePreviewCards = Object.entries(TATA_THEMES).map(([key, theme]) => (
    <motion.div
      key={key}
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
    >
      <Card
        className={`theme-preview-card ${currentTheme === key ? 'active' : ''}`}
        hoverable
        onClick={() => handleThemeChange(key as ThemeType)}
        bodyStyle={{ padding: '16px' }}
      >
        <div className="theme-preview-header">
          <div className="theme-preview-colors">
            <div
              className="color-dot"
              style={{ backgroundColor: theme.colors.primary }}
            />
            <div
              className="color-dot"
              style={{ backgroundColor: theme.colors.secondary }}
            />
            <div
              className="color-dot"
              style={{ backgroundColor: theme.colors.accent }}
            />
          </div>
          {currentTheme === key && (
            <Badge status="processing" text="Active" />
          )}
        </div>
        <Title level={5} className="theme-name">
          {theme.name}
        </Title>
        <Text type="secondary" className="theme-description">
          {key === 'tata_classic' && 'Traditional TATA brand colors'}
          {key === 'tata_modern' && 'Contemporary design approach'}
          {key === 'tata_dark' && 'Dark mode optimized'}
          {key === 'automotive_pro' && 'Professional automotive theme'}
        </Text>
      </Card>
    </motion.div>
  ));

  return (
    <div className="theme-customizer">
      <div className="customizer-header">
        <Title level={3}>
          <PaletteOutlined /> Theme Customization
        </Title>
        <Text type="secondary">
          Personalize your TATA AI Co-pilot experience with custom themes and layouts
        </Text>
      </div>

      <Tabs defaultActiveKey="themes" className="customizer-tabs">
        <TabPane
          tab={
            <span>
              <BgColorsOutlined />
              Themes
            </span>
          }
          key="themes"
        >
          <div className="theme-section">
            <div className="section-header">
              <Title level={4}>TATA Brand Themes</Title>
              <Text type="secondary">
                Choose from our curated collection of TATA-branded themes
              </Text>
            </div>

            <Row gutter={[16, 16]} className="theme-grid">
              {themePreviewCards.map((card, index) => (
                <Col xs={24} sm={12} lg={6} key={index}>
                  {card}
                </Col>
              ))}
            </Row>

            <Alert
              message="TATA Innovate Hackathon Special"
              description="These themes are specially designed for the TATA Innovate Hackathon, incorporating official TATA brand colors and automotive industry standards."
              type="info"
              showIcon
              className="hackathon-alert"
            />
          </div>
        </TabPane>

        <TabPane
          tab={
            <span>
              <PaletteOutlined />
              Colors
            </span>
          }
          key="colors"
        >
          <div className="color-section">
            <div className="section-header">
              <Title level={4}>Custom Colors</Title>
              <Space>
                <Switch
                  checked={previewMode}
                  onChange={setPreviewMode}
                  checkedChildren={<EyeOutlined />}
                  unCheckedChildren={<EyeOutlined />}
                />
                <Text>Live Preview</Text>
              </Space>
            </div>

            <Row gutter={[24, 24]}>
              <Col xs={24} lg={12}>
                <Card title="Primary Colors" className="color-card">
                  <Space direction="vertical" style={{ width: '100%' }}>
                    <div className="color-item">
                      <Text strong>Primary Color</Text>
                      <ColorPicker
                        value={tempColors.primary || themeConfig.colors.primary}
                        onChange={(color) => handleColorChange('primary', color)}
                        showText
                        size="large"
                      />
                    </div>
                    <div className="color-item">
                      <Text strong>Secondary Color</Text>
                      <ColorPicker
                        value={tempColors.secondary || themeConfig.colors.secondary}
                        onChange={(color) => handleColorChange('secondary', color)}
                        showText
                        size="large"
                      />
                    </div>
                    <div className="color-item">
                      <Text strong>Accent Color</Text>
                      <ColorPicker
                        value={tempColors.accent || themeConfig.colors.accent}
                        onChange={(color) => handleColorChange('accent', color)}
                        showText
                        size="large"
                      />
                    </div>
                  </Space>
                </Card>
              </Col>

              <Col xs={24} lg={12}>
                <Card title="Status Colors" className="color-card">
                  <Space direction="vertical" style={{ width: '100%' }}>
                    <div className="color-item">
                      <Text strong>Success Color</Text>
                      <ColorPicker
                        value={tempColors.success || themeConfig.colors.success}
                        onChange={(color) => handleColorChange('success', color)}
                        showText
                        size="large"
                      />
                    </div>
                    <div className="color-item">
                      <Text strong>Warning Color</Text>
                      <ColorPicker
                        value={tempColors.warning || themeConfig.colors.warning}
                        onChange={(color) => handleColorChange('warning', color)}
                        showText
                        size="large"
                      />
                    </div>
                    <div className="color-item">
                      <Text strong>Error Color</Text>
                      <ColorPicker
                        value={tempColors.error || themeConfig.colors.error}
                        onChange={(color) => handleColorChange('error', color)}
                        showText
                        size="large"
                      />
                    </div>
                  </Space>
                </Card>
              </Col>
            </Row>

            <div className="color-actions">
              <Space>
                <Button
                  type="primary"
                  icon={<SaveOutlined />}
                  onClick={applyColors}
                  disabled={previewMode}
                >
                  Apply Colors
                </Button>
                <Button
                  icon={<ReloadOutlined />}
                  onClick={resetColors}
                >
                  Reset to Default
                </Button>
              </Space>
            </div>
          </div>
        </TabPane>

        <TabPane
          tab={
            <span>
              <LayoutOutlined />
              Layout
            </span>
          }
          key="layout"
        >
          <div className="layout-section">
            <Row gutter={[24, 24]}>
              <Col xs={24} lg={12}>
                <Card title="Display Settings" className="settings-card">
                  <Space direction="vertical" style={{ width: '100%' }}>
                    <div className="setting-item">
                      <div className="setting-header">
                        <Text strong>Dark Mode</Text>
                        <Switch
                          checked={isDarkMode}
                          onChange={toggleDarkMode}
                          checkedChildren={<MoonOutlined />}
                          unCheckedChildren={<SunOutlined />}
                        />
                      </div>
                      <Text type="secondary">
                        Toggle between light and dark themes
                      </Text>
                    </div>

                    <Divider />

                    <div className="setting-item">
                      <div className="setting-header">
                        <Text strong>Compact Mode</Text>
                        <Switch
                          checked={compactMode}
                          onChange={setCompactMode}
                          checkedChildren={<CompressOutlined />}
                          unCheckedChildren={<ExpandOutlined />}
                        />
                      </div>
                      <Text type="secondary">
                        Reduce spacing for more content density
                      </Text>
                    </div>
                  </Space>
                </Card>
              </Col>

              <Col xs={24} lg={12}>
                <Card title="Typography" className="settings-card">
                  <div className="setting-item">
                    <Text strong>Font Size</Text>
                    <Radio.Group
                      value={fontSize}
                      onChange={(e) => setFontSize(e.target.value)}
                      className="font-size-group"
                    >
                      <Radio.Button value="small">
                        <FontSizeOutlined style={{ fontSize: '12px' }} />
                        Small
                      </Radio.Button>
                      <Radio.Button value="medium">
                        <FontSizeOutlined style={{ fontSize: '14px' }} />
                        Medium
                      </Radio.Button>
                      <Radio.Button value="large">
                        <FontSizeOutlined style={{ fontSize: '16px' }} />
                        Large
                      </Radio.Button>
                    </Radio.Group>
                  </div>
                </Card>
              </Col>
            </Row>
          </div>
        </TabPane>
      </Tabs>

      <div className="customizer-footer">
        <Space>
          <Button
            type="primary"
            icon={<SaveOutlined />}
            onClick={exportTheme}
          >
            Export Theme
          </Button>
          <Text type="secondary">
            Save your customizations as a theme file
          </Text>
        </Space>
      </div>
    </div>
  );
};

export default ThemeCustomizer;
