#!/usr/bin/env python3
"""
Simple demo of the AI Co-pilot API functionality
"""

import asyncio
import json
from ai_copilot import AICopilot, CopilotConfig
from ai_copilot.core import CodeRequest


async def demo_api_functionality():
    """Demonstrate the core API functionality"""
    print("🚗 AI Co-pilot API Functionality Demo")
    print("=" * 50)
    
    # Initialize the AI Co-pilot
    config = CopilotConfig()
    copilot = AICopilot(config)
    
    try:
        print("🚀 Initializing AI Co-pilot...")
        await copilot.initialize()
        print("✓ AI Co-pilot initialized successfully")
        
        # Demo 1: Code Generation
        print("\n1. 🔧 Code Generation Demo")
        print("-" * 30)
        
        request = CodeRequest(
            description="Create a CAN message handler for brake system data",
            language="c",
            target_platform="ARM Cortex-M",
            constraints={
                "message_id": "0x200",
                "data_length": 8
            }
        )
        
        print(f"Request: {request.description}")
        print(f"Platform: {request.target_platform}")
        
        response = await copilot.generate_code(request)
        
        print(f"✓ Generated {len(response.generated_code)} characters of code")
        print(f"📝 Explanation: {response.explanation}")
        print(f"⚠️  Warnings: {len(response.warnings)}")
        print(f"💡 Suggestions: {len(response.suggestions)}")
        
        # Show code snippet
        code_lines = response.generated_code.split('\n')
        print("\n📄 Generated Code (first 15 lines):")
        for i, line in enumerate(code_lines[:15], 1):
            print(f"{i:2d}: {line}")
        if len(code_lines) > 15:
            print(f"... and {len(code_lines) - 15} more lines")
        
        # Demo 2: Code Analysis
        print("\n\n2. 🔍 Code Analysis Demo")
        print("-" * 30)
        
        sample_code = '''
#include <stdio.h>
#include <stdlib.h>

void brake_control_function() {
    char large_buffer[2000];  // Large stack allocation
    int* sensor_data = malloc(500);  // Dynamic allocation
    
    printf("Brake system active\\n");  // Not suitable for embedded
    
    while(1) {  // Infinite loop without yield
        if (sensor_data[100] > 50) {  // Potential buffer overflow
            goto emergency_stop;  // MISRA C violation
        }
    }
    
    emergency_stop:
    // Missing free(sensor_data) - memory leak
    return;
}
'''
        
        print("Analyzing problematic embedded code...")
        analysis = await copilot.analyze_existing_code(sample_code, "c")
        
        print(f"✓ Analysis completed")
        print(f"⚠️  Warnings found: {len(analysis.get('warnings', []))}")
        print(f"💡 Suggestions: {len(analysis.get('suggestions', []))}")
        
        # Show warnings
        if analysis.get('warnings'):
            print("\n🚨 Key Warnings:")
            for i, warning in enumerate(analysis['warnings'][:3], 1):
                print(f"  {i}. {warning}")
        
        # Show metrics
        if analysis.get('metrics'):
            print("\n📊 Code Metrics:")
            for metric, value in analysis['metrics'].items():
                print(f"  • {metric.replace('_', ' ').title()}: {value}")
        
        # Demo 3: Code Suggestions
        print("\n\n3. 💡 Code Completion Demo")
        print("-" * 30)
        
        partial_code = '''
#include <stdint.h>
#include "can_driver.h"

void send_brake_data() {
    can_message_t msg;
    msg.id = 0x200;
    msg.dlc = 4;
    
    // Cursor position here - what should come next?
    can_'''
        
        print("Getting code completion suggestions...")
        suggestions = await copilot.get_suggestions(partial_code, len(partial_code))
        
        print(f"✓ Found {len(suggestions)} suggestions:")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"  {i}. {suggestion}")
        
        print("\n" + "=" * 50)
        print("🎉 Demo completed successfully!")
        print("\n📚 This demonstrates the core functionality that powers:")
        print("  • Web API endpoints (/api/generate, /api/analyze)")
        print("  • Command line interface (ai-copilot CLI)")
        print("  • React web frontend (when built)")
        
        print("\n🌐 To start the web server:")
        print("  python -m uvicorn web_api.main:app --host 0.0.0.0 --port 8000")
        print("  Then visit: http://localhost:8000")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        copilot.shutdown()
        print("\n🔧 AI Co-pilot shutdown complete")


if __name__ == "__main__":
    asyncio.run(demo_api_functionality())
