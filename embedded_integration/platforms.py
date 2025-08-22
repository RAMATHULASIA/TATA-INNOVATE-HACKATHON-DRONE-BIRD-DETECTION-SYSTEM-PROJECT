"""
Platform manager for different embedded architectures
"""

from typing import Dict, List, Optional, Any
from ai_copilot.config import CopilotConfig


class PlatformManager:
    """
    Manages platform-specific information and optimizations
    """
    
    def __init__(self, config: CopilotConfig):
        self.config = config
        self.platforms = self._load_platform_info()
    
    def _load_platform_info(self) -> Dict[str, Dict[str, Any]]:
        """Load platform-specific information"""
        return {
            "ARM Cortex-M": {
                "architecture": "ARM",
                "word_size": 32,
                "endianness": "little",
                "has_fpu": False,
                "memory_model": "harvard",
                "typical_flash": "512KB",
                "typical_ram": "64KB",
                "compiler_flags": ["-mcpu=cortex-m4", "-mthumb"],
                "optimization_hints": [
                    "Use thumb instructions",
                    "Minimize stack usage",
                    "Avoid floating point if no FPU"
                ]
            },
            "AVR": {
                "architecture": "AVR",
                "word_size": 8,
                "endianness": "little",
                "has_fpu": False,
                "memory_model": "harvard",
                "typical_flash": "32KB",
                "typical_ram": "2KB",
                "compiler_flags": ["-mmcu=atmega328p"],
                "optimization_hints": [
                    "Use 8-bit data types when possible",
                    "Minimize RAM usage",
                    "Use PROGMEM for constants"
                ]
            },
            "x86": {
                "architecture": "x86",
                "word_size": 32,
                "endianness": "little",
                "has_fpu": True,
                "memory_model": "von_neumann",
                "typical_flash": "unlimited",
                "typical_ram": "unlimited",
                "compiler_flags": ["-m32"],
                "optimization_hints": [
                    "Can use standard library",
                    "Floating point operations available",
                    "Memory constraints less critical"
                ]
            }
        }
    
    def get_platform_info(self, platform_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific platform"""
        return self.platforms.get(platform_name)
    
    def get_optimization_hints(self, platform_name: str) -> List[str]:
        """Get optimization hints for a platform"""
        platform_info = self.get_platform_info(platform_name)
        if platform_info:
            return platform_info.get("optimization_hints", [])
        return []
    
    def get_compiler_flags(self, platform_name: str) -> List[str]:
        """Get recommended compiler flags for a platform"""
        platform_info = self.get_platform_info(platform_name)
        if platform_info:
            return platform_info.get("compiler_flags", [])
        return []
    
    def is_platform_suitable(self, platform_name: str, requirements: Dict[str, Any]) -> bool:
        """Check if a platform meets the requirements"""
        platform_info = self.get_platform_info(platform_name)
        if not platform_info:
            return False
        
        # Check memory requirements
        if "min_ram" in requirements:
            # This would need proper parsing of memory sizes
            # For now, just a basic check
            pass
        
        # Check FPU requirements
        if requirements.get("requires_fpu", False):
            if not platform_info.get("has_fpu", False):
                return False
        
        return True
