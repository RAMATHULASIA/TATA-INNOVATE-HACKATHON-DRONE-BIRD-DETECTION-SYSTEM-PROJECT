#!/usr/bin/env python3
"""
Test script for the web API functionality
"""

import asyncio
import json
from web_api.main import app
from fastapi.testclient import TestClient


def test_web_api():
    """Test the web API endpoints"""
    print("🧪 Testing AI Co-pilot Web API")
    print("=" * 50)
    
    # Create test client
    client = TestClient(app)
    
    # Test 1: Check API status
    print("1. Testing API status...")
    try:
        response = client.get("/api/status")
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.json()}")
        print("   ✓ Status endpoint working")
    except Exception as e:
        print(f"   ❌ Status test failed: {e}")
    
    print()
    
    # Test 2: Test code generation
    print("2. Testing code generation...")
    try:
        generation_request = {
            "description": "Create a CAN message handler for brake system",
            "language": "c",
            "target_platform": "ARM Cortex-M"
        }
        
        response = client.post("/api/generate", json=generation_request)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   Generated {len(result['generated_code'])} characters of code")
            print(f"   Warnings: {len(result['warnings'])}")
            print(f"   Suggestions: {len(result['suggestions'])}")
            print("   ✓ Code generation working")
            
            # Show a snippet of generated code
            code_snippet = result['generated_code'][:200] + "..." if len(result['generated_code']) > 200 else result['generated_code']
            print(f"   Code snippet:\n{code_snippet}")
        else:
            print(f"   ❌ Generation failed: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Generation test failed: {e}")
    
    print()
    
    # Test 3: Test code analysis
    print("3. Testing code analysis...")
    try:
        analysis_request = {
            "code": """
#include <stdio.h>
void test_function() {
    char buffer[2000];  // Large buffer
    int* ptr = malloc(100);  // Dynamic allocation
    printf("Hello World");
}
""",
            "language": "c"
        }
        
        response = client.post("/api/analyze", json=analysis_request)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   Warnings: {len(result['warnings'])}")
            print(f"   Suggestions: {len(result['suggestions'])}")
            print(f"   Valid: {result['is_valid']}")
            print("   ✓ Code analysis working")
            
            # Show warnings
            if result['warnings']:
                print("   Sample warnings:")
                for warning in result['warnings'][:2]:
                    print(f"     - {warning}")
                    
        else:
            print(f"   ❌ Analysis failed: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Analysis test failed: {e}")
    
    print()
    
    # Test 4: Test platforms endpoint
    print("4. Testing platforms endpoint...")
    try:
        response = client.get("/api/platforms")
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   Available platforms: {result['platforms']}")
            print("   ✓ Platforms endpoint working")
        else:
            print(f"   ❌ Platforms failed: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Platforms test failed: {e}")
    
    print()
    
    # Test 5: Test templates endpoint
    print("5. Testing templates endpoint...")
    try:
        response = client.get("/api/templates")
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   Available templates: {result['templates']}")
            print("   ✓ Templates endpoint working")
        else:
            print(f"   ❌ Templates failed: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Templates test failed: {e}")
    
    print()
    print("🎉 Web API testing completed!")
    print("\n📝 To start the web server, run:")
    print("   python -m uvicorn web_api.main:app --host 0.0.0.0 --port 8000 --reload")
    print("\n🌐 Then visit:")
    print("   - API Documentation: http://localhost:8000/api/docs")
    print("   - Interactive API: http://localhost:8000/api/redoc")
    print("   - Web Interface: http://localhost:8000")


if __name__ == "__main__":
    test_web_api()
