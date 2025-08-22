#!/usr/bin/env python3
"""
Basic test script to verify the AI Co-pilot functionality

This script tests the core components without requiring heavy AI models.
"""

import asyncio
import sys
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from ai_copilot.config import CopilotConfig
from code_generation.generator import CodeGenerator
from code_generation.validators import CodeValidator
from embedded_integration.analyzer import EmbeddedAnalyzer
from vehicle_context.context_manager import VehicleContextManager


async def test_configuration():
    """Test configuration loading and setup"""
    print("Testing Configuration...")
    
    config = CopilotConfig()
    assert config.model.name is not None
    assert config.embedded.target_architectures is not None
    assert config.vehicle.ecu_types is not None
    
    # Test configuration file operations
    test_config_path = "test_config.yaml"
    config.to_file(test_config_path)
    
    loaded_config = CopilotConfig.from_file(test_config_path)
    assert loaded_config.model.name == config.model.name
    
    # Cleanup
    Path(test_config_path).unlink()
    
    print("✓ Configuration tests passed")


async def test_code_generator():
    """Test code generation functionality"""
    print("Testing Code Generator...")
    
    config = CopilotConfig()
    generator = CodeGenerator(config)
    
    # Test template-based generation (without AI model)
    can_code = generator._generate_can_template()
    assert "can_message_t" in can_code
    assert "can_transmit" in can_code
    
    autosar_code = generator._generate_autosar_template()
    assert "SampleComponent" in autosar_code
    assert "Rte_" in autosar_code
    
    embedded_code = generator._generate_embedded_c_template()
    assert "#include" in embedded_code
    assert "initialize_system" in embedded_code
    
    print("✓ Code Generator tests passed")


async def test_code_validator():
    """Test code validation functionality"""
    print("Testing Code Validator...")
    
    config = CopilotConfig()
    validator = CodeValidator(config)
    
    # Test with valid code
    valid_code = '''
#include <stdint.h>
#include <stdbool.h>

bool test_function(uint8_t input) {
    if (input > 100) {
        return false;
    }
    return true;
}
'''
    
    class MockRequest:
        language = "c"
    
    result = await validator.validate(valid_code, MockRequest())
    assert result.is_valid or len(result.issues) == 0  # Should be mostly valid
    
    # Test with problematic code
    problematic_code = '''
void bad_function() {
    char buffer[2000];  // Large stack allocation
    int* ptr = malloc(100);  // No null check
    printf("Hello");  // Embedded-unsafe function
}
'''
    
    result = await validator.validate(problematic_code, MockRequest())
    assert len(result.issues) > 0  # Should find issues
    
    print("✓ Code Validator tests passed")


async def test_embedded_analyzer():
    """Test embedded systems analyzer"""
    print("Testing Embedded Analyzer...")
    
    config = CopilotConfig()
    analyzer = EmbeddedAnalyzer(config)
    
    # Test memory analysis
    test_code = '''
#include <stdint.h>

void test_function() {
    char large_buffer[1024];  // Large local array
    int* ptr = malloc(100);   // Dynamic allocation
    
    while(1) {  // Infinite loop
        // Do something
    }
}
'''
    
    analysis = await analyzer.analyze_code(test_code)
    
    assert 'warnings' in analysis
    assert 'suggestions' in analysis
    assert 'metrics' in analysis
    
    # Should detect memory issues
    warnings = analysis['warnings']
    assert any('allocation' in warning.lower() for warning in warnings)
    
    print("✓ Embedded Analyzer tests passed")


async def test_vehicle_context():
    """Test vehicle context manager"""
    print("Testing Vehicle Context Manager...")
    
    config = CopilotConfig()
    context_manager = VehicleContextManager(config)
    
    # Test ECU type identification
    ecu_type = context_manager._identify_ecu_type("engine control system", None)
    assert ecu_type == "engine"
    
    ecu_type = context_manager._identify_ecu_type("brake control", None)
    assert ecu_type == "brake"
    
    # Test protocol identification
    protocols = context_manager._identify_protocols("CAN bus communication")
    assert "CAN" in protocols
    
    protocols = context_manager._identify_protocols("LIN network setup")
    assert "LIN" in protocols
    
    # Test context analysis
    context = await context_manager.analyze_context(
        "Create CAN communication for engine ECU", 
        "engine"
    )
    
    assert context['ecu_type'] == 'engine'
    assert 'protocols' in context
    assert 'constraints' in context
    
    print("✓ Vehicle Context Manager tests passed")


async def test_integration():
    """Test integration between components"""
    print("Testing Component Integration...")
    
    config = CopilotConfig()
    
    # Test that all components can be instantiated together
    generator = CodeGenerator(config)
    validator = CodeValidator(config)
    analyzer = EmbeddedAnalyzer(config)
    context_manager = VehicleContextManager(config)
    
    # Test a simple workflow
    description = "CAN message transmission for engine RPM"
    context = await context_manager.analyze_context(description, "engine")
    
    # Generate some code (template-based)
    code = generator._generate_can_template()
    
    # Validate the code
    class MockRequest:
        language = "c"
    
    validation_result = await validator.validate(code, MockRequest())
    
    # Analyze the code
    analysis_result = await analyzer.analyze_code(code)
    
    # All operations should complete without errors
    assert context is not None
    assert code is not None
    assert validation_result is not None
    assert analysis_result is not None
    
    print("✓ Integration tests passed")


async def main():
    """Run all tests"""
    print("AI Co-pilot for Embedded Software Design - Basic Tests")
    print("=" * 60)
    
    try:
        await test_configuration()
        await test_code_generator()
        await test_code_validator()
        await test_embedded_analyzer()
        await test_vehicle_context()
        await test_integration()
        
        print("\n" + "=" * 60)
        print("🎉 All tests passed successfully!")
        print("\nThe AI Co-pilot system is ready for use.")
        print("Try running: python examples/basic_usage.py")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
