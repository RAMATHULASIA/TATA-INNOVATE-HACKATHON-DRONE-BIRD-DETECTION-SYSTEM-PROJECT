#!/usr/bin/env python3
"""
Direct launcher for TATA AI Co-pilot Demo
"""

import uvicorn
import sys
import os
from pathlib import Path

def main():
    print("🏆 TATA AI Co-pilot - Demo Launcher")
    print("🚗 TATA Innovate Hackathon 2024 Edition")
    print("=" * 60)
    
    # Add current directory to Python path
    current_dir = os.getcwd()
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    print(f"✅ Working directory: {current_dir}")
    print(f"✅ Python path updated")
    
    # Check required files
    required_files = [
        "web_api/main.py",
        "ai_copilot/core.py",
        "web_frontend/src/App.tsx"
    ]
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ Found: {file_path}")
        else:
            print(f"❌ Missing: {file_path}")
            return 1
    
    print("\n🚀 Starting TATA AI Co-pilot Web Server...")
    print("🌐 Server will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/api/docs")
    print("\n🔐 Demo Login Credentials:")
    print("   • engineer@tata.com / tata123 (Full Access)")
    print("   • admin@tata.com / tata123 (Admin Access)")
    print("   • viewer@tata.com / tata123 (Read-Only)")
    print("\n🎯 Press Ctrl+C to stop the server")
    print("-" * 60)
    
    try:
        # Import and run the FastAPI app
        from web_api.main import app
        
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            log_level="info",
            access_log=True
        )
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        return 0
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Trying alternative startup method...")
        
        # Alternative method
        try:
            uvicorn.run(
                "web_api.main:app",
                host="0.0.0.0", 
                port=8000,
                log_level="info"
            )
        except Exception as e2:
            print(f"❌ Alternative startup failed: {e2}")
            return 1
            
    except Exception as e:
        print(f"❌ Server error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
