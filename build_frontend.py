#!/usr/bin/env python3
"""
Build script for the AI Co-pilot frontend

This script builds the React frontend and prepares it for deployment.
"""

import subprocess
import sys
import os
import shutil
from pathlib import Path


def check_node_npm():
    """Check if Node.js and npm are installed"""
    try:
        node_result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        npm_result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
        
        if node_result.returncode == 0 and npm_result.returncode == 0:
            print(f"✓ Node.js: {node_result.stdout.strip()}")
            print(f"✓ npm: {npm_result.stdout.strip()}")
            return True
        else:
            print("❌ Node.js or npm not found")
            return False
            
    except FileNotFoundError:
        print("❌ Node.js or npm not found. Please install Node.js from https://nodejs.org/")
        return False


def install_dependencies():
    """Install frontend dependencies"""
    frontend_dir = Path("web_frontend")
    
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return False
    
    print("📦 Installing dependencies...")
    
    try:
        result = subprocess.run(
            ['npm', 'install'],
            cwd=frontend_dir,
            check=True,
            capture_output=True,
            text=True
        )
        
        print("✓ Dependencies installed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e.stderr}")
        return False


def build_frontend():
    """Build the React frontend"""
    frontend_dir = Path("web_frontend")
    
    print("🔨 Building React frontend...")
    
    try:
        result = subprocess.run(
            ['npm', 'run', 'build'],
            cwd=frontend_dir,
            check=True,
            capture_output=True,
            text=True
        )
        
        print("✓ Frontend built successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to build frontend: {e.stderr}")
        return False


def copy_build_files():
    """Copy build files to the appropriate location"""
    build_dir = Path("web_frontend/build")
    
    if not build_dir.exists():
        print("❌ Build directory not found")
        return False
    
    print("📁 Build files are ready in web_frontend/build/")
    print("✓ Frontend is ready to serve!")
    return True


def main():
    """Main build process"""
    print("🏆 TATA AI Co-pilot Frontend Build Process")
    print("🚗 TATA Innovate Hackathon 2024 Edition")
    print("=" * 60)
    
    # Check prerequisites
    if not check_node_npm():
        return 1
    
    # Install dependencies
    if not install_dependencies():
        return 1
    
    # Build frontend
    if not build_frontend():
        return 1
    
    # Copy build files
    if not copy_build_files():
        return 1
    
    print("\n" + "=" * 60)
    print("🎉 TATA AI Co-pilot Frontend Build Completed Successfully!")
    print("\n🏆 TATA Innovate Hackathon 2024 Features:")
    print("   ✅ Advanced Theme Customization with TATA Branding")
    print("   ✅ PWA Support with Offline Functionality")
    print("   ✅ User Authentication & Role-Based Access")
    print("   ✅ Project Management & Data Persistence")
    print("   ✅ Responsive Design for All Devices")
    print("\n📋 Next steps:")
    print("1. Start the backend server:")
    print("   python -m uvicorn web_api.main:app --host 0.0.0.0 --port 8000")
    print("\n2. Open your browser and visit:")
    print("   http://localhost:8000")
    print("\n3. Demo Login Credentials:")
    print("   • engineer@tata.com / tata123 (Full Access)")
    print("   • admin@tata.com / tata123 (Admin Access)")
    print("   • viewer@tata.com / tata123 (Read-Only)")
    print("\n4. Install as PWA:")
    print("   • Click 'Install' button in browser address bar")
    print("   • Use offline features when disconnected")
    print("\n🚗 Ready for TATA Innovate Hackathon Demo!")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
