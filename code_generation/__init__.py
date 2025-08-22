"""
Code Generation Module

This module handles AI-powered code generation for embedded systems,
with specific focus on automotive and real-time constraints.
"""

from .generator import CodeGenerator
from .templates import TemplateManager
from .validators import CodeValidator

__all__ = ["CodeGenerator", "TemplateManager", "CodeValidator"]
