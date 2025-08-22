"""
Automotive protocol manager
"""

from typing import Dict, List, Optional, Any
from ai_copilot.config import CopilotConfig


class ProtocolManager:
    """
    Manages automotive communication protocols
    """
    
    def __init__(self, config: CopilotConfig):
        self.config = config
        self.protocols = self._load_protocol_specs()
    
    def _load_protocol_specs(self) -> Dict[str, Dict[str, Any]]:
        """Load protocol specifications"""
        return {
            "CAN": {
                "name": "Controller Area Network",
                "max_data_length": 8,
                "frame_format": "standard_extended",
                "error_detection": ["CRC", "ACK", "form_check"],
                "typical_baudrates": [125000, 250000, 500000, 1000000],
                "compliance_checks": [
                    "message_id_range",
                    "data_length_check",
                    "baudrate_validation"
                ]
            },
            "LIN": {
                "name": "Local Interconnect Network",
                "max_data_length": 8,
                "frame_format": "lin_frame",
                "error_detection": ["checksum"],
                "typical_baudrates": [9600, 19200],
                "compliance_checks": [
                    "master_slave_topology",
                    "schedule_table_compliance"
                ]
            },
            "FlexRay": {
                "name": "FlexRay Communication System",
                "max_data_length": 254,
                "frame_format": "flexray_frame",
                "error_detection": ["CRC", "header_crc"],
                "typical_baudrates": [10000000],
                "compliance_checks": [
                    "static_dynamic_segment",
                    "slot_allocation",
                    "timing_constraints"
                ]
            }
        }
    
    async def check_protocol_compliance(self, code: str, protocol: str) -> Dict[str, Any]:
        """
        Check code compliance with protocol specifications
        
        Args:
            code: Source code to check
            protocol: Protocol name (CAN, LIN, FlexRay, etc.)
            
        Returns:
            Compliance check results
        """
        
        protocol_spec = self.protocols.get(protocol)
        if not protocol_spec:
            return {"error": f"Unknown protocol: {protocol}"}
        
        compliance_results = {
            "protocol": protocol,
            "compliant": True,
            "violations": [],
            "warnings": [],
            "suggestions": []
        }
        
        # Perform protocol-specific checks
        if protocol == "CAN":
            can_results = self._check_can_compliance(code, protocol_spec)
            compliance_results.update(can_results)
        elif protocol == "LIN":
            lin_results = self._check_lin_compliance(code, protocol_spec)
            compliance_results.update(lin_results)
        elif protocol == "FlexRay":
            flexray_results = self._check_flexray_compliance(code, protocol_spec)
            compliance_results.update(flexray_results)
        
        return compliance_results
    
    def _check_can_compliance(self, code: str, spec: Dict[str, Any]) -> Dict[str, Any]:
        """Check CAN protocol compliance"""
        violations = []
        warnings = []
        suggestions = []
        
        # Check for proper data length validation
        if "dlc" in code.lower():
            if "dlc > 8" not in code and "dlc <= 8" not in code:
                violations.append("Missing DLC validation (should check dlc <= 8)")
                suggestions.append("Add DLC validation: if (dlc > 8) return error;")
        
        # Check for message ID validation
        if "id" in code.lower() and "can" in code.lower():
            if "0x7FF" not in code and "2047" not in code:
                warnings.append("Consider validating CAN ID range (0-0x7FF for standard)")
                suggestions.append("Add ID validation for standard CAN frames")
        
        return {
            "violations": violations,
            "warnings": warnings,
            "suggestions": suggestions,
            "compliant": len(violations) == 0
        }
    
    def _check_lin_compliance(self, code: str, spec: Dict[str, Any]) -> Dict[str, Any]:
        """Check LIN protocol compliance"""
        violations = []
        warnings = []
        suggestions = []
        
        # Check for master/slave architecture
        if "lin" in code.lower():
            if "master" not in code.lower() and "slave" not in code.lower():
                warnings.append("LIN master/slave role not clearly defined")
                suggestions.append("Clearly define LIN master or slave role")
        
        return {
            "violations": violations,
            "warnings": warnings,
            "suggestions": suggestions,
            "compliant": len(violations) == 0
        }
    
    def _check_flexray_compliance(self, code: str, spec: Dict[str, Any]) -> Dict[str, Any]:
        """Check FlexRay protocol compliance"""
        violations = []
        warnings = []
        suggestions = []
        
        # Check for slot allocation
        if "flexray" in code.lower():
            if "slot" not in code.lower():
                warnings.append("FlexRay slot allocation not evident")
                suggestions.append("Ensure proper FlexRay slot allocation")
        
        return {
            "violations": violations,
            "warnings": warnings,
            "suggestions": suggestions,
            "compliant": len(violations) == 0
        }
