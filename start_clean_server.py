#!/usr/bin/env python3
"""
Clean server startup for TATA AI Co-pilot
This will start the application properly without any import conflicts
"""

import uvicorn
import sys
import os
import time
import webbrowser
import threading
from pathlib import Path

def open_browser_delayed():
    """Open browser after server starts"""
    time.sleep(3)
    try:
        webbrowser.open('http://localhost:8000')
        print("🌐 Browser opened automatically")
    except Exception as e:
        print(f"⚠️  Could not open browser automatically: {e}")
        print("   Please manually open: http://localhost:8000")

def main():
    print("🏆 TATA AI Co-pilot - Clean Server Startup")
    print("🚗 TATA Innovate Hackathon 2024 Edition")
    print("=" * 70)
    
    # Set working directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    # Add to Python path
    if str(project_dir) not in sys.path:
        sys.path.insert(0, str(project_dir))
    
    print(f"✅ Working directory: {project_dir}")
    
    # Check key files
    key_files = [
        "web_api/main.py",
        "ai_copilot/core.py", 
        "web_frontend/src/App.tsx",
        "web_frontend/public/manifest.json"
    ]
    
    missing_files = []
    for file_path in key_files:
        if Path(file_path).exists():
            size = Path(file_path).stat().st_size
            print(f"✅ {file_path}: {size:,} bytes")
        else:
            missing_files.append(file_path)
            print(f"❌ {file_path}: NOT FOUND")
    
    if missing_files:
        print(f"\n❌ Missing files: {missing_files}")
        print("   Cannot start server without required files")
        return 1
    
    print("\n🚀 Starting TATA AI Co-pilot Web Server...")
    print("🌐 Server URL: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/api/docs")
    print("🔐 Demo Login Credentials:")
    print("   • engineer@tata.com / tata123 (Full Access)")
    print("   • admin@tata.com / tata123 (Admin Access)")
    print("   • viewer@tata.com / tata123 (Read-Only)")
    print("\n🎯 Features Available:")
    print("   • 4 TATA Brand Themes with real-time switching")
    print("   • PWA installation and offline support")
    print("   • AI-powered code generation for automotive systems")
    print("   • Project management with ASIL compliance")
    print("   • Mobile-responsive design")
    print("\n" + "=" * 70)
    print("🎯 Browser will open automatically in 3 seconds...")
    print("🛑 Press Ctrl+C to stop the server")
    print("-" * 70)
    
    # Start browser in background
    browser_thread = threading.Thread(target=open_browser_delayed, daemon=True)
    browser_thread.start()
    
    try:
        # Start the FastAPI server
        uvicorn.run(
            "web_api.main:app",
            host="0.0.0.0",
            port=8000,
            reload=False,  # Disable reload to avoid import issues
            log_level="info",
            access_log=True
        )
        
    except KeyboardInterrupt:
        print("\n🛑 TATA AI Co-pilot server stopped by user")
        print("🎉 Thank you for using TATA AI Co-pilot!")
        return 0
        
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        print("🔧 Troubleshooting tips:")
        print("   1. Check if port 8000 is already in use")
        print("   2. Ensure all dependencies are installed")
        print("   3. Verify Python path and working directory")
        return 1

if __name__ == "__main__":
    sys.exit(main())
