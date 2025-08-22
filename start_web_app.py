#!/usr/bin/env python3
"""
Startup script for the AI Co-pilot web application

This script starts both the FastAPI backend and serves the React frontend.
"""

import subprocess
import sys
import os
import time
import webbrowser
from pathlib import Path
import threading


def check_node_installed():
    """Check if Node.js is installed"""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ Node.js found: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ Node.js not found. Please install Node.js from https://nodejs.org/")
    return False


def check_npm_installed():
    """Check if npm is installed"""
    try:
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ npm found: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ npm not found. Please install npm (usually comes with Node.js)")
    return False


def install_frontend_dependencies():
    """Install frontend dependencies"""
    frontend_dir = Path("web_frontend")
    
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return False
    
    print("📦 Installing frontend dependencies...")
    
    try:
        result = subprocess.run(
            ['npm', 'install'],
            cwd=frontend_dir,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✓ Frontend dependencies installed successfully")
            return True
        else:
            print(f"❌ Failed to install dependencies: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False


def build_frontend():
    """Build the React frontend"""
    frontend_dir = Path("web_frontend")
    
    print("🔨 Building React frontend...")
    
    try:
        result = subprocess.run(
            ['npm', 'run', 'build'],
            cwd=frontend_dir,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✓ Frontend built successfully")
            return True
        else:
            print(f"❌ Failed to build frontend: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error building frontend: {e}")
        return False


def start_backend():
    """Start the FastAPI backend"""
    print("🚀 Starting FastAPI backend...")
    
    try:
        # Start the backend server
        subprocess.run([
            sys.executable, '-m', 'uvicorn',
            'web_api.main:app',
            '--host', '0.0.0.0',
            '--port', '8000',
            '--reload'
        ])
        
    except KeyboardInterrupt:
        print("\n🛑 Backend server stopped")
    except Exception as e:
        print(f"❌ Error starting backend: {e}")


def open_browser():
    """Open the web browser after a delay"""
    time.sleep(3)  # Wait for server to start
    print("🌐 Opening web browser...")
    webbrowser.open('http://localhost:8000')


def main():
    """Main function"""
    print("🚗 AI Co-pilot Web Application Startup")
    print("=" * 50)
    
    # Check prerequisites
    if not check_node_installed():
        return 1
    
    if not check_npm_installed():
        return 1
    
    # Check if frontend dependencies are installed
    frontend_dir = Path("web_frontend")
    node_modules = frontend_dir / "node_modules"
    
    if not node_modules.exists():
        if not install_frontend_dependencies():
            return 1
    
    # Check if frontend is built
    build_dir = frontend_dir / "build"
    
    if not build_dir.exists():
        print("📝 Frontend not built yet. Building now...")
        if not build_frontend():
            print("⚠️  Frontend build failed, but continuing with backend only...")
    
    # Start browser in a separate thread
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    print("\n🎯 Starting the application...")
    print("📍 Backend API: http://localhost:8000/api/docs")
    print("🌐 Web Interface: http://localhost:8000")
    print("\n💡 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    # Start the backend (this will block)
    start_backend()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
