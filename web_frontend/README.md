# AI Co-pilot Frontend

A modern, responsive React application for the AI Co-pilot for Embedded Software Design.

## 🎨 Features

### 🏠 **Dashboard**
- **Real-time Statistics**: Code generation and analysis metrics
- **Performance Charts**: Weekly activity visualization with beautiful charts
- **Platform Distribution**: Pie chart showing target platform usage
- **Quick Actions**: One-click access to common tasks
- **Recent Activity**: Timeline of recent generations and analyses

### 🔧 **Code Generation**
- **Smart Input Interface**: Natural language code description with auto-suggestions
- **Quick Start Templates**: Pre-built prompts for common automotive patterns
- **Advanced Monaco Editor**: Professional code editor with syntax highlighting
- **Real-time Analysis**: Instant feedback on generated code
- **History Management**: Track and restore previous generations
- **Export Options**: Copy, download, or save generated code

### 🔍 **Code Analysis**
- **Interactive Code Editor**: Upload files or paste code for analysis
- **Sample Code Library**: Pre-loaded examples with known issues
- **Comprehensive Results**: Warnings, suggestions, and metrics visualization
- **Visual Analytics**: Charts showing code metrics and compliance status
- **Detailed Reports**: In-depth analysis with actionable recommendations

### 🎯 **Advanced UI Components**
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Dark/Light Theme**: Automatic theme switching support
- **Smooth Animations**: Framer Motion powered transitions
- **Professional Layout**: Modern sidebar navigation with collapsible menu
- **Real-time Status**: Live API connection status indicator

## 🛠 Technology Stack

- **React 18** - Modern React with hooks and concurrent features
- **TypeScript** - Type-safe development
- **Ant Design 5** - Professional UI component library
- **Monaco Editor** - VS Code editor experience in the browser
- **Framer Motion** - Smooth animations and transitions
- **Recharts** - Beautiful and responsive charts
- **Axios** - HTTP client for API communication

## 🚀 Getting Started

### Prerequisites

- Node.js 16+ and npm
- Python backend server running on port 8000

### Installation

1. **Install Dependencies**
   ```bash
   cd web_frontend
   npm install
   ```

2. **Development Mode**
   ```bash
   npm start
   ```
   Opens http://localhost:3000 with hot reload

3. **Production Build**
   ```bash
   npm run build
   ```
   Creates optimized build in `build/` folder

### Quick Setup Script

Use the automated build script from the project root:

```bash
python build_frontend.py
```

This will:
- Check Node.js/npm installation
- Install dependencies
- Build the production version
- Prepare files for deployment

## 📁 Project Structure

```
web_frontend/
├── public/
│   ├── index.html          # Main HTML template
│   └── manifest.json       # PWA manifest
├── src/
│   ├── components/
│   │   ├── Layout/
│   │   │   ├── AppLayout.tsx    # Main application layout
│   │   │   └── AppLayout.css    # Layout styles
│   │   ├── Dashboard/
│   │   │   ├── Dashboard.tsx    # Dashboard component
│   │   │   └── Dashboard.css    # Dashboard styles
│   │   ├── CodeGeneration/
│   │   │   ├── CodeGeneration.tsx  # Code generation interface
│   │   │   └── CodeGeneration.css  # Generation styles
│   │   └── CodeAnalysis/
│   │       ├── CodeAnalysis.tsx    # Code analysis interface
│   │       └── CodeAnalysis.css    # Analysis styles
│   ├── App.tsx             # Main application component
│   ├── App.css             # Global application styles
│   ├── index.tsx           # Application entry point
│   └── index.css           # Global CSS styles
├── package.json            # Dependencies and scripts
├── tsconfig.json          # TypeScript configuration
└── README.md              # This file
```

## 🎨 Design System

### Color Palette
- **Primary**: #1890ff (Blue)
- **Secondary**: #722ed1 (Purple)
- **Success**: #52c41a (Green)
- **Warning**: #faad14 (Orange)
- **Error**: #ff4d4f (Red)

### Typography
- **Headings**: System fonts with 600 weight
- **Body**: -apple-system, BlinkMacSystemFont, 'Segoe UI'
- **Code**: Monaco, 'Courier New', monospace

### Layout
- **Sidebar**: 280px width, collapsible to 80px
- **Content**: Responsive grid with 24px gutters
- **Cards**: 12px border radius, subtle shadows
- **Buttons**: 8px border radius, gradient backgrounds

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the web_frontend directory:

```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_VERSION=0.1.0
REACT_APP_TITLE=AI Co-pilot for Embedded Software Design
```

### API Integration

The frontend communicates with the FastAPI backend through these endpoints:

- `GET /api/status` - Check API status
- `POST /api/generate` - Generate code
- `POST /api/analyze` - Analyze code
- `GET /api/platforms` - Get available platforms
- `GET /api/templates` - Get code templates

## 📱 Responsive Design

The application is fully responsive with breakpoints:

- **Desktop**: 1200px+ (Full layout with sidebar)
- **Tablet**: 768px-1199px (Collapsible sidebar)
- **Mobile**: <768px (Mobile-optimized layout)

## 🎭 Animations

Powered by Framer Motion for smooth, professional animations:

- **Page Transitions**: Fade and slide effects
- **Component Mounting**: Staggered animations
- **Hover Effects**: Subtle scale and shadow changes
- **Loading States**: Smooth progress indicators

## 🧪 Testing

```bash
# Run tests
npm test

# Run tests with coverage
npm test -- --coverage

# Run tests in watch mode
npm test -- --watch
```

## 🚀 Deployment

### Development
```bash
npm start
```

### Production Build
```bash
npm run build
```

### Serve with Backend
The built files are automatically served by the FastAPI backend when you visit http://localhost:8000

## 🔧 Customization

### Adding New Components

1. Create component directory in `src/components/`
2. Add TypeScript component file
3. Add corresponding CSS file
4. Export from main App component

### Modifying Themes

Edit the ConfigProvider theme in `App.tsx`:

```typescript
theme={{
  algorithm: darkMode ? theme.darkAlgorithm : theme.defaultAlgorithm,
  token: {
    colorPrimary: '#1890ff',
    borderRadius: 8,
    // Add more customizations
  },
}}
```

### Adding New Pages

1. Create component in appropriate directory
2. Add route to `renderContent()` function in App.tsx
3. Add menu item to AppLayout component

## 🐛 Troubleshooting

### Common Issues

1. **Build Fails**
   - Check Node.js version (16+ required)
   - Clear node_modules and reinstall: `rm -rf node_modules && npm install`

2. **API Connection Issues**
   - Ensure backend is running on port 8000
   - Check CORS configuration in backend

3. **Monaco Editor Issues**
   - Ensure proper webpack configuration
   - Check browser console for loading errors

### Performance Optimization

- Use React.memo for expensive components
- Implement code splitting with React.lazy
- Optimize bundle size with webpack-bundle-analyzer

## 📄 License

This project is part of the AI Co-pilot for Embedded Software Design system.

## 🤝 Contributing

1. Follow TypeScript best practices
2. Use Ant Design components when possible
3. Maintain responsive design principles
4. Add proper error handling
5. Include loading states for async operations

---

**Built with ❤️ for embedded software engineers**
