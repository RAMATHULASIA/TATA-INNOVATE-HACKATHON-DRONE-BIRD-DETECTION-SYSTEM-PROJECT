import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { theme } from 'antd';

// TATA Brand Colors
export const TATA_THEMES = {
  tata_classic: {
    name: 'TATA Classic',
    colors: {
      primary: '#1B4F72',      // TATA Blue
      secondary: '#E74C3C',    // TATA Red
      accent: '#F39C12',       // TATA Orange
      success: '#27AE60',
      warning: '#F39C12',
      error: '#E74C3C',
      background: '#FFFFFF',
      surface: '#F8F9FA',
      text: '#2C3E50'
    },
    logo: '/assets/tata-logo-classic.png'
  },
  tata_modern: {
    name: 'TATA Modern',
    colors: {
      primary: '#0066CC',      // Modern TATA Blue
      secondary: '#FF6B35',    // Modern Orange
      accent: '#4ECDC4',       // Teal accent
      success: '#45B7D1',
      warning: '#FFA726',
      error: '#EF5350',
      background: '#FAFAFA',
      surface: '#FFFFFF',
      text: '#37474F'
    },
    logo: '/assets/tata-logo-modern.png'
  },
  tata_dark: {
    name: 'TATA Dark',
    colors: {
      primary: '#3498DB',      // Bright blue for dark theme
      secondary: '#E67E22',    // Orange
      accent: '#9B59B6',       // Purple accent
      success: '#2ECC71',
      warning: '#F1C40F',
      error: '#E74C3C',
      background: '#1A1A1A',
      surface: '#2D2D2D',
      text: '#ECEFF1'
    },
    logo: '/assets/tata-logo-dark.png'
  },
  automotive_pro: {
    name: 'Automotive Pro',
    colors: {
      primary: '#1890FF',      // Professional blue
      secondary: '#722ED1',    // Purple
      accent: '#52C41A',       // Green
      success: '#52C41A',
      warning: '#FAAD14',
      error: '#FF4D4F',
      background: '#F5F5F5',
      surface: '#FFFFFF',
      text: '#262626'
    },
    logo: '/assets/automotive-logo.png'
  }
};

export type ThemeType = keyof typeof TATA_THEMES;

