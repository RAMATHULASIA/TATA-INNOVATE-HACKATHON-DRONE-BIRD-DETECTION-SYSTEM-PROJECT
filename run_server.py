#!/usr/bin/env python3
"""
Simple server runner for TATA AI Co-pilot
"""

import uvicorn
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("🏆 Starting TATA AI Co-pilot Server")
    print("🚗 TATA Innovate Hackathon 2024 Edition")
    print("=" * 50)
    print("🌐 Server will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/api/docs")
    print("🔐 Demo Login: engineer@tata.com / tata123")
    print("=" * 50)
    
    try:
        uvicorn.run(
            "web_api.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")

if __name__ == "__main__":
    main()
