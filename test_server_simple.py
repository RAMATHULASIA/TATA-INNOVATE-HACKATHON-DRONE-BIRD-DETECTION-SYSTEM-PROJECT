#!/usr/bin/env python3
"""
Simple server test without import conflicts
"""

def test_server():
    print("🔍 TATA AI Co-pilot - Server Test")
    print("=" * 50)
    
    try:
        import requests
        
        # Test main page
        try:
            response = requests.get('http://localhost:8000/', timeout=5)
            print(f"✅ Main Page: {response.status_code}")
        except Exception as e:
            print(f"❌ Main Page Error: {e}")
        
        # Test API status
        try:
            response = requests.get('http://localhost:8000/api/status', timeout=5)
            print(f"✅ API Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   Status: {data.get('status', 'N/A')}")
                print(f"   Message: {data.get('message', 'N/A')}")
        except Exception as e:
            print(f"❌ API Status Error: {e}")
        
        # Test code generation
        try:
            gen_data = {
                'description': 'Create a simple TATA vehicle CAN handler',
                'language': 'c',
                'target_platform': 'ARM Cortex-M'
            }
            response = requests.post('http://localhost:8000/api/generate', json=gen_data, timeout=15)
            print(f"✅ Code Generation: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                code_len = len(result.get('generated_code', ''))
                exp_len = len(result.get('explanation', ''))
                warnings = len(result.get('warnings', []))
                suggestions = len(result.get('suggestions', []))
                
                print(f"   Generated Code: {code_len} characters")
                print(f"   Explanation: {exp_len} characters")
                print(f"   Warnings: {warnings}")
                print(f"   Suggestions: {suggestions}")
                
                if code_len > 0:
                    print("🎉 Code generation is working!")
                    # Show first few lines
                    code = result.get('generated_code', '')
                    lines = code.split('\n')[:5]
                    print("   Sample code:")
                    for i, line in enumerate(lines, 1):
                        print(f"     {i}: {line}")
                else:
                    print("⚠️  Code generation returned empty result")
            else:
                print(f"   Error: {response.text[:200]}")
                
        except Exception as e:
            print(f"❌ Code Generation Error: {e}")
        
        print("\n" + "=" * 50)
        print("🎯 Server Test Complete")
        
    except ImportError:
        print("❌ requests module not available")
        print("   Install with: pip install requests")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    test_server()
