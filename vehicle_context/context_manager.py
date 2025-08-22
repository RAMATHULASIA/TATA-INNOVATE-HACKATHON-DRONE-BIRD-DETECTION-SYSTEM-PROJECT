"""
Vehicle Context Manager

Manages automotive domain knowledge and provides context-aware
information for code generation and analysis.
"""

import json
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
from dataclasses import dataclass

from ai_copilot.config import CopilotConfig
from .protocols import ProtocolManager
from .standards import StandardsChecker


@dataclass
class VehicleContext:
    """Vehicle context information"""
    ecu_type: str
    protocols: List[str]
    safety_level: str
    real_time_requirements: bool
    memory_constraints: Dict[str, int]
    communication_matrix: Dict[str, List[str]]


class VehicleContextManager:
    """
    Manages vehicle-specific context and domain knowledge
    """
    
    def __init__(self, config: CopilotConfig):
        self.config = config
        self.protocol_manager = ProtocolManager(config)
        self.standards_checker = StandardsChecker(config)
        
        # Load vehicle domain knowledge
        self.ecu_knowledge = self._load_ecu_knowledge()
        self.protocol_knowledge = self._load_protocol_knowledge()
        self.automotive_patterns = self._load_automotive_patterns()
    
    def _load_ecu_knowledge(self) -> Dict[str, Any]:
        """Load ECU-specific knowledge base"""
        return {
            "engine": {
                "description": "Engine Control Unit",
                "typical_protocols": ["CAN", "CAN-FD"],
                "safety_level": "ASIL-D",
                "real_time": True,
                "typical_functions": [
                    "fuel_injection_control",
                    "ignition_timing",
                    "emission_control",
                    "engine_diagnostics"
                ],
                "memory_requirements": {
                    "flash_kb": 2048,
                    "ram_kb": 256,
                    "eeprom_kb": 64
                }
            },
            "transmission": {
                "description": "Transmission Control Unit",
                "typical_protocols": ["CAN", "LIN"],
                "safety_level": "ASIL-C",
                "real_time": True,
                "typical_functions": [
                    "gear_shift_control",
                    "torque_management",
                    "transmission_diagnostics"
                ],
                "memory_requirements": {
                    "flash_kb": 1024,
                    "ram_kb": 128,
                    "eeprom_kb": 32
                }
            },
            "brake": {
                "description": "Brake Control Unit",
                "typical_protocols": ["CAN", "FlexRay"],
                "safety_level": "ASIL-D",
                "real_time": True,
                "typical_functions": [
                    "abs_control",
                    "esp_control",
                    "brake_assist",
                    "brake_diagnostics"
                ],
                "memory_requirements": {
                    "flash_kb": 1536,
                    "ram_kb": 192,
                    "eeprom_kb": 48
                }
            },
            "infotainment": {
                "description": "Infotainment Control Unit",
                "typical_protocols": ["CAN", "Ethernet", "MOST"],
                "safety_level": "QM",
                "real_time": False,
                "typical_functions": [
                    "media_playback",
                    "navigation",
                    "connectivity",
                    "user_interface"
                ],
                "memory_requirements": {
                    "flash_kb": 8192,
                    "ram_kb": 1024,
                    "eeprom_kb": 128
                }
            }
        }
    
    def _load_protocol_knowledge(self) -> Dict[str, Any]:
        """Load automotive protocol knowledge"""
        return {
            "CAN": {
                "description": "Controller Area Network",
                "max_data_length": 8,
                "typical_baudrates": [125000, 250000, 500000, 1000000],
                "frame_types": ["data", "remote", "error", "overload"],
                "error_detection": ["CRC", "ACK", "form_check", "bit_monitoring"],
                "typical_usage": ["powertrain", "chassis", "body"]
            },
            "CAN-FD": {
                "description": "CAN with Flexible Data-Rate",
                "max_data_length": 64,
                "typical_baudrates": [500000, 1000000, 2000000, 5000000],
                "features": ["flexible_data_rate", "extended_payload", "improved_crc"],
                "typical_usage": ["high_bandwidth_applications", "gateway_communication"]
            },
            "LIN": {
                "description": "Local Interconnect Network",
                "max_data_length": 8,
                "typical_baudrates": [9600, 19200],
                "topology": "single_master_multiple_slave",
                "typical_usage": ["body_electronics", "comfort_functions"]
            },
            "FlexRay": {
                "description": "FlexRay Communication System",
                "max_data_length": 254,
                "typical_baudrates": [10000000],
                "features": ["time_triggered", "fault_tolerant", "dual_channel"],
                "typical_usage": ["safety_critical", "x_by_wire", "advanced_chassis"]
            }
        }
    
    def _load_automotive_patterns(self) -> Dict[str, Any]:
        """Load common automotive software patterns"""
        return {
            "initialization_patterns": [
                "hardware_init",
                "peripheral_config",
                "interrupt_setup",
                "watchdog_init"
            ],
            "communication_patterns": [
                "message_transmission",
                "message_reception",
                "protocol_stack",
                "diagnostic_communication"
            ],
            "safety_patterns": [
                "error_detection",
                "error_handling",
                "redundancy",
                "fail_safe_behavior"
            ],
            "real_time_patterns": [
                "cyclic_tasks",
                "interrupt_handling",
                "priority_scheduling",
                "deadline_monitoring"
            ]
        }
    
    async def analyze_context(self, description: str, target_platform: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze the context of a code generation request
        
        Args:
            description: Description of the requested functionality
            target_platform: Target platform/ECU type
            
        Returns:
            Context information for code generation
        """
        
        context = {
            "ecu_type": self._identify_ecu_type(description, target_platform),
            "protocols": self._identify_protocols(description),
            "functions": self._identify_functions(description),
            "patterns": self._identify_patterns(description),
            "constraints": self._get_constraints(description, target_platform)
        }
        
        # Enrich context with ECU-specific knowledge
        if context["ecu_type"] in self.ecu_knowledge:
            ecu_info = self.ecu_knowledge[context["ecu_type"]]
            context.update({
                "safety_level": ecu_info["safety_level"],
                "real_time": ecu_info["real_time"],
                "memory_requirements": ecu_info["memory_requirements"],
                "typical_protocols": ecu_info["typical_protocols"]
            })
        
        return context
    
    def _identify_ecu_type(self, description: str, target_platform: Optional[str] = None) -> str:
        """Identify the ECU type from description"""
        
        if target_platform:
            target_lower = target_platform.lower()
            for ecu_type in self.ecu_knowledge.keys():
                if ecu_type in target_lower:
                    return ecu_type
        
        description_lower = description.lower()
        
        # Check for ECU-specific keywords
        ecu_keywords = {
            "engine": ["engine", "fuel", "ignition", "emission", "combustion"],
            "transmission": ["transmission", "gear", "shift", "torque", "clutch"],
            "brake": ["brake", "abs", "esp", "stability", "traction"],
            "infotainment": ["infotainment", "media", "navigation", "display", "audio"]
        }
        
        for ecu_type, keywords in ecu_keywords.items():
            if any(keyword in description_lower for keyword in keywords):
                return ecu_type
        
        return "generic"
    
    def _identify_protocols(self, description: str) -> List[str]:
        """Identify communication protocols from description"""
        
        protocols = []
        description_lower = description.lower()
        
        protocol_keywords = {
            "CAN": ["can", "controller area network"],
            "CAN-FD": ["can-fd", "can fd", "flexible data"],
            "LIN": ["lin", "local interconnect"],
            "FlexRay": ["flexray", "flex ray"],
            "Ethernet": ["ethernet", "tcp", "udp"]
        }
        
        for protocol, keywords in protocol_keywords.items():
            if any(keyword in description_lower for keyword in keywords):
                protocols.append(protocol)
        
        return protocols
    
    def _identify_functions(self, description: str) -> List[str]:
        """Identify automotive functions from description"""
        
        functions = []
        description_lower = description.lower()
        
        function_keywords = {
            "diagnostics": ["diagnostic", "dtc", "trouble code", "obd"],
            "communication": ["send", "receive", "transmit", "message"],
            "control": ["control", "regulate", "manage", "adjust"],
            "monitoring": ["monitor", "check", "watch", "observe"],
            "safety": ["safety", "fail", "error", "fault"]
        }
        
        for function, keywords in function_keywords.items():
            if any(keyword in description_lower for keyword in keywords):
                functions.append(function)
        
        return functions
    
    def _identify_patterns(self, description: str) -> List[str]:
        """Identify applicable automotive patterns"""
        
        patterns = []
        description_lower = description.lower()
        
        # Check for pattern indicators
        if any(word in description_lower for word in ["init", "initialize", "setup"]):
            patterns.append("initialization")
        
        if any(word in description_lower for word in ["send", "receive", "communicate"]):
            patterns.append("communication")
        
        if any(word in description_lower for word in ["error", "fault", "safety"]):
            patterns.append("safety")
        
        if any(word in description_lower for word in ["cyclic", "periodic", "real-time"]):
            patterns.append("real_time")
        
        return patterns
    
    def _get_constraints(self, description: str, target_platform: Optional[str] = None) -> Dict[str, Any]:
        """Get applicable constraints for the context"""
        
        constraints = {
            "memory_constraints": self.config.embedded.memory_constraints.copy(),
            "real_time": self.config.embedded.real_time_requirements,
            "safety_level": self.config.embedded.safety_level
        }
        
        # Adjust constraints based on identified ECU type
        ecu_type = self._identify_ecu_type(description, target_platform)
        if ecu_type in self.ecu_knowledge:
            ecu_info = self.ecu_knowledge[ecu_type]
            constraints.update({
                "memory_constraints": ecu_info["memory_requirements"],
                "real_time": ecu_info["real_time"],
                "safety_level": ecu_info["safety_level"]
            })
        
        return constraints
    
    async def analyze_code_compliance(self, code: str) -> Dict[str, Any]:
        """
        Analyze code for automotive compliance
        
        Args:
            code: Source code to analyze
            
        Returns:
            Compliance analysis results
        """
        
        compliance_results = {
            "autosar_compliance": [],
            "iso26262_compliance": [],
            "protocol_compliance": [],
            "warnings": [],
            "suggestions": []
        }
        
        # Check AUTOSAR compliance
        autosar_results = await self.standards_checker.check_autosar_compliance(code)
        compliance_results["autosar_compliance"] = autosar_results
        
        # Check ISO 26262 compliance
        iso26262_results = await self.standards_checker.check_iso26262_compliance(code)
        compliance_results["iso26262_compliance"] = iso26262_results
        
        # Check protocol-specific compliance
        protocols = self._identify_protocols(code)
        for protocol in protocols:
            protocol_results = await self.protocol_manager.check_protocol_compliance(code, protocol)
            compliance_results["protocol_compliance"].append({
                "protocol": protocol,
                "results": protocol_results
            })
        
        return compliance_results