interface ThemeContextType {
  currentTheme: ThemeType;
  themeConfig: typeof TATA_THEMES[ThemeType];
  setTheme: (theme: ThemeType) => void;
  isDarkMode: boolean;
  toggleDarkMode: () => void;
  customColors: any;
  updateCustomColors: (colors: any) => void;
  fontSize: 'small' | 'medium' | 'large';
  setFontSize: (size: 'small' | 'medium' | 'large') => void;
  compactMode: boolean;
  setCompactMode: (compact: boolean) => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

interface ThemeProviderProps {
  children: ReactNode;
}

export const ThemeProvider: React.FC<ThemeProviderProps> = ({ children }) => {
  const [currentTheme, setCurrentTheme] = useState<ThemeType>('tata_classic');
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [customColors, setCustomColors] = useState({});
  const [fontSize, setFontSize] = useState<'small' | 'medium' | 'large'>('medium');
  const [compactMode, setCompactMode] = useState(false);

  // Load theme from localStorage on mount
  useEffect(() => {
    const savedTheme = localStorage.getItem('tata-ai-theme') as ThemeType;
    const savedDarkMode = localStorage.getItem('tata-ai-dark-mode') === 'true';
    const savedFontSize = localStorage.getItem('tata-ai-font-size') as 'small' | 'medium' | 'large';
    const savedCompactMode = localStorage.getItem('tata-ai-compact-mode') === 'true';
    const savedCustomColors = localStorage.getItem('tata-ai-custom-colors');

    if (savedTheme && TATA_THEMES[savedTheme]) {
      setCurrentTheme(savedTheme);
    }
    if (savedDarkMode !== null) {
      setIsDarkMode(savedDarkMode);
    }
    if (savedFontSize) {
      setFontSize(savedFontSize);
    }
    if (savedCompactMode !== null) {
      setCompactMode(savedCompactMode);
    }
    if (savedCustomColors) {
      try {
        setCustomColors(JSON.parse(savedCustomColors));
      } catch (e) {
        console.warn('Failed to parse custom colors from localStorage');
      }
    }
  }, []);

  const setTheme = (newTheme: ThemeType) => {
    setCurrentTheme(newTheme);
    localStorage.setItem('tata-ai-theme', newTheme);
  };

  const toggleDarkMode = () => {
    const newDarkMode = !isDarkMode;
    setIsDarkMode(newDarkMode);
    localStorage.setItem('tata-ai-dark-mode', newDarkMode.toString());
  };

  const updateCustomColors = (colors: any) => {
    setCustomColors(colors);
    localStorage.setItem('tata-ai-custom-colors', JSON.stringify(colors));
  };

  const handleSetFontSize = (size: 'small' | 'medium' | 'large') => {
    setFontSize(size);
    localStorage.setItem('tata-ai-font-size', size);
  };

  const handleSetCompactMode = (compact: boolean) => {
    setCompactMode(compact);
    localStorage.setItem('tata-ai-compact-mode', compact.toString());
  };

  const themeConfig = TATA_THEMES[currentTheme];

  // Apply CSS custom properties for dynamic theming
  useEffect(() => {
    const root = document.documentElement;
    const colors = { ...themeConfig.colors, ...customColors };
    
    Object.entries(colors).forEach(([key, value]) => {
      root.style.setProperty(`--color-${key}`, value as string);
    });

    // Font size variables
    const fontSizes = {
      small: { base: '12px', heading: '16px' },
      medium: { base: '14px', heading: '18px' },
      large: { base: '16px', heading: '20px' }
    };
    
    root.style.setProperty('--font-size-base', fontSizes[fontSize].base);
    root.style.setProperty('--font-size-heading', fontSizes[fontSize].heading);
    
    // Compact mode spacing
    root.style.setProperty('--spacing-base', compactMode ? '12px' : '24px');
    root.style.setProperty('--spacing-small', compactMode ? '6px' : '12px');
  }, [themeConfig, customColors, fontSize, compactMode]);

  const value: ThemeContextType = {
    currentTheme,
    themeConfig,
    setTheme,
    isDarkMode,
    toggleDarkMode,
    customColors,
    updateCustomColors,
    fontSize,
    setFontSize: handleSetFontSize,
    compactMode,
    setCompactMode: handleSetCompactMode
  };

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useTheme = (): ThemeContextType => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
};

// Ant Design theme configuration generator
export const getAntdThemeConfig = (themeConfig: typeof TATA_THEMES[ThemeType], isDarkMode: boolean, customColors: any, fontSize: string, compactMode: boolean) => {
  const colors = { ...themeConfig.colors, ...customColors };
  
  const fontSizeMap = {
    small: 12,
    medium: 14,
    large: 16
  };

  return {
    algorithm: isDarkMode ? theme.darkAlgorithm : theme.defaultAlgorithm,
    token: {
      colorPrimary: colors.primary,
      colorSuccess: colors.success,
      colorWarning: colors.warning,
      colorError: colors.error,
      colorInfo: colors.primary,
      colorBgContainer: isDarkMode ? colors.surface : colors.background,
      colorBgElevated: colors.surface,
      fontSize: fontSizeMap[fontSize as keyof typeof fontSizeMap],
      borderRadius: compactMode ? 4 : 8,
      wireframe: false,
      // TATA specific customizations
      fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
      lineHeight: 1.5,
      controlHeight: compactMode ? 28 : 32,
      padding: compactMode ? 12 : 16,
      margin: compactMode ? 8 : 16,
    },
    components: {
      Layout: {
        headerBg: colors.primary,
        siderBg: isDarkMode ? colors.surface : colors.primary,
        bodyBg: colors.background,
      },
      Menu: {
        darkItemBg: 'transparent',
        darkItemSelectedBg: colors.accent,
        darkItemHoverBg: `${colors.primary}20`,
      },
      Button: {
        primaryShadow: `0 2px 8px ${colors.primary}30`,
        dangerShadow: `0 2px 8px ${colors.error}30`,
      },
      Card: {
        headerBg: colors.surface,
        actionsBg: colors.background,
      }
    }
  };
};
