import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { message } from 'antd';
import axios from 'axios';

export interface User {
  id: string;
  email: string;
  name: string;
  role: 'admin' | 'engineer' | 'viewer';
  department: string;
  avatar?: string;
  preferences: {
    theme: string;
    notifications: boolean;
    autoSave: boolean;
  };
  stats: {
    codeGenerated: number;
    codeAnalyzed: number;
    projectsCreated: number;
    lastLogin: string;
  };
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<boolean>;
  logout: () => void;
  register: (userData: RegisterData) => Promise<boolean>;
  updateProfile: (updates: Partial<User>) => Promise<boolean>;
  resetPassword: (email: string) => Promise<boolean>;
  changePassword: (oldPassword: string, newPassword: string) => Promise<boolean>;
}

interface RegisterData {
  email: string;
  password: string;
  name: string;
  department: string;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Check for existing session on mount
  useEffect(() => {
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    try {
      const token = localStorage.getItem('tata-ai-token');
      if (!token) {
        setIsLoading(false);
        return;
      }

      // Set axios default header
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;

      // Verify token with backend
      const response = await axios.get('/api/auth/me');
      if (response.data.user) {
        setUser(response.data.user);
      } else {
        // Token invalid, clear it
        localStorage.removeItem('tata-ai-token');
        delete axios.defaults.headers.common['Authorization'];
      }
    } catch (error) {
      console.error('Auth check failed:', error);
      localStorage.removeItem('tata-ai-token');
      delete axios.defaults.headers.common['Authorization'];
    } finally {
      setIsLoading(false);
    }
  };

  const login = async (email: string, password: string): Promise<boolean> => {
    try {
      setIsLoading(true);
      
      // For demo purposes, simulate login with predefined users
      const demoUsers: Record<string, User> = {
        'engineer@tata.com': {
          id: '1',
          email: 'engineer@tata.com',
          name: 'TATA Engineer',
          role: 'engineer',
          department: 'Embedded Systems',
          avatar: '/assets/avatars/engineer.png',
          preferences: {
            theme: 'tata_classic',
            notifications: true,
            autoSave: true
          },
          stats: {
            codeGenerated: 156,
            codeAnalyzed: 89,
            projectsCreated: 12,
            lastLogin: new Date().toISOString()
          }
        },
        'admin@tata.com': {
          id: '2',
          email: 'admin@tata.com',
          name: 'TATA Admin',
          role: 'admin',
          department: 'IT Administration',
          avatar: '/assets/avatars/admin.png',
          preferences: {
            theme: 'tata_modern',
            notifications: true,
            autoSave: true
          },
          stats: {
            codeGenerated: 45,
            codeAnalyzed: 234,
            projectsCreated: 8,
            lastLogin: new Date().toISOString()
          }
        },
        'viewer@tata.com': {
          id: '3',
          email: 'viewer@tata.com',
          name: 'TATA Viewer',
          role: 'viewer',
          department: 'Quality Assurance',
          avatar: '/assets/avatars/viewer.png',
          preferences: {
            theme: 'automotive_pro',
            notifications: false,
            autoSave: false
          },
          stats: {
            codeGenerated: 0,
            codeAnalyzed: 67,
            projectsCreated: 0,
            lastLogin: new Date().toISOString()
          }
        }
      };

      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 1000));

      if (demoUsers[email] && password === 'tata123') {
        const userData = demoUsers[email];
        const token = `demo-token-${userData.id}-${Date.now()}`;
        
        // Store token
        localStorage.setItem('tata-ai-token', token);
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        
        // Store user data
        setUser(userData);
        localStorage.setItem('tata-ai-user', JSON.stringify(userData));
        
        message.success(`Welcome back, ${userData.name}!`);
        return true;
      } else {
        message.error('Invalid credentials. Try: engineer@tata.com / tata123');
        return false;
      }
    } catch (error) {
      console.error('Login failed:', error);
      message.error('Login failed. Please try again.');
      return false;
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('tata-ai-token');
    localStorage.removeItem('tata-ai-user');
    delete axios.defaults.headers.common['Authorization'];
    message.success('Logged out successfully');
  };

  const register = async (userData: RegisterData): Promise<boolean> => {
    try {
      setIsLoading(true);
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      // For demo, create a new user
      const newUser: User = {
        id: Date.now().toString(),
        email: userData.email,
        name: userData.name,
        role: 'engineer',
        department: userData.department,
        preferences: {
          theme: 'tata_classic',
          notifications: true,
          autoSave: true
        },
        stats: {
          codeGenerated: 0,
          codeAnalyzed: 0,
          projectsCreated: 0,
          lastLogin: new Date().toISOString()
        }
      };

      const token = `demo-token-${newUser.id}-${Date.now()}`;
      
      localStorage.setItem('tata-ai-token', token);
      localStorage.setItem('tata-ai-user', JSON.stringify(newUser));
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      
      setUser(newUser);
      message.success('Registration successful! Welcome to TATA AI Co-pilot!');
      return true;
    } catch (error) {
      console.error('Registration failed:', error);
      message.error('Registration failed. Please try again.');
      return false;
    } finally {
      setIsLoading(false);
    }
  };

  const updateProfile = async (updates: Partial<User>): Promise<boolean> => {
    try {
      if (!user) return false;
      
      const updatedUser = { ...user, ...updates };
      setUser(updatedUser);
      localStorage.setItem('tata-ai-user', JSON.stringify(updatedUser));
      
      message.success('Profile updated successfully');
      return true;
    } catch (error) {
      console.error('Profile update failed:', error);
      message.error('Failed to update profile');
      return false;
    }
  };

  const resetPassword = async (email: string): Promise<boolean> => {
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      message.success('Password reset link sent to your email');
      return true;
    } catch (error) {
      console.error('Password reset failed:', error);
      message.error('Failed to send reset link');
      return false;
    }
  };

  const changePassword = async (oldPassword: string, newPassword: string): Promise<boolean> => {
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      message.success('Password changed successfully');
      return true;
    } catch (error) {
      console.error('Password change failed:', error);
      message.error('Failed to change password');
      return false;
    }
  };

  const value: AuthContextType = {
    user,
    isAuthenticated: !!user,
    isLoading,
    login,
    logout,
    register,
    updateProfile,
    resetPassword,
    changePassword
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

// Role-based access control hook
export const usePermissions = () => {
  const { user } = useAuth();
  
  const canGenerate = user?.role === 'admin' || user?.role === 'engineer';
  const canAnalyze = user?.role === 'admin' || user?.role === 'engineer' || user?.role === 'viewer';
  const canManageProjects = user?.role === 'admin' || user?.role === 'engineer';
  const canAccessSettings = user?.role === 'admin';
  const canViewAnalytics = user?.role === 'admin' || user?.role === 'engineer';
  
  return {
    canGenerate,
    canAnalyze,
    canManageProjects,
    canAccessSettings,
    canViewAnalytics
  };
};
