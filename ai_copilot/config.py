"""
Configuration management for AI Co-pilot
"""

import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from pathlib import Path
import yaml
from pydantic import BaseModel, Field


class ModelConfig(BaseModel):
    """Configuration for AI models"""
    name: str = "microsoft/DialoGPT-medium"
    max_length: int = 512
    temperature: float = 0.7
    top_p: float = 0.9
    device: str = "auto"
    cache_dir: Optional[str] = None


class EmbeddedConfig(BaseModel):
    """Configuration for embedded systems integration"""
    target_architectures: List[str] = ["ARM Cortex-M", "AVR", "x86", "RISC-V"]
    supported_protocols: List[str] = ["CAN", "LIN", "FlexRay", "Ethernet"]
    memory_constraints: Dict[str, int] = {
        "flash_kb": 512,
        "ram_kb": 64,
        "stack_kb": 8
    }
    real_time_requirements: bool = True
    safety_level: str = "ASIL-B"  # ISO 26262 levels: QM, ASIL-A, ASIL-B, ASIL-C, ASIL-D


class VehicleConfig(BaseModel):
    """Configuration for vehicle-specific features"""
    vehicle_type: str = "passenger_car"  # passenger_car, commercial, motorcycle
    ecu_types: List[str] = ["engine", "transmission", "brake", "steering", "infotainment"]
    communication_protocols: List[str] = ["CAN-FD", "LIN", "FlexRay"]
    autosar_version: str = "4.4"
    compliance_standards: List[str] = ["ISO 26262", "ISO 14229", "ISO 15765"]


class CopilotConfig(BaseModel):
    """Main configuration class for AI Co-pilot"""
    
    # Model configuration
    model: ModelConfig = Field(default_factory=ModelConfig)
    
    # Embedded systems configuration
    embedded: EmbeddedConfig = Field(default_factory=EmbeddedConfig)
    
    # Vehicle-specific configuration
    vehicle: VehicleConfig = Field(default_factory=VehicleConfig)
    
    # General settings
    debug: bool = False
    log_level: str = "INFO"
    output_dir: str = "./output"
    cache_enabled: bool = True
    
    # Code generation settings
    code_style: str = "automotive"  # automotive, embedded, general
    include_comments: bool = True
    generate_tests: bool = True
    validate_syntax: bool = True
    
    @classmethod
    def from_file(cls, config_path: str) -> "CopilotConfig":
        """Load configuration from YAML file"""
        with open(config_path, 'r') as f:
            config_data = yaml.safe_load(f)
        return cls(**config_data)
    
    def to_file(self, config_path: str) -> None:
        """Save configuration to YAML file"""
        with open(config_path, 'w') as f:
            yaml.dump(self.dict(), f, default_flow_style=False)
    
    @classmethod
    def get_default_config_path(cls) -> Path:
        """Get default configuration file path"""
        return Path.home() / ".ai_copilot" / "config.yaml"
    
    def setup_directories(self) -> None:
        """Create necessary directories"""
        os.makedirs(self.output_dir, exist_ok=True)
        if self.model.cache_dir:
            os.makedirs(self.model.cache_dir, exist_ok=True)


# Default configuration instance
default_config = CopilotConfig()
