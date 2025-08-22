import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { message } from 'antd';
import { useAuth } from './AuthContext';

export interface CodeFile {
  id: string;
  name: string;
  content: string;
  language: 'c' | 'cpp';
  size: number;
  lastModified: string;
  analysis?: {
    warnings: string[];
    suggestions: string[];
    metrics: any;
    isValid: boolean;
  };
}

export interface Project {
  id: string;
  name: string;
  description: string;
  type: 'automotive' | 'embedded' | 'iot' | 'general';
  platform: string;
  createdAt: string;
  updatedAt: string;
  owner: string;
  collaborators: string[];
  files: CodeFile[];
  settings: {
    autoSave: boolean;
    safetyLevel: 'ASIL-A' | 'ASIL-B' | 'ASIL-C' | 'ASIL-D' | 'QM';
    targetArchitecture: string;
    compilerFlags: string[];
  };
  stats: {
    totalFiles: number;
    totalLines: number;
    lastGeneration: string;
    lastAnalysis: string;
  };
  tags: string[];
  isStarred: boolean;
  isArchived: boolean;
}

interface ProjectContextType {
  projects: Project[];
  currentProject: Project | null;
  isLoading: boolean;
  createProject: (projectData: Omit<Project, 'id' | 'createdAt' | 'updatedAt' | 'owner' | 'stats'>) => Promise<Project>;
  updateProject: (projectId: string, updates: Partial<Project>) => Promise<boolean>;
  deleteProject: (projectId: string) => Promise<boolean>;
  setCurrentProject: (project: Project | null) => void;
  addFileToProject: (projectId: string, file: Omit<CodeFile, 'id' | 'lastModified'>) => Promise<CodeFile>;
  updateFile: (projectId: string, fileId: string, updates: Partial<CodeFile>) => Promise<boolean>;
  deleteFile: (projectId: string, fileId: string) => Promise<boolean>;
  exportProject: (projectId: string) => Promise<Blob>;
  importProject: (file: File) => Promise<Project>;
  searchProjects: (query: string) => Project[];
  getRecentProjects: (limit?: number) => Project[];
  starProject: (projectId: string) => Promise<boolean>;
  archiveProject: (projectId: string) => Promise<boolean>;
  duplicateProject: (projectId: string) => Promise<Project>;
}

const ProjectContext = createContext<ProjectContextType | undefined>(undefined);

interface ProjectProviderProps {
  children: ReactNode;
}

