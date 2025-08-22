"""
Embedded Systems Integration Module

This module provides interfaces and analyzers for embedded systems,
including memory analysis, real-time constraints, and platform-specific optimizations.
"""

from .analyzer import EmbeddedAnalyzer
from .platforms import PlatformManager
from .constraints import ConstraintChecker

__all__ = ["EmbeddedAnalyzer", "PlatformManager", "ConstraintChecker"]
