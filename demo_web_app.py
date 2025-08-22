#!/usr/bin/env python3
"""
Demo script for the AI Co-pilot web application

This script demonstrates the web API functionality without requiring
the full React frontend setup.
"""

import asyncio
import uvicorn
from web_api.main import app
import webbrowser
import time
import threading


def open_browser_delayed():
    """Open browser after server starts"""
    time.sleep(2)
    print("🌐 Opening web browser...")
    webbrowser.open('http://localhost:8000/api/docs')


def main():
    """Run the demo"""
    print("🚗 AI Co-pilot Web Application Demo")
    print("=" * 50)
    print("🚀 Starting FastAPI backend...")
    print("📍 API Documentation: http://localhost:8000/api/docs")
    print("🔧 API Endpoints: http://localhost:8000/api/")
    print("\n💡 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    # Start browser in background
    browser_thread = threading.Thread(target=open_browser_delayed)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Start the server
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )


if __name__ == "__main__":
    main()