export const ProjectProvider: React.FC<ProjectProviderProps> = ({ children }) => {
  const [projects, setProjects] = useState<Project[]>([]);
  const [currentProject, setCurrentProject] = useState<Project | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const { user } = useAuth();

  // Load projects from localStorage on mount
  useEffect(() => {
    if (user) {
      loadProjects();
    }
  }, [user]);

  // Auto-save current project
  useEffect(() => {
    if (currentProject && currentProject.settings.autoSave) {
      const timeoutId = setTimeout(() => {
        saveProjectToStorage(currentProject);
      }, 2000);
      return () => clearTimeout(timeoutId);
    }
  }, [currentProject]);

  const loadProjects = () => {
    try {
      const savedProjects = localStorage.getItem(`tata-ai-projects-${user?.id}`);
      if (savedProjects) {
        const parsedProjects = JSON.parse(savedProjects);
        setProjects(parsedProjects);
        
        // Load current project if exists
        const currentProjectId = localStorage.getItem(`tata-ai-current-project-${user?.id}`);
        if (currentProjectId) {
          const current = parsedProjects.find((p: Project) => p.id === currentProjectId);
          if (current) {
            setCurrentProject(current);
          }
        }
      } else {
        // Create sample projects for demo
        createSampleProjects();
      }
    } catch (error) {
      console.error('Failed to load projects:', error);
      message.error('Failed to load projects');
    }
  };

  const createSampleProjects = () => {
    const sampleProjects: Project[] = [
      {
        id: 'sample-1',
        name: 'TATA Vehicle ECU',
        description: 'Engine control unit software for TATA commercial vehicles',
        type: 'automotive',
        platform: 'ARM Cortex-M',
        createdAt: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString(),
        updatedAt: new Date().toISOString(),
        owner: user?.id || 'demo',
        collaborators: [],
        files: [
          {
            id: 'file-1',
            name: 'engine_control.c',
            content: `#include <stdint.h>\n#include <stdbool.h>\n\n// TATA Engine Control Module\nvoid engine_init() {\n    // Initialize engine parameters\n}\n\nvoid engine_update() {\n    // Update engine state\n}`,
            language: 'c',
            size: 256,
            lastModified: new Date().toISOString()
          }
        ],
        settings: {
          autoSave: true,
          safetyLevel: 'ASIL-B',
          targetArchitecture: 'ARM Cortex-M4',
          compilerFlags: ['-O2', '-Wall', '-Wextra']
        },
        stats: {
          totalFiles: 1,
          totalLines: 12,
          lastGeneration: new Date().toISOString(),
          lastAnalysis: new Date().toISOString()
        },
        tags: ['automotive', 'engine', 'ecu'],
        isStarred: true,
        isArchived: false
      },
      {
        id: 'sample-2',
        name: 'Brake System Controller',
        description: 'Anti-lock braking system for TATA passenger cars',
        type: 'automotive',
        platform: 'ARM Cortex-M',
        createdAt: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString(),
        updatedAt: new Date().toISOString(),
        owner: user?.id || 'demo',
        collaborators: [],
        files: [],
        settings: {
          autoSave: true,
          safetyLevel: 'ASIL-D',
          targetArchitecture: 'ARM Cortex-M7',
          compilerFlags: ['-O3', '-Wall', '-Werror']
        },
        stats: {
          totalFiles: 0,
          totalLines: 0,
          lastGeneration: '',
          lastAnalysis: ''
        },
        tags: ['automotive', 'brake', 'safety'],
        isStarred: false,
        isArchived: false
      }
    ];

    setProjects(sampleProjects);
    saveProjectsToStorage(sampleProjects);
  };

  const saveProjectsToStorage = (projectsToSave: Project[]) => {
    try {
      localStorage.setItem(`tata-ai-projects-${user?.id}`, JSON.stringify(projectsToSave));
    } catch (error) {
      console.error('Failed to save projects:', error);
      message.error('Failed to save projects');
    }
  };

  const saveProjectToStorage = (project: Project) => {
    const updatedProjects = projects.map(p => p.id === project.id ? project : p);
    setProjects(updatedProjects);
    saveProjectsToStorage(updatedProjects);
  };

  const createProject = async (projectData: Omit<Project, 'id' | 'createdAt' | 'updatedAt' | 'owner' | 'stats'>): Promise<Project> => {
    setIsLoading(true);
    try {
      const newProject: Project = {
        ...projectData,
        id: `project-${Date.now()}`,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
        owner: user?.id || 'anonymous',
        stats: {
          totalFiles: 0,
          totalLines: 0,
          lastGeneration: '',
          lastAnalysis: ''
        }
      };

      const updatedProjects = [...projects, newProject];
      setProjects(updatedProjects);
      saveProjectsToStorage(updatedProjects);
      
      message.success(`Project "${newProject.name}" created successfully`);
      return newProject;
    } catch (error) {
      console.error('Failed to create project:', error);
      message.error('Failed to create project');
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const updateProject = async (projectId: string, updates: Partial<Project>): Promise<boolean> => {
    try {
      const updatedProjects = projects.map(project => 
        project.id === projectId 
          ? { ...project, ...updates, updatedAt: new Date().toISOString() }
          : project
      );
      
      setProjects(updatedProjects);
      saveProjectsToStorage(updatedProjects);
      
      // Update current project if it's the one being updated
      if (currentProject?.id === projectId) {
        setCurrentProject({ ...currentProject, ...updates, updatedAt: new Date().toISOString() });
      }
      
      return true;
    } catch (error) {
      console.error('Failed to update project:', error);
      message.error('Failed to update project');
      return false;
    }
  };

  const deleteProject = async (projectId: string): Promise<boolean> => {
    try {
      const updatedProjects = projects.filter(project => project.id !== projectId);
      setProjects(updatedProjects);
      saveProjectsToStorage(updatedProjects);
      
      if (currentProject?.id === projectId) {
        setCurrentProject(null);
        localStorage.removeItem(`tata-ai-current-project-${user?.id}`);
      }
      
      message.success('Project deleted successfully');
      return true;
    } catch (error) {
      console.error('Failed to delete project:', error);
      message.error('Failed to delete project');
      return false;
    }
  };

  const handleSetCurrentProject = (project: Project | null) => {
    setCurrentProject(project);
    if (project) {
      localStorage.setItem(`tata-ai-current-project-${user?.id}`, project.id);
    } else {
      localStorage.removeItem(`tata-ai-current-project-${user?.id}`);
    }
  };

  const addFileToProject = async (projectId: string, file: Omit<CodeFile, 'id' | 'lastModified'>): Promise<CodeFile> => {
    try {
      const newFile: CodeFile = {
        ...file,
        id: `file-${Date.now()}`,
        lastModified: new Date().toISOString()
      };

      const updatedProjects = projects.map(project => {
        if (project.id === projectId) {
          const updatedFiles = [...project.files, newFile];
          return {
            ...project,
            files: updatedFiles,
            stats: {
              ...project.stats,
              totalFiles: updatedFiles.length,
              totalLines: updatedFiles.reduce((total, f) => total + f.content.split('\n').length, 0)
            },
            updatedAt: new Date().toISOString()
          };
        }
        return project;
      });

      setProjects(updatedProjects);
      saveProjectsToStorage(updatedProjects);
      
      message.success(`File "${newFile.name}" added successfully`);
      return newFile;
    } catch (error) {
      console.error('Failed to add file:', error);
      message.error('Failed to add file');
      throw error;
    }
  };

  const updateFile = async (projectId: string, fileId: string, updates: Partial<CodeFile>): Promise<boolean> => {
    try {
      const updatedProjects = projects.map(project => {
        if (project.id === projectId) {
          const updatedFiles = project.files.map(file =>
            file.id === fileId
              ? { ...file, ...updates, lastModified: new Date().toISOString() }
              : file
          );
          return {
            ...project,
            files: updatedFiles,
            stats: {
              ...project.stats,
              totalLines: updatedFiles.reduce((total, f) => total + f.content.split('\n').length, 0)
            },
            updatedAt: new Date().toISOString()
          };
        }
        return project;
      });

      setProjects(updatedProjects);
      saveProjectsToStorage(updatedProjects);
      return true;
    } catch (error) {
      console.error('Failed to update file:', error);
      message.error('Failed to update file');
      return false;
    }
  };

  const deleteFile = async (projectId: string, fileId: string): Promise<boolean> => {
    try {
      const updatedProjects = projects.map(project => {
        if (project.id === projectId) {
          const updatedFiles = project.files.filter(file => file.id !== fileId);
          return {
            ...project,
            files: updatedFiles,
            stats: {
              ...project.stats,
              totalFiles: updatedFiles.length,
              totalLines: updatedFiles.reduce((total, f) => total + f.content.split('\n').length, 0)
            },
            updatedAt: new Date().toISOString()
          };
        }
        return project;
      });

      setProjects(updatedProjects);
      saveProjectsToStorage(updatedProjects);
      
      message.success('File deleted successfully');
      return true;
    } catch (error) {
      console.error('Failed to delete file:', error);
      message.error('Failed to delete file');
      return false;
    }
  };

  const exportProject = async (projectId: string): Promise<Blob> => {
    const project = projects.find(p => p.id === projectId);
    if (!project) {
      throw new Error('Project not found');
    }

    const exportData = {
      project,
      exportedAt: new Date().toISOString(),
      version: '1.0'
    };

    return new Blob([JSON.stringify(exportData, null, 2)], {
      type: 'application/json'
    });
  };

  const importProject = async (file: File): Promise<Project> => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = async (e) => {
        try {
          const importData = JSON.parse(e.target?.result as string);
          const importedProject = importData.project;
          
          // Generate new ID to avoid conflicts
          const newProject: Project = {
            ...importedProject,
            id: `imported-${Date.now()}`,
            owner: user?.id || 'anonymous',
            createdAt: new Date().toISOString(),
            updatedAt: new Date().toISOString()
          };

          const updatedProjects = [...projects, newProject];
          setProjects(updatedProjects);
          saveProjectsToStorage(updatedProjects);
          
          message.success(`Project "${newProject.name}" imported successfully`);
          resolve(newProject);
        } catch (error) {
          console.error('Failed to import project:', error);
          message.error('Failed to import project');
          reject(error);
        }
      };
      reader.readAsText(file);
    });
  };

  const searchProjects = (query: string): Project[] => {
    if (!query.trim()) return projects;
    
    const lowercaseQuery = query.toLowerCase();
    return projects.filter(project =>
      project.name.toLowerCase().includes(lowercaseQuery) ||
      project.description.toLowerCase().includes(lowercaseQuery) ||
      project.tags.some(tag => tag.toLowerCase().includes(lowercaseQuery))
    );
  };

  const getRecentProjects = (limit: number = 5): Project[] => {
    return [...projects]
      .sort((a, b) => new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime())
      .slice(0, limit);
  };

  const starProject = async (projectId: string): Promise<boolean> => {
    return updateProject(projectId, { isStarred: !projects.find(p => p.id === projectId)?.isStarred });
  };

  const archiveProject = async (projectId: string): Promise<boolean> => {
    return updateProject(projectId, { isArchived: !projects.find(p => p.id === projectId)?.isArchived });
  };

  const duplicateProject = async (projectId: string): Promise<Project> => {
    const originalProject = projects.find(p => p.id === projectId);
    if (!originalProject) {
      throw new Error('Project not found');
    }

    const duplicatedProject: Project = {
      ...originalProject,
      id: `duplicate-${Date.now()}`,
      name: `${originalProject.name} (Copy)`,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      files: originalProject.files.map(file => ({
        ...file,
        id: `file-${Date.now()}-${Math.random()}`
      }))
    };

    const updatedProjects = [...projects, duplicatedProject];
    setProjects(updatedProjects);
    saveProjectsToStorage(updatedProjects);
    
    message.success(`Project duplicated as "${duplicatedProject.name}"`);
    return duplicatedProject;
  };

  const value: ProjectContextType = {
    projects,
    currentProject,
    isLoading,
    createProject,
    updateProject,
    deleteProject,
    setCurrentProject: handleSetCurrentProject,
    addFileToProject,
    updateFile,
    deleteFile,
    exportProject,
    importProject,
    searchProjects,
    getRecentProjects,
    starProject,
    archiveProject,
    duplicateProject
  };

  return (
    <ProjectContext.Provider value={value}>
      {children}
    </ProjectContext.Provider>
  );
};

export const useProjects = (): ProjectContextType => {
  const context = useContext(ProjectContext);
  if (!context) {
    throw new Error('useProjects must be used within a ProjectProvider');
  }
  return context;
};
