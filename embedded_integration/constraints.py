"""
Constraint checker for embedded systems
"""

from typing import Dict, List, Optional, Any
from ai_copilot.config import CopilotConfig


class ConstraintChecker:
    """
    Checks code against embedded system constraints
    """
    
    def __init__(self, config: CopilotConfig):
        self.config = config
    
    async def check_constraints(self, code: str, constraints: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        Check code against specified constraints
        
        Args:
            code: Source code to check
            constraints: Constraints to validate against
            
        Returns:
            Dictionary with warnings and suggestions
        """
        
        warnings = []
        suggestions = []
        
        # Memory constraints
        if 'memory' in constraints:
            memory_warnings = self._check_memory_constraints(code, constraints['memory'])
            warnings.extend(memory_warnings)
        
        # Timing constraints
        if 'timing' in constraints:
            timing_warnings = self._check_timing_constraints(code, constraints['timing'])
            warnings.extend(timing_warnings)
        
        # Power constraints
        if 'power' in constraints:
            power_warnings = self._check_power_constraints(code, constraints['power'])
            warnings.extend(power_warnings)
        
        return {
            'warnings': warnings,
            'suggestions': suggestions
        }
    
    def _check_memory_constraints(self, code: str, memory_constraints: Dict[str, Any]) -> List[str]:
        """Check memory-related constraints"""
        warnings = []
        
        # Check for memory usage patterns
        if 'max_stack_usage' in memory_constraints:
            # Estimate stack usage (simplified)
            estimated_stack = self._estimate_stack_usage(code)
            max_allowed = memory_constraints['max_stack_usage']
            
            if estimated_stack > max_allowed:
                warnings.append(
                    f"Estimated stack usage ({estimated_stack} bytes) exceeds "
                    f"constraint ({max_allowed} bytes)"
                )
        
        return warnings
    
    def _check_timing_constraints(self, code: str, timing_constraints: Dict[str, Any]) -> List[str]:
        """Check timing-related constraints"""
        warnings = []
        
        # Check for real-time violations
        if timing_constraints.get('real_time_required', False):
            if 'malloc' in code or 'printf' in code:
                warnings.append(
                    "Non-deterministic functions detected in real-time code"
                )
        
        return warnings
    
    def _check_power_constraints(self, code: str, power_constraints: Dict[str, Any]) -> List[str]:
        """Check power-related constraints"""
        warnings = []
        
        # Check for power-hungry operations
        if power_constraints.get('low_power_mode', False):
            if 'while(1)' in code.replace(' ', ''):
                warnings.append(
                    "Busy-wait loops detected in low-power mode"
                )
        
        return warnings
    
    def _estimate_stack_usage(self, code: str) -> int:
        """Estimate stack usage (simplified implementation)"""
        # This is a very basic estimation
        # In practice, you'd need more sophisticated analysis
        
        import re
        
        # Count local variable declarations
        var_patterns = [
            r'int\s+\w+',
            r'char\s+\w+\[\s*(\d+)\s*\]',
            r'uint8_t\s+\w+\[\s*(\d+)\s*\]'
        ]
        
        total_bytes = 0
        
        for pattern in var_patterns:
            matches = re.findall(pattern, code)
            for match in matches:
                if isinstance(match, str) and match.isdigit():
                    total_bytes += int(match)
                else:
                    total_bytes += 4  # Assume 4 bytes for basic types
        
        return total_bytes
