"""
AI-powered code generator for embedded systems
"""

import asyncio
from typing import Dict, List, Optional, Any, Tuple
import re
from pathlib import Path

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

from ai_copilot.config import CopilotConfig
from .templates import TemplateManager
from .validators import CodeValidator


class CodeGenerator:
    """
    AI-powered code generator specialized for embedded systems
    """
    
    def __init__(self, config: CopilotConfig):
        self.config = config
        self.template_manager = TemplateManager()
        self.validator = CodeValidator(config)
        
        # Code generation prompts for different contexts
        self.prompts = {
            "embedded_c": """
Generate embedded C code for automotive ECU with the following requirements:
- Target: {target_platform}
- Memory constraints: Flash {flash_kb}KB, RAM {ram_kb}KB
- Real-time requirements: {real_time}
- Safety level: {safety_level}
- Description: {description}

Requirements:
1. Use appropriate data types for memory efficiency
2. Include proper error handling
3. Follow MISRA C guidelines
4. Add inline comments explaining the logic
5. Consider interrupt safety if applicable

Generated code:
""",
            
            "autosar_component": """
Generate AUTOSAR component code with the following specifications:
- Component type: {component_type}
- Interfaces: {interfaces}
- Description: {description}

Requirements:
1. Follow AUTOSAR architecture patterns
2. Include proper port definitions
3. Implement runnable entities
4. Add appropriate error handling
5. Include component documentation

Generated code:
""",
            
            "can_protocol": """
Generate CAN protocol implementation for:
- Protocol: {protocol_type}
- Message ID: {message_id}
- Data length: {data_length}
- Description: {description}

Requirements:
1. Implement proper CAN frame handling
2. Include error detection and handling
3. Add message validation
4. Consider bus load optimization
5. Include diagnostic capabilities

Generated code:
"""
        }
    
    async def generate(self, request, context_info: Dict[str, Any]) -> str:
        """
        Generate code based on request and context
        
        Args:
            request: CodeRequest object
            context_info: Context information from vehicle context manager
            
        Returns:
            Generated code as string
        """
        # Determine the appropriate prompt template
        prompt_key = self._select_prompt_template(request, context_info)
        
        # Build the prompt
        prompt = self._build_prompt(prompt_key, request, context_info)
        
        # Generate code using AI model
        generated_code = await self._generate_with_model(prompt)
        
        # Post-process and validate
        processed_code = self._post_process_code(generated_code, request)
        
        # Validate the generated code
        validation_result = await self.validator.validate(processed_code, request)
        
        if not validation_result.is_valid:
            # Try to fix common issues
            processed_code = self._fix_common_issues(processed_code, validation_result)
        
        return processed_code
    
    def _select_prompt_template(self, request, context_info: Dict[str, Any]) -> str:
        """Select appropriate prompt template based on request context"""
        
        description_lower = request.description.lower()
        
        if "autosar" in description_lower or "component" in description_lower:
            return "autosar_component"
        elif "can" in description_lower or "protocol" in description_lower:
            return "can_protocol"
        else:
            return "embedded_c"
    
    def _build_prompt(self, prompt_key: str, request, context_info: Dict[str, Any]) -> str:
        """Build the complete prompt for code generation"""
        
        prompt_template = self.prompts[prompt_key]
        
        # Prepare template variables
        template_vars = {
            "description": request.description,
            "target_platform": request.target_platform or "ARM Cortex-M",
            "flash_kb": self.config.embedded.memory_constraints.get("flash_kb", 512),
            "ram_kb": self.config.embedded.memory_constraints.get("ram_kb", 64),
            "real_time": "Yes" if self.config.embedded.real_time_requirements else "No",
            "safety_level": self.config.embedded.safety_level,
        }
        
        # Add context-specific variables
        if context_info:
            template_vars.update(context_info)

        # Add request-specific constraints
        if request.constraints:
            template_vars.update(request.constraints)

        # Add default values for missing template variables
        default_values = {
            "component_type": "generic_component",
            "interfaces": "input_port, output_port",
            "protocol_type": "CAN",
            "message_id": "0x123",
            "data_length": "8"
        }

        for key, default_value in default_values.items():
            if key not in template_vars:
                template_vars[key] = default_value

        return prompt_template.format(**template_vars)
    
    async def _generate_with_model(self, prompt: str) -> str:
        """Generate code using the AI model"""
        
        # This is a placeholder for actual model inference
        # In a real implementation, you would use the loaded model
        
        # For now, return a template-based response
        if "CAN" in prompt or "protocol" in prompt:
            return self._generate_can_template()
        elif "AUTOSAR" in prompt or "component" in prompt:
            return self._generate_autosar_template()
        else:
            return self._generate_embedded_c_template()
    
    def _generate_can_template(self) -> str:
        """Generate a basic CAN protocol template"""
        return '''
#include <stdint.h>
#include <stdbool.h>
#include "can_driver.h"

// CAN message structure
typedef struct {
    uint32_t id;
    uint8_t dlc;
    uint8_t data[8];
} can_message_t;

// Function to send CAN message
bool send_can_message(uint32_t msg_id, uint8_t* data, uint8_t length) {
    can_message_t msg;
    
    // Validate input parameters
    if (data == NULL || length > 8) {
        return false;
    }
    
    // Prepare message
    msg.id = msg_id;
    msg.dlc = length;
    
    // Copy data
    for (uint8_t i = 0; i < length; i++) {
        msg.data[i] = data[i];
    }
    
    // Send message via CAN driver
    return can_transmit(&msg);
}

// Function to receive CAN message
bool receive_can_message(can_message_t* msg) {
    if (msg == NULL) {
        return false;
    }
    
    return can_receive(msg);
}
'''
    
    def _generate_autosar_template(self) -> str:
        """Generate a basic AUTOSAR component template"""
        return '''
#include "Rte_SampleComponent.h"

// Component implementation
void SampleComponent_Init(void) {
    // Initialize component resources
    // Set default values
}

void SampleComponent_MainFunction(void) {
    // Main cyclic function
    uint8_t input_data;
    uint8_t output_data;
    
    // Read input ports
    Rte_Read_InputPort_Data(&input_data);
    
    // Process data
    output_data = process_data(input_data);
    
    // Write output ports
    Rte_Write_OutputPort_Data(output_data);
}

static uint8_t process_data(uint8_t input) {
    // Data processing logic
    return input * 2; // Example processing
}
'''
    
    def _generate_embedded_c_template(self) -> str:
        """Generate a basic embedded C template"""
        return '''
#include <stdint.h>
#include <stdbool.h>

// Constants
#define MAX_BUFFER_SIZE 64
#define TIMEOUT_MS 1000

// Global variables
static uint8_t buffer[MAX_BUFFER_SIZE];
static volatile bool data_ready = false;

// Function prototypes
void initialize_system(void);
bool process_data(uint8_t* input, uint8_t length);
void error_handler(uint8_t error_code);

// System initialization
void initialize_system(void) {
    // Initialize hardware peripherals
    // Configure interrupts
    // Set initial state
    
    data_ready = false;
}

// Main processing function
bool process_data(uint8_t* input, uint8_t length) {
    // Validate input parameters
    if (input == NULL || length == 0 || length > MAX_BUFFER_SIZE) {
        error_handler(0x01); // Invalid parameters
        return false;
    }
    
    // Copy data to buffer
    for (uint8_t i = 0; i < length; i++) {
        buffer[i] = input[i];
    }
    
    // Set data ready flag
    data_ready = true;
    
    return true;
}

// Error handling function
void error_handler(uint8_t error_code) {
    // Log error
    // Take corrective action
    // Reset system if necessary
}
'''
    
    def _post_process_code(self, code: str, request) -> str:
        """Post-process generated code"""
        
        # Remove any unwanted prefixes/suffixes from model output
        code = code.strip()
        
        # Ensure proper formatting
        code = self._format_code(code)
        
        # Add header comments if requested
        if self.config.include_comments:
            code = self._add_header_comment(code, request)
        
        return code
    
    def _format_code(self, code: str) -> str:
        """Basic code formatting"""
        # Remove extra blank lines
        code = re.sub(r'\n\s*\n\s*\n', '\n\n', code)
        
        # Ensure consistent indentation (basic)
        lines = code.split('\n')
        formatted_lines = []
        indent_level = 0
        
        for line in lines:
            stripped = line.strip()
            if not stripped:
                formatted_lines.append('')
                continue
                
            # Adjust indent level
            if stripped.endswith('{'):
                formatted_lines.append('    ' * indent_level + stripped)
                indent_level += 1
            elif stripped.startswith('}'):
                indent_level = max(0, indent_level - 1)
                formatted_lines.append('    ' * indent_level + stripped)
            else:
                formatted_lines.append('    ' * indent_level + stripped)
        
        return '\n'.join(formatted_lines)
    
    def _add_header_comment(self, code: str, request) -> str:
        """Add header comment to generated code"""
        header = f'''/**
 * Generated by AI Co-pilot for Embedded Software Design
 * Description: {request.description}
 * Target Platform: {request.target_platform or 'Generic'}
 * Language: {request.language.upper()}
 * 
 * Note: This code is AI-generated and should be reviewed
 * before use in production systems.
 */

'''
        return header + code
    
    def _fix_common_issues(self, code: str, validation_result) -> str:
        """Fix common code generation issues"""
        
        # Add missing includes
        if "missing_includes" in validation_result.issues:
            for include in validation_result.issues["missing_includes"]:
                if f'#include "{include}"' not in code and f'#include <{include}>' not in code:
                    code = f'#include <{include}>\n' + code
        
        # Fix missing semicolons (basic)
        code = re.sub(r'(\w+)\s*$', r'\1;', code, flags=re.MULTILINE)
        
        return code
    
    async def get_completions(self, partial_code: str, cursor_position: int) -> List[str]:
        """Get code completion suggestions"""
        
        # Extract context around cursor
        lines = partial_code[:cursor_position].split('\n')
        current_line = lines[-1] if lines else ""
        
        # Generate context-aware suggestions
        suggestions = []
        
        # Basic keyword suggestions
        if current_line.strip().endswith('if'):
            suggestions.append('if (condition) {')
        elif current_line.strip().endswith('for'):
            suggestions.append('for (int i = 0; i < n; i++) {')
        elif current_line.strip().endswith('while'):
            suggestions.append('while (condition) {')
        
        # Function suggestions based on context
        if 'can' in partial_code.lower():
            suggestions.extend([
                'can_transmit(message);',
                'can_receive(&message);',
                'can_init();'
            ])
        
        return suggestions[:5]  # Return top 5 suggestions
