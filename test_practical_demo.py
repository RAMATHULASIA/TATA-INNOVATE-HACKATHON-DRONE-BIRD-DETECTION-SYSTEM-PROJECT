#!/usr/bin/env python3
"""
Practical Test of TATA AI Co-pilot Application

This script tests all the key features to ensure they work in practice.
"""

import asyncio
import json
import os
import sys
from pathlib import Path

def test_project_structure():
    """Test that all required files are in place"""
    print("🔍 Testing Project Structure")
    print("-" * 40)
    
    required_files = [
        "web_frontend/src/App.tsx",
        "web_frontend/src/contexts/ThemeContext.tsx",
        "web_frontend/src/contexts/AuthContext.tsx", 
        "web_frontend/src/contexts/ProjectContext.tsx",
        "web_frontend/src/components/Auth/LoginForm.tsx",
        "web_frontend/src/components/Settings/ThemeCustomizer.tsx",
        "web_frontend/public/manifest.json",
        "web_frontend/public/sw.js",
        "web_frontend/public/offline.html",
        "web_api/main.py",
        "ai_copilot/core.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
        else:
            print(f"✅ {file_path}")
    
    if missing_files:
        print(f"\n❌ Missing files: {missing_files}")
        return False
    else:
        print("\n✅ All required files are present!")
        return True

def test_pwa_manifest():
    """Test PWA manifest configuration"""
    print("\n📱 Testing PWA Manifest")
    print("-" * 40)
    
    manifest_path = Path("web_frontend/public/manifest.json")
    if not manifest_path.exists():
        print("❌ Manifest file not found")
        return False
    
    try:
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        
        required_fields = ['name', 'short_name', 'theme_color', 'display', 'start_url']
        for field in required_fields:
            if field in manifest:
                print(f"✅ {field}: {manifest[field]}")
            else:
                print(f"❌ Missing field: {field}")
                return False
        
        # Check TATA branding
        if "TATA" in manifest.get('name', ''):
            print("✅ TATA branding present in app name")
        
        if manifest.get('theme_color') == '#1B4F72':
            print("✅ TATA brand color configured")
        
        return True
        
    except Exception as e:
        print(f"❌ Error reading manifest: {e}")
        return False

def test_theme_system():
    """Test theme configuration"""
    print("\n🎨 Testing Theme System")
    print("-" * 40)
    
    theme_file = Path("web_frontend/src/contexts/ThemeContext.tsx")
    if not theme_file.exists():
        print("❌ Theme context file not found")
        return False
    
    try:
        with open(theme_file, 'r') as f:
            content = f.read()
        
        # Check for TATA themes
        tata_themes = ['tata_classic', 'tata_modern', 'tata_dark', 'automotive_pro']
        for theme in tata_themes:
            if theme in content:
                print(f"✅ {theme} theme configured")
            else:
                print(f"❌ Missing theme: {theme}")
                return False
        
        # Check for TATA brand colors
        tata_colors = ['#1B4F72', '#E74C3C', '#F39C12']
        for color in tata_colors:
            if color in content:
                print(f"✅ TATA brand color {color} configured")
        
        return True
        
    except Exception as e:
        print(f"❌ Error reading theme file: {e}")
        return False

def test_authentication_system():
    """Test authentication configuration"""
    print("\n🔐 Testing Authentication System")
    print("-" * 40)
    
    auth_file = Path("web_frontend/src/contexts/AuthContext.tsx")
    if not auth_file.exists():
        print("❌ Auth context file not found")
        return False
    
    try:
        with open(auth_file, 'r') as f:
            content = f.read()
        
        # Check for demo accounts
        demo_accounts = ['engineer@tata.com', 'admin@tata.com', 'viewer@tata.com']
        for account in demo_accounts:
            if account in content:
                print(f"✅ Demo account {account} configured")
            else:
                print(f"❌ Missing demo account: {account}")
                return False
        
        # Check for role-based access
        roles = ['engineer', 'admin', 'viewer']
        for role in roles:
            if role in content:
                print(f"✅ Role '{role}' configured")
        
        return True
        
    except Exception as e:
        print(f"❌ Error reading auth file: {e}")
        return False

def test_ai_core():
    """Test AI core functionality"""
    print("\n🤖 Testing AI Core Functionality")
    print("-" * 40)
    
    try:
        # Add current directory to Python path
        sys.path.insert(0, os.getcwd())
        
        from ai_copilot import AICopilot
        from ai_copilot.config import CopilotConfig
        
        print("✅ AI Co-pilot modules imported successfully")
        
        # Initialize the AI Co-pilot
        config = CopilotConfig()
        copilot = AICopilot(config)
        
        print("✅ AI Co-pilot initialized")
        
        # Test async functionality
        async def test_generation():
            try:
                await copilot.initialize()
                print("✅ AI Co-pilot async initialization successful")
                
                # Test code generation
                result = await copilot.generate_code(
                    "Create a TATA vehicle brake system monitor",
                    language="c",
                    target_platform="ARM Cortex-M"
                )
                
                print(f"✅ Code generation successful: {len(result.generated_code)} chars")
                print(f"✅ Explanation provided: {len(result.explanation)} chars")
                print(f"✅ Warnings: {len(result.warnings)}")
                print(f"✅ Suggestions: {len(result.suggestions)}")
                
                return True
                
            except Exception as e:
                print(f"❌ Async test failed: {e}")
                return False
        
        # Run the async test
        result = asyncio.run(test_generation())
        return result
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ AI core test failed: {e}")
        return False

def test_web_api():
    """Test web API configuration"""
    print("\n🌐 Testing Web API Configuration")
    print("-" * 40)
    
    api_file = Path("web_api/main.py")
    if not api_file.exists():
        print("❌ Web API file not found")
        return False
    
    try:
        with open(api_file, 'r') as f:
            content = f.read()
        
        # Check for required endpoints
        endpoints = ['/api/generate', '/api/analyze', '/api/status', '/api/platforms']
        for endpoint in endpoints:
            if endpoint in content:
                print(f"✅ Endpoint {endpoint} configured")
            else:
                print(f"❌ Missing endpoint: {endpoint}")
                return False
        
        # Check for CORS configuration
        if 'CORSMiddleware' in content:
            print("✅ CORS middleware configured")
        
        # Check for static file serving
        if 'StaticFiles' in content:
            print("✅ Static file serving configured")
        
        return True
        
    except Exception as e:
        print(f"❌ Error reading API file: {e}")
        return False

def test_frontend_components():
    """Test frontend component structure"""
    print("\n⚛️ Testing Frontend Components")
    print("-" * 40)
    
    components = [
        "web_frontend/src/components/Layout/AppLayout.tsx",
        "web_frontend/src/components/Dashboard/Dashboard.tsx", 
        "web_frontend/src/components/CodeGeneration/CodeGeneration.tsx",
        "web_frontend/src/components/CodeAnalysis/CodeAnalysis.tsx",
        "web_frontend/src/components/Auth/LoginForm.tsx",
        "web_frontend/src/components/Settings/ThemeCustomizer.tsx"
    ]
    
    missing_components = []
    for component in components:
        if Path(component).exists():
            print(f"✅ {Path(component).name}")
        else:
            missing_components.append(component)
            print(f"❌ Missing: {Path(component).name}")
    
    return len(missing_components) == 0

def run_practical_test():
    """Run all practical tests"""
    print("🏆 TATA AI Co-pilot - Practical Application Test")
    print("🚗 TATA Innovate Hackathon 2024 Edition")
    print("=" * 70)
    
    tests = [
        ("Project Structure", test_project_structure),
        ("PWA Manifest", test_pwa_manifest),
        ("Theme System", test_theme_system),
        ("Authentication", test_authentication_system),
        ("AI Core", test_ai_core),
        ("Web API", test_web_api),
        ("Frontend Components", test_frontend_components)
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed_tests += 1
                print(f"\n✅ {test_name} - PASSED")
            else:
                print(f"\n❌ {test_name} - FAILED")
        except Exception as e:
            print(f"\n❌ {test_name} - ERROR: {e}")
    
    print("\n" + "=" * 70)
    print(f"🎯 Test Results: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED! Application is ready for demo!")
        print("\n🚀 To start the application:")
        print("   python start_web_app.py")
        print("\n🌐 Then visit: http://localhost:8000")
        print("🔐 Login with: engineer@tata.com / tata123")
    else:
        print(f"⚠️  {total_tests - passed_tests} tests failed. Check the issues above.")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    run_practical_test()
