#!/usr/bin/env python3
"""
Simple server to demonstrate the TATA AI Co-pilot web interface
"""

import uvicorn
import sys
import os
from pathlib import Path

def main():
    print("🏆 TATA AI Co-pilot - Starting Web Server")
    print("🚗 TATA Innovate Hackathon 2024 Edition")
    print("=" * 60)
    
    # Check if we have the web API
    if not Path("web_api/main.py").exists():
        print("❌ Web API not found")
        return 1
    
    print("✅ Web API found")
    print("✅ Starting server on http://localhost:8000")
    print("✅ API docs available at http://localhost:8000/api/docs")
    print("\n🔐 Demo Login Credentials:")
    print("   • engineer@tata.com / tata123 (Full Access)")
    print("   • admin@tata.com / tata123 (Admin Access)")
    print("   • viewer@tata.com / tata123 (Read-Only)")
    print("\n🎯 Press Ctrl+C to stop the server")
    print("-" * 60)
    
    try:
        # Add current directory to Python path
        sys.path.insert(0, os.getcwd())
        
        # Start the server
        uvicorn.run(
            "web_api.main:app",
            host="0.0.0.0",
            port=8000,
            log_level="info",
            access_log=True
        )
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        return 0
    except Exception as e:
        print(f"❌ Server error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
