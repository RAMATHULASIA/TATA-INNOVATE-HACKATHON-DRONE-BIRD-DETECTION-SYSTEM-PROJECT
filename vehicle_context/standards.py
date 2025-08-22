"""
Automotive standards checker (AUTOSAR, ISO 26262, etc.)
"""

from typing import Dict, List, Optional, Any
import re
from ai_copilot.config import CopilotConfig


class StandardsChecker:
    """
    Checks code compliance with automotive standards
    """
    
    def __init__(self, config: CopilotConfig):
        self.config = config
        self.standards = self._load_standards()
    
    def _load_standards(self) -> Dict[str, Dict[str, Any]]:
        """Load automotive standards information"""
        return {
            "AUTOSAR": {
                "version": "4.4",
                "components": ["SWC", "BSW", "RTE"],
                "naming_conventions": {
                    "functions": "PascalCase",
                    "variables": "camelCase",
                    "constants": "UPPER_CASE"
                },
                "required_patterns": [
                    "component_initialization",
                    "port_interfaces",
                    "runnable_entities"
                ]
            },
            "ISO26262": {
                "name": "Functional Safety for Road Vehicles",
                "asil_levels": ["QM", "ASIL-A", "ASIL-B", "ASIL-C", "ASIL-D"],
                "safety_requirements": [
                    "error_detection",
                    "error_handling",
                    "fail_safe_behavior",
                    "diagnostic_coverage"
                ]
            },
            "MISRA-C": {
                "version": "2012",
                "categories": ["mandatory", "required", "advisory"],
                "common_rules": [
                    "no_goto",
                    "no_magic_numbers",
                    "proper_error_handling",
                    "consistent_naming"
                ]
            }
        }
    
    async def check_autosar_compliance(self, code: str) -> Dict[str, Any]:
        """
        Check AUTOSAR compliance
        
        Args:
            code: Source code to check
            
        Returns:
            AUTOSAR compliance results
        """
        
        compliance_results = {
            "standard": "AUTOSAR",
            "version": self.standards["AUTOSAR"]["version"],
            "compliant": True,
            "violations": [],
            "warnings": [],
            "suggestions": []
        }
        
        # Check for AUTOSAR component structure
        if not self._has_autosar_structure(code):
            compliance_results["violations"].append(
                "Missing AUTOSAR component structure"
            )
            compliance_results["suggestions"].append(
                "Implement proper AUTOSAR SWC structure with ports and runnables"
            )
        
        # Check naming conventions
        naming_issues = self._check_autosar_naming(code)
        if naming_issues:
            compliance_results["warnings"].extend(naming_issues)
        
        # Check for required includes
        if "#include \"Rte_" not in code and "autosar" in code.lower():
            compliance_results["warnings"].append(
                "Missing RTE header include for AUTOSAR component"
            )
            compliance_results["suggestions"].append(
                "Include appropriate Rte_<ComponentName>.h header"
            )
        
        compliance_results["compliant"] = len(compliance_results["violations"]) == 0
        
        return compliance_results
    
    async def check_iso26262_compliance(self, code: str) -> Dict[str, Any]:
        """
        Check ISO 26262 functional safety compliance
        
        Args:
            code: Source code to check
            
        Returns:
            ISO 26262 compliance results
        """
        
        compliance_results = {
            "standard": "ISO 26262",
            "asil_level": self.config.embedded.safety_level,
            "compliant": True,
            "violations": [],
            "warnings": [],
            "suggestions": []
        }
        
        # Check for error handling
        if not self._has_error_handling(code):
            compliance_results["violations"].append(
                "Insufficient error handling for safety-critical code"
            )
            compliance_results["suggestions"].append(
                "Add comprehensive error detection and handling mechanisms"
            )
        
        # Check for fail-safe behavior
        if not self._has_fail_safe_behavior(code):
            compliance_results["warnings"].append(
                "Fail-safe behavior not evident in code"
            )
            compliance_results["suggestions"].append(
                "Implement fail-safe states and transitions"
            )
        
        # Check for diagnostic capabilities
        if self.config.embedded.safety_level in ["ASIL-C", "ASIL-D"]:
            if not self._has_diagnostics(code):
                compliance_results["violations"].append(
                    f"Missing diagnostic capabilities for {self.config.embedded.safety_level}"
                )
                compliance_results["suggestions"].append(
                    "Implement diagnostic and monitoring functions"
                )
        
        compliance_results["compliant"] = len(compliance_results["violations"]) == 0
        
        return compliance_results
    
    def _has_autosar_structure(self, code: str) -> bool:
        """Check if code has AUTOSAR component structure"""
        autosar_indicators = [
            "Rte_",
            "_Init(",
            "_MainFunction(",
            "Runnable",
            "Port"
        ]
        
        return any(indicator in code for indicator in autosar_indicators)
    
    def _check_autosar_naming(self, code: str) -> List[str]:
        """Check AUTOSAR naming conventions"""
        issues = []
        
        # Check function naming (should be PascalCase for AUTOSAR)
        function_pattern = r'(\w+)\s*\([^)]*\)\s*{'
        functions = re.findall(function_pattern, code)
        
        for func_name in functions:
            if func_name[0].islower() and not func_name.startswith('_'):
                issues.append(
                    f"Function '{func_name}' should use PascalCase naming"
                )
        
        return issues
    
    def _has_error_handling(self, code: str) -> bool:
        """Check if code has proper error handling"""
        error_indicators = [
            "if (",
            "return",
            "error",
            "Error",
            "ERROR",
            "!=",
            "==",
            "NULL"
        ]
        
        # Simple heuristic: if code has conditional checks and returns, 
        # assume it has some error handling
        has_conditionals = any("if (" in line for line in code.split('\n'))
        has_returns = any("return" in line for line in code.split('\n'))
        
        return has_conditionals and has_returns
    
    def _has_fail_safe_behavior(self, code: str) -> bool:
        """Check if code implements fail-safe behavior"""
        fail_safe_indicators = [
            "fail_safe",
            "safe_state",
            "emergency",
            "shutdown",
            "disable"
        ]
        
        code_lower = code.lower()
        return any(indicator in code_lower for indicator in fail_safe_indicators)
    
    def _has_diagnostics(self, code: str) -> bool:
        """Check if code has diagnostic capabilities"""
        diagnostic_indicators = [
            "diagnostic",
            "dtc",
            "monitor",
            "check",
            "status",
            "health"
        ]
        
        code_lower = code.lower()
        return any(indicator in code_lower for indicator in diagnostic_indicators)
