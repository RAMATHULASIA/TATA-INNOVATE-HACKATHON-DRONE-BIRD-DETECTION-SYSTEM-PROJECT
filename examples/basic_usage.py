#!/usr/bin/env python3
"""
Basic usage example for AI Co-pilot for Embedded Software Design

This example demonstrates how to use the AI co-pilot to generate
embedded code for automotive applications.
"""

import asyncio
import sys
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from ai_copilot import AICopilot, CopilotConfig
from ai_copilot.core import CodeRequest


async def main():
    """Main example function"""
    
    print("AI Co-pilot for Embedded Software Design - Basic Usage Example")
    print("=" * 60)
    
    # Create configuration
    config = CopilotConfig()
    config.debug = True
    config.log_level = "INFO"
    
    # Configure for automotive embedded systems
    config.embedded.target_architectures = ["ARM Cortex-M"]
    config.embedded.safety_level = "ASIL-B"
    config.vehicle.ecu_types = ["engine", "brake"]
    
    # Initialize the AI co-pilot
    copilot = AICopilot(config)
    
    try:
        print("\n1. Initializing AI Co-pilot...")
        await copilot.initialize()
        print("✓ AI Co-pilot initialized successfully")
        
        # Example 1: Generate CAN communication code
        print("\n2. Generating CAN communication code...")
        can_request = CodeRequest(
            description="Create a CAN message transmission function for engine RPM data",
            language="c",
            target_platform="ARM Cortex-M",
            constraints={
                "message_id": "0x123",
                "data_length": 8,
                "protocol_type": "CAN"
            }
        )
        
        can_response = await copilot.generate_code(can_request)
        
        print("Generated CAN Code:")
        print("-" * 40)
        print(can_response.generated_code)
        
        if can_response.warnings:
            print("\nWarnings:")
            for warning in can_response.warnings:
                print(f"  ⚠️  {warning}")
        
        if can_response.suggestions:
            print("\nSuggestions:")
            for suggestion in can_response.suggestions:
                print(f"  💡 {suggestion}")
        
        # Example 2: Generate AUTOSAR component
        print("\n" + "=" * 60)
        print("3. Generating AUTOSAR component...")
        
        autosar_request = CodeRequest(
            description="Create an AUTOSAR software component for brake control",
            language="c",
            target_platform="brake",
            constraints={
                "component_type": "brake_control",
                "interfaces": ["brake_pedal_input", "brake_actuator_output"]
            }
        )
        
        autosar_response = await copilot.generate_code(autosar_request)
        
        print("Generated AUTOSAR Component:")
        print("-" * 40)
        print(autosar_response.generated_code)
        
        # Example 3: Analyze existing code
        print("\n" + "=" * 60)
        print("4. Analyzing existing code...")
        
        sample_code = '''
#include <stdint.h>

void unsafe_function() {
    char buffer[1000];  // Large stack allocation
    int* ptr = malloc(100);  // Dynamic allocation without check
    
    while(1) {  // Infinite loop without yield
        // Do something
    }
    
    // Missing free(ptr)
}
'''
        
        analysis_result = await copilot.analyze_existing_code(sample_code, "c")
        
        print("Analysis Results:")
        print("-" * 40)
        
        if analysis_result.get('warnings'):
            print("Warnings found:")
            for warning in analysis_result['warnings']:
                print(f"  ⚠️  {warning}")
        
        if analysis_result.get('suggestions'):
            print("\nSuggestions:")
            for suggestion in analysis_result['suggestions']:
                print(f"  💡 {suggestion}")
        
        if analysis_result.get('metrics'):
            print("\nCode Metrics:")
            for metric, value in analysis_result['metrics'].items():
                print(f"  📊 {metric}: {value}")
        
        # Example 4: Get code completion suggestions
        print("\n" + "=" * 60)
        print("5. Getting code completion suggestions...")
        
        partial_code = '''
#include <stdint.h>
#include "can_driver.h"

void send_engine_data() {
    can_message_t msg;
    msg.id = 0x123;
    msg.dlc = 8;
    
    // Cursor position here - what should come next?
    can_'''
        
        suggestions = await copilot.get_suggestions(partial_code, len(partial_code))
        
        print("Code Completion Suggestions:")
        print("-" * 40)
        for i, suggestion in enumerate(suggestions, 1):
            print(f"  {i}. {suggestion}")
        
        print("\n" + "=" * 60)
        print("✓ All examples completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Clean up
        copilot.shutdown()
        print("\n🔧 AI Co-pilot shutdown complete")


if __name__ == "__main__":
    # Run the example
    asyncio.run(main())
