#!/usr/bin/env python3
"""
Run TATA AI Co-pilot Application
Direct execution without import conflicts
"""

import uvicorn
import sys
import os
from pathlib import Path

def main():
    print("🏆 TATA AI Co-pilot - Starting Application")
    print("🚗 TATA Innovate Hackathon 2024 Edition")
    print("=" * 60)
    
    # Set working directory
    os.chdir(Path(__file__).parent)
    current_dir = os.getcwd()
    
    print(f"✅ Working directory: {current_dir}")
    
    # Check key files
    key_files = [
        "web_api/main.py",
        "web_frontend/src/App.tsx",
        "web_frontend/public/manifest.json"
    ]
    
    for file_path in key_files:
        if Path(file_path).exists():
            size = Path(file_path).stat().st_size
            print(f"✅ {file_path}: {size:,} bytes")
        else:
            print(f"❌ {file_path}: NOT FOUND")
    
    print("\n🚀 Starting TATA AI Co-pilot Web Server...")
    print("🌐 Application URL: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/api/docs")
    print("\n🔐 Demo Login Credentials:")
    print("   • engineer@tata.com / tata123 (Full Access)")
    print("   • admin@tata.com / tata123 (Admin Access)")
    print("   • viewer@tata.com / tata123 (Read-Only)")
    print("\n🎯 Features Available:")
    print("   • 4 TATA Brand Themes")
    print("   • PWA Installation")
    print("   • AI Code Generation")
    print("   • Project Management")
    print("   • Mobile Responsive Design")
    print("\n" + "=" * 60)
    
    try:
        # Start the FastAPI server directly
        uvicorn.run(
            "web_api.main:app",
            host="0.0.0.0",
            port=8000,
            reload=False,
            log_level="info",
            access_log=True
        )
        
    except KeyboardInterrupt:
        print("\n🛑 TATA AI Co-pilot stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        print("\nTrying alternative method...")
        
        # Alternative: Simple HTTP server for static files
        import http.server
        import socketserver
        
        class TATAHandler(http.server.SimpleHTTPRequestHandler):
            def end_headers(self):
                self.send_header('Access-Control-Allow-Origin', '*')
                super().end_headers()
        
        print("🔄 Starting static file server...")
        with socketserver.TCPServer(("", 8000), TATAHandler) as httpd:
            print("🌐 Static server running at http://localhost:8000")
            print("📁 Serving TATA AI Co-pilot files")
            httpd.serve_forever()

if __name__ == "__main__":
    main()
