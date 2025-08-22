"""
Code validators for embedded systems
"""

import re
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

from ai_copilot.config import CopilotConfig


@dataclass
class ValidationResult:
    """Result of code validation"""
    is_valid: bool
    issues: Dict[str, List[str]]
    suggestions: List[str]


class CodeValidator:
    """
    Validates generated code for embedded systems compliance
    """
    
    def __init__(self, config: CopilotConfig):
        self.config = config
    
    async def validate(self, code: str, request) -> ValidationResult:
        """
        Validate generated code
        
        Args:
            code: Generated code to validate
            request: Original code request
            
        Returns:
            ValidationResult with validation status and issues
        """
        
        issues = {}
        suggestions = []
        
        # Syntax validation
        syntax_issues = self._validate_syntax(code, request.language)
        if syntax_issues:
            issues['syntax'] = syntax_issues
        
        # Include validation
        include_issues = self._validate_includes(code)
        if include_issues:
            issues['missing_includes'] = include_issues
        
        # Memory safety validation
        memory_issues = self._validate_memory_safety(code)
        if memory_issues:
            issues['memory_safety'] = memory_issues
            suggestions.extend([
                "Review memory allocation patterns",
                "Consider using static allocation instead of dynamic"
            ])
        
        # Embedded-specific validation
        embedded_issues = self._validate_embedded_constraints(code)
        if embedded_issues:
            issues['embedded_constraints'] = embedded_issues
        
        is_valid = len(issues) == 0
        
        return ValidationResult(
            is_valid=is_valid,
            issues=issues,
            suggestions=suggestions
        )
    
    def _validate_syntax(self, code: str, language: str) -> List[str]:
        """Basic syntax validation"""
        issues = []
        
        if language.lower() in ['c', 'cpp']:
            # Check for basic C/C++ syntax issues
            
            # Check for unmatched braces
            open_braces = code.count('{')
            close_braces = code.count('}')
            if open_braces != close_braces:
                issues.append(f"Unmatched braces: {open_braces} open, {close_braces} close")
            
            # Check for unmatched parentheses
            open_parens = code.count('(')
            close_parens = code.count(')')
            if open_parens != close_parens:
                issues.append(f"Unmatched parentheses: {open_parens} open, {close_parens} close")
            
            # Check for missing semicolons (basic check)
            lines = code.split('\n')
            for i, line in enumerate(lines, 1):
                stripped = line.strip()
                if (stripped and 
                    not stripped.startswith('#') and 
                    not stripped.startswith('//') and
                    not stripped.startswith('/*') and
                    not stripped.endswith(';') and
                    not stripped.endswith('{') and
                    not stripped.endswith('}') and
                    not stripped.endswith('*/') and
                    'return' in stripped):
                    issues.append(f"Possible missing semicolon at line {i}")
        
        return issues
    
    def _validate_includes(self, code: str) -> List[str]:
        """Check for missing includes"""
        missing_includes = []
        
        # Common function to include mappings
        function_includes = {
            'printf': 'stdio.h',
            'malloc': 'stdlib.h',
            'free': 'stdlib.h',
            'memcpy': 'string.h',
            'memset': 'string.h',
            'strlen': 'string.h',
            'uint8_t': 'stdint.h',
            'uint16_t': 'stdint.h',
            'uint32_t': 'stdint.h',
            'bool': 'stdbool.h',
            'true': 'stdbool.h',
            'false': 'stdbool.h'
        }
        
        for func, include in function_includes.items():
            if func in code and f'#include <{include}>' not in code:
                missing_includes.append(include)
        
        return list(set(missing_includes))  # Remove duplicates
    
    def _validate_memory_safety(self, code: str) -> List[str]:
        """Validate memory safety"""
        issues = []
        
        # Check for potential buffer overflows
        array_access_pattern = r'(\w+)\[([^]]+)\]'
        matches = re.findall(array_access_pattern, code)
        
        for array_name, index in matches:
            # Basic check for potential issues
            if index.isdigit():
                # Static index - would need array size info to validate
                pass
            elif '+' in index or '-' in index:
                issues.append(f"Complex array indexing detected for '{array_name}' - verify bounds checking")
        
        # Check for unchecked malloc
        if 'malloc(' in code:
            # Look for malloc without null check
            malloc_pattern = r'(\w+)\s*=\s*malloc\s*\([^)]+\)\s*;'
            malloc_matches = re.findall(malloc_pattern, code)
            
            for var_name in malloc_matches:
                null_check_pattern = rf'if\s*\(\s*{var_name}\s*==\s*NULL\s*\)'
                if not re.search(null_check_pattern, code):
                    issues.append(f"malloc result '{var_name}' not checked for NULL")
        
        return issues
    
    def _validate_embedded_constraints(self, code: str) -> List[str]:
        """Validate embedded-specific constraints"""
        issues = []
        
        # Check for floating point usage (may not be available on all embedded systems)
        if re.search(r'\bfloat\b|\bdouble\b', code):
            issues.append("Floating point types detected - verify FPU availability on target")
        
        # Check for large stack allocations
        large_array_pattern = r'(\w+)\s+\w+\[\s*(\d+)\s*\]'
        matches = re.findall(large_array_pattern, code)
        
        for data_type, size in matches:
            try:
                array_size = int(size)
                if array_size > 1024:  # Arbitrary threshold
                    issues.append(f"Large stack allocation detected: {array_size} elements of {data_type}")
            except ValueError:
                pass
        
        # Check for recursive functions
        function_pattern = r'(\w+)\s*\([^)]*\)\s*{([^}]*)}'
        functions = re.findall(function_pattern, code, re.DOTALL)
        
        for func_name, func_body in functions:
            if func_name in func_body:
                issues.append(f"Recursive function '{func_name}' detected - may cause stack overflow")
        
        return issues
