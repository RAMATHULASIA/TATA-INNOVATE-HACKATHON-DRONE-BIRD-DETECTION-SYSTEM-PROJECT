"""
Embedded Systems Code Analyzer

Analyzes code for embedded systems constraints including memory usage,
real-time requirements, and platform-specific optimizations.
"""

import re
import ast
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from pathlib import Path

from ai_copilot.config import CopilotConfig
from .constraints import ConstraintChecker
from .platforms import PlatformManager


@dataclass
class AnalysisResult:
    """Results from code analysis"""
    is_valid: bool
    warnings: List[str]
    suggestions: List[str]
    metrics: Dict[str, Any]
    issues: Dict[str, List[str]]


class EmbeddedAnalyzer:
    """
    Analyzes code for embedded systems compliance and optimization
    """
    
    def __init__(self, config: CopilotConfig):
        self.config = config
        self.constraint_checker = ConstraintChecker(config)
        self.platform_manager = PlatformManager(config)
        
        # Common embedded patterns and anti-patterns
        self.memory_patterns = {
            'dynamic_allocation': [
                r'\bmalloc\s*\(',
                r'\bcalloc\s*\(',
                r'\brealloc\s*\(',
                r'\bfree\s*\(',
                r'\bnew\s+\w+',
                r'\bdelete\s+'
            ],
            'stack_usage': [
                r'char\s+\w+\[\s*(\d+)\s*\]',
                r'int\s+\w+\[\s*(\d+)\s*\]',
                r'uint8_t\s+\w+\[\s*(\d+)\s*\]'
            ],
            'recursion': [
                r'(\w+)\s*\([^)]*\)\s*{[^}]*\1\s*\('
            ]
        }
        
        self.timing_patterns = {
            'blocking_calls': [
                r'\bdelay\s*\(',
                r'\bsleep\s*\(',
                r'\bwait\s*\(',
                r'while\s*\(\s*1\s*\)',
                r'for\s*\(\s*;\s*;\s*\)'
            ],
            'interrupt_unsafe': [
                r'printf\s*\(',
                r'malloc\s*\(',
                r'free\s*\('
            ]
        }
    
    async def analyze_code(self, code: str, constraints: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Perform comprehensive analysis of embedded code
        
        Args:
            code: Source code to analyze
            constraints: Additional constraints to check
            
        Returns:
            Analysis results with warnings, suggestions, and metrics
        """
        
        analysis_result = AnalysisResult(
            is_valid=True,
            warnings=[],
            suggestions=[],
            metrics={},
            issues={}
        )
        
        # Memory analysis
        memory_analysis = self._analyze_memory_usage(code)
        analysis_result.metrics.update(memory_analysis['metrics'])
        analysis_result.warnings.extend(memory_analysis['warnings'])
        analysis_result.suggestions.extend(memory_analysis['suggestions'])
        
        # Timing analysis
        timing_analysis = self._analyze_timing_constraints(code)
        analysis_result.warnings.extend(timing_analysis['warnings'])
        analysis_result.suggestions.extend(timing_analysis['suggestions'])
        
        # Platform-specific analysis
        platform_analysis = await self._analyze_platform_compatibility(code)
        analysis_result.warnings.extend(platform_analysis['warnings'])
        analysis_result.suggestions.extend(platform_analysis['suggestions'])
        
        # Safety analysis
        safety_analysis = self._analyze_safety_compliance(code)
        analysis_result.warnings.extend(safety_analysis['warnings'])
        analysis_result.suggestions.extend(safety_analysis['suggestions'])
        
        # Check custom constraints
        if constraints:
            constraint_analysis = await self.constraint_checker.check_constraints(code, constraints)
            analysis_result.warnings.extend(constraint_analysis['warnings'])
            analysis_result.suggestions.extend(constraint_analysis['suggestions'])
        
        # Determine overall validity
        analysis_result.is_valid = len(analysis_result.warnings) == 0
        
        return {
            'explanation': self._generate_explanation(analysis_result),
            'warnings': analysis_result.warnings,
            'suggestions': analysis_result.suggestions,
            'metrics': analysis_result.metrics,
            'is_valid': analysis_result.is_valid
        }
    
    def _analyze_memory_usage(self, code: str) -> Dict[str, Any]:
        """Analyze memory usage patterns"""
        
        warnings = []
        suggestions = []
        metrics = {
            'estimated_stack_usage': 0,
            'dynamic_allocations': 0,
            'large_arrays': []
        }
        
        # Check for dynamic memory allocation
        for pattern in self.memory_patterns['dynamic_allocation']:
            matches = re.findall(pattern, code, re.IGNORECASE)
            if matches:
                metrics['dynamic_allocations'] += len(matches)
                warnings.append(
                    f"Dynamic memory allocation detected ({len(matches)} instances). "
                    "Consider using static allocation for embedded systems."
                )
                suggestions.append(
                    "Replace dynamic allocation with static arrays or memory pools."
                )
        
        # Analyze stack usage from local arrays
        for pattern in self.memory_patterns['stack_usage']:
            matches = re.findall(pattern, code)
            for match in matches:
                try:
                    size = int(match)
                    metrics['estimated_stack_usage'] += size
                    if size > 1024:  # Large array threshold
                        metrics['large_arrays'].append(size)
                        warnings.append(
                            f"Large local array detected ({size} bytes). "
                            "Consider using static or heap allocation."
                        )
                except ValueError:
                    pass
        
        # Check for recursion
        for pattern in self.memory_patterns['recursion']:
            matches = re.findall(pattern, code, re.DOTALL)
            if matches:
                warnings.append(
                    "Recursive function detected. Recursion can cause stack overflow "
                    "in embedded systems with limited stack space."
                )
                suggestions.append(
                    "Consider converting recursive algorithms to iterative ones."
                )
        
        return {
            'warnings': warnings,
            'suggestions': suggestions,
            'metrics': metrics
        }
    
    def _analyze_timing_constraints(self, code: str) -> Dict[str, Any]:
        """Analyze real-time and timing constraints"""
        
        warnings = []
        suggestions = []
        
        # Check for blocking calls
        for pattern in self.timing_patterns['blocking_calls']:
            matches = re.findall(pattern, code, re.IGNORECASE)
            if matches:
                warnings.append(
                    f"Blocking call detected ({pattern}). This may violate "
                    "real-time constraints in interrupt handlers or critical sections."
                )
                suggestions.append(
                    "Use non-blocking alternatives or move to background tasks."
                )
        
        # Check for interrupt-unsafe operations
        for pattern in self.timing_patterns['interrupt_unsafe']:
            matches = re.findall(pattern, code, re.IGNORECASE)
            if matches:
                warnings.append(
                    f"Interrupt-unsafe operation detected ({pattern}). "
                    "Avoid using in interrupt service routines."
                )
                suggestions.append(
                    "Use interrupt-safe alternatives or defer to main loop."
                )
        
        # Check for infinite loops without yield
        infinite_loop_pattern = r'while\s*\(\s*1\s*\)\s*{[^}]*}'
        matches = re.findall(infinite_loop_pattern, code, re.DOTALL)
        for match in matches:
            if 'yield' not in match and 'delay' not in match and 'sleep' not in match:
                warnings.append(
                    "Infinite loop without yield detected. This may starve other tasks."
                )
                suggestions.append(
                    "Add appropriate delays or yield points in infinite loops."
                )
        
        return {
            'warnings': warnings,
            'suggestions': suggestions
        }
    
    async def _analyze_platform_compatibility(self, code: str) -> Dict[str, Any]:
        """Analyze platform-specific compatibility"""
        
        warnings = []
        suggestions = []
        
        # Check for platform-specific includes
        platform_includes = {
            'windows.h': 'Windows-specific',
            'unistd.h': 'Unix-specific',
            'sys/types.h': 'Unix-specific'
        }
        
        for include, platform in platform_includes.items():
            if f'#include <{include}>' in code or f'#include "{include}"' in code:
                warnings.append(
                    f"{platform} header detected ({include}). "
                    "This may not be available on embedded platforms."
                )
                suggestions.append(
                    f"Use platform-abstraction layer instead of {include}."
                )
        
        # Check for standard library functions that may not be available
        embedded_unsafe_functions = [
            'printf', 'scanf', 'malloc', 'free', 'exit', 'system',
            'fopen', 'fclose', 'fprintf', 'fscanf'
        ]
        
        for func in embedded_unsafe_functions:
            pattern = rf'\b{func}\s*\('
            if re.search(pattern, code):
                warnings.append(
                    f"Standard library function '{func}' may not be available "
                    "or suitable for embedded systems."
                )
                suggestions.append(
                    f"Consider embedded-specific alternatives to '{func}'."
                )
        
        return {
            'warnings': warnings,
            'suggestions': suggestions
        }
    
    def _analyze_safety_compliance(self, code: str) -> Dict[str, Any]:
        """Analyze safety and compliance aspects"""
        
        warnings = []
        suggestions = []
        
        # MISRA C compliance checks (basic)
        misra_violations = []
        
        # Check for magic numbers
        magic_number_pattern = r'\b(?<!#define\s)\d{2,}\b'
        matches = re.findall(magic_number_pattern, code)
        if matches:
            misra_violations.append("Magic numbers detected")
            suggestions.append(
                "Replace magic numbers with named constants (#define or const)."
            )
        
        # Check for goto statements
        if re.search(r'\bgoto\b', code):
            misra_violations.append("goto statement detected")
            warnings.append(
                "goto statements violate MISRA C guidelines and should be avoided."
            )
            suggestions.append("Restructure code to eliminate goto statements.")
        
        # Check for proper error handling
        function_pattern = r'(\w+)\s*\([^)]*\)\s*{'
        functions = re.findall(function_pattern, code)
        for func in functions:
            if func not in ['main', 'void']:
                # Check if function has return value checking
                call_pattern = rf'{func}\s*\([^)]*\)\s*;'
                calls = re.findall(call_pattern, code)
                if calls:
                    warnings.append(
                        f"Function '{func}' return value may not be checked. "
                        "Always check return values for error handling."
                    )
                    suggestions.append(
                        f"Add return value checking for '{func}' function calls."
                    )
        
        if misra_violations:
            warnings.append(f"MISRA C violations detected: {', '.join(misra_violations)}")
        
        return {
            'warnings': warnings,
            'suggestions': suggestions
        }
    
    def _generate_explanation(self, analysis_result: AnalysisResult) -> str:
        """Generate human-readable explanation of analysis results"""
        
        if analysis_result.is_valid:
            explanation = "Code analysis completed successfully. "
        else:
            explanation = "Code analysis found potential issues. "
        
        if analysis_result.metrics.get('estimated_stack_usage', 0) > 0:
            stack_usage = analysis_result.metrics['estimated_stack_usage']
            explanation += f"Estimated stack usage: {stack_usage} bytes. "
        
        if analysis_result.metrics.get('dynamic_allocations', 0) > 0:
            allocs = analysis_result.metrics['dynamic_allocations']
            explanation += f"Found {allocs} dynamic memory allocations. "
        
        if len(analysis_result.warnings) > 0:
            explanation += f"Found {len(analysis_result.warnings)} warnings. "
        
        if len(analysis_result.suggestions) > 0:
            explanation += f"Generated {len(analysis_result.suggestions)} improvement suggestions."
        
        return explanation
