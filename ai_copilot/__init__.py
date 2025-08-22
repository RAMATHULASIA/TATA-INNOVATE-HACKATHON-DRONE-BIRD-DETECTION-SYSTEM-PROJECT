"""
AI Co-pilot for Embedded Software Design

This package provides a generative AI system specifically designed for
embedded software development in smart vehicles.
"""

__version__ = "0.1.0"
__author__ = "TATA Project Team"
__email__ = "team@tata-project.com"

from .core import AICopilot
from .config import CopilotConfig

__all__ = ["AICopilot", "CopilotConfig"]
