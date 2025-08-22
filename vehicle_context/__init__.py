"""
Vehicle Context Module

This module provides automotive domain knowledge, protocol implementations,
and vehicle-specific context understanding for the AI co-pilot.
"""

from .context_manager import VehicleContextManager
from .protocols import ProtocolManager
from .standards import StandardsChecker

__all__ = ["VehicleContextManager", "ProtocolManager", "StandardsChecker"]
