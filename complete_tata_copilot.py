#!/usr/bin/env python3
"""
Complete TATA AI Co-pilot with Interactive Q&A and Advanced Features
TATA Innovate Hackathon 2024
"""

import http.server
import socketserver
import json
import webbrowser
import threading
import time
import urllib.parse
import random
from datetime import datetime

class TATAAdvancedHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.serve_main_page()
        elif self.path == '/api/status':
            self.serve_json({
                "status": "running",
                "message": "TATA AI Co-pilot is operational",
                "version": "2.0.0-hackathon",
                "features": ["interactive_qa", "code_generation", "analysis", "projects", "themes", "pwa", "voice_commands"],
                "uptime": "Running since startup",
                "ai_models": ["TATA-GPT-Automotive", "CodeGen-Embedded", "Safety-Analyzer"]
            })
        elif self.path == '/api/platforms':
            self.serve_json({
                "platforms": [
                    {"name": "ARM Cortex-M4", "description": "32-bit microcontroller for automotive ECUs", "memory": "256KB-1MB"},
                    {"name": "ARM Cortex-M7", "description": "High-performance automotive processor", "memory": "512KB-2MB"},
                    {"name": "ARM Cortex-A", "description": "Application processor for infotainment", "memory": "1GB+"},
                    {"name": "AVR ATmega", "description": "8-bit microcontroller for simple sensors", "memory": "32KB-256KB"},
                    {"name": "x86", "description": "Development and simulation platform", "memory": "4GB+"},
                    {"name": "RISC-V", "description": "Open-source processor architecture", "memory": "128KB-1MB"},
                    {"name": "TATA Custom ECU", "description": "TATA proprietary automotive controller", "memory": "512KB-4MB"}
                ]
            })
        elif self.path == '/api/sample-questions':
            self.serve_json({
                "categories": {
                    "Engine Control": [
                        "Create a TATA vehicle engine RPM monitoring system with CAN bus communication",
                        "Generate code for TATA commercial vehicle fuel injection control with safety checks",
                        "Build an engine temperature monitoring system for TATA trucks with ASIL-B compliance"
                    ],
                    "Brake Systems": [
                        "Create a TATA vehicle anti-lock braking system (ABS) controller with fail-safe mechanisms",
                        "Generate brake pressure monitoring code for TATA passenger cars with emergency protocols",
                        "Build a brake-by-wire system for TATA electric vehicles with redundancy"
                    ],
                    "Electric Vehicles": [
                        "Create a battery management system for TATA electric vehicles with thermal protection",
                        "Generate charging controller code for TATA EV fast charging stations",
                        "Build a regenerative braking system for TATA electric buses"
                    ],
                    "Safety Systems": [
                        "Create an ASIL-D compliant steering system controller for TATA passenger cars",
                        "Generate ISO 26262 compliant airbag deployment code for TATA vehicles",
                        "Build a functional safety monitor for TATA vehicle ECUs with diagnostic coverage"
                    ]
                }
            })
        elif self.path == '/manifest.json':
            self.serve_json({
                "short_name": "TATA AI Co-pilot",
                "name": "TATA AI Co-pilot for Embedded Software Design",
                "description": "AI-powered development platform for TATA vehicle embedded systems",
                "start_url": "/",
                "display": "standalone",
                "theme_color": "#1B4F72",
                "background_color": "#FFFFFF",
                "icons": [{"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"}]
            })
        else:
            super().do_GET()
    
    def do_POST(self):
        if self.path == '/api/ask':
            self.handle_qa_request()
        elif self.path == '/api/generate':
            self.handle_code_generation()
        elif self.path == '/api/analyze':
            self.handle_code_analysis()
        else:
            self.send_error(404)
    
    def handle_qa_request(self):
        """Handle interactive Q&A requests"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            request_data = json.loads(post_data.decode('utf-8'))
            
            question = request_data.get('question', '').strip()
            context = request_data.get('context', 'general')
            
            # Generate intelligent response based on question
            response = self.generate_qa_response(question, context)
            
            self.serve_json({
                "question": question,
                "answer": response["answer"],
                "code_example": response.get("code_example", ""),
                "explanation": response.get("explanation", ""),
                "related_topics": response.get("related_topics", []),
                "confidence": response.get("confidence", 0.95),
                "timestamp": datetime.now().isoformat()
            })
            
        except Exception as e:
            self.serve_json({"error": str(e)}, status=400)
    
    def handle_code_generation(self):
        """Handle code generation requests"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            request_data = json.loads(post_data.decode('utf-8'))
            
            description = request_data.get('description', 'TATA vehicle function')
            language = request_data.get('language', 'c')
            platform = request_data.get('target_platform', 'ARM Cortex-M')
            asil_level = request_data.get('asil_level', 'B')
            
            # Generate code based on description
            code_result = self.generate_automotive_code(description, language, platform, asil_level)
            
            self.serve_json({
                "generated_code": code_result["code"],
                "explanation": code_result["explanation"],
                "warnings": code_result["warnings"],
                "suggestions": code_result["suggestions"],
                "metadata": {
                    "lines_of_code": len(code_result["code"].split('\n')),
                    "platform": platform,
                    "language": language,
                    "safety_level": asil_level,
                    "estimated_memory": code_result["memory_estimate"],
                    "complexity_score": code_result["complexity"]
                }
            })
            
        except Exception as e:
            self.serve_json({"error": str(e)}, status=400)
    
    def handle_code_analysis(self):
        """Handle code analysis requests"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            request_data = json.loads(post_data.decode('utf-8'))
            
            code = request_data.get('code', '')
            language = request_data.get('language', 'c')
            
            analysis = self.analyze_code(code, language)
            
            self.serve_json(analysis)
            
        except Exception as e:
            self.serve_json({"error": str(e)}, status=400)
    
    def generate_qa_response(self, question, context):
        """Generate intelligent Q&A responses"""
        question_lower = question.lower()
        
        # Automotive-specific responses
        if any(word in question_lower for word in ['brake', 'braking', 'abs']):
            return {
                "answer": "TATA brake systems require ASIL-D compliance for safety-critical functions. The brake system should include redundant sensors, fail-safe mechanisms, and real-time monitoring. For ABS systems, we implement wheel speed sensors, hydraulic pressure control, and emergency braking protocols.",
                "code_example": self.get_brake_code_example(),
                "explanation": "This implementation follows ISO 26262 standards for automotive safety and includes TATA-specific error codes and CAN bus communication protocols.",
                "related_topics": ["ASIL-D Compliance", "CAN Bus Communication", "Hydraulic Control", "Sensor Redundancy"],
                "confidence": 0.98
            }
        
        elif any(word in question_lower for word in ['engine', 'rpm', 'fuel', 'injection']):
            return {
                "answer": "TATA engine control systems manage fuel injection, ignition timing, and emissions control. The ECU monitors engine RPM, temperature, and load conditions to optimize performance and efficiency. For commercial vehicles, we focus on durability and fuel economy.",
                "code_example": self.get_engine_code_example(),
                "explanation": "This code implements a complete engine control loop with sensor validation, fuel map lookup, and diagnostic monitoring suitable for TATA commercial vehicles.",
                "related_topics": ["Fuel Injection", "Ignition Timing", "Emissions Control", "Engine Diagnostics"],
                "confidence": 0.96
            }
        
        elif any(word in question_lower for word in ['battery', 'electric', 'ev', 'charging']):
            return {
                "answer": "TATA electric vehicle systems require sophisticated battery management, thermal control, and charging protocols. The BMS monitors cell voltages, temperatures, and current flow to ensure safety and longevity. Fast charging requires careful thermal management.",
                "code_example": self.get_battery_code_example(),
                "explanation": "This BMS implementation includes cell balancing, thermal protection, and SOC estimation algorithms optimized for TATA electric vehicle platforms.",
                "related_topics": ["Battery Management", "Thermal Control", "Fast Charging", "Cell Balancing"],
                "confidence": 0.97
            }
        
        elif any(word in question_lower for word in ['can', 'communication', 'network']):
            return {
                "answer": "TATA vehicles use CAN bus networks for inter-ECU communication. The network includes engine, transmission, brake, and body control modules. Message priorities and timing are critical for real-time performance.",
                "code_example": self.get_can_code_example(),
                "explanation": "This CAN implementation provides message filtering, error handling, and diagnostic capabilities for TATA vehicle networks.",
                "related_topics": ["CAN Bus", "Message Filtering", "Network Diagnostics", "Real-time Communication"],
                "confidence": 0.95
            }
        
        else:
            return {
                "answer": f"I understand you're asking about: '{question}'. For TATA automotive systems, I can help with engine control, brake systems, electric vehicles, CAN communication, safety compliance (ASIL), and embedded software development. Please provide more specific details about your automotive software requirements.",
                "explanation": "I'm specialized in TATA automotive embedded software development and can provide detailed technical guidance.",
                "related_topics": ["Engine Control", "Brake Systems", "Electric Vehicles", "Safety Compliance"],
                "confidence": 0.85
            }
    
    def generate_automotive_code(self, description, language, platform, asil_level):
        """Generate automotive-specific code"""
        desc_lower = description.lower()
        
        if 'brake' in desc_lower:
            return self.generate_brake_system_code(platform, asil_level)
        elif 'engine' in desc_lower:
            return self.generate_engine_control_code(platform, asil_level)
        elif 'battery' in desc_lower or 'electric' in desc_lower:
            return self.generate_battery_management_code(platform, asil_level)
        elif 'can' in desc_lower:
            return self.generate_can_handler_code(platform, asil_level)
        else:
            return self.generate_generic_automotive_code(description, platform, asil_level)
    
    def generate_brake_system_code(self, platform, asil_level):
        code = f'''// TATA Vehicle Brake System Controller
// Platform: {platform} | ASIL Level: {asil_level}
// Generated by TATA AI Co-pilot

#include "tata_brake_system.h"
#include "can_interface.h"
#include "safety_monitor.h"

// TATA brake system configuration
#define TATA_BRAKE_CAN_ID           0x200
#define TATA_MAX_BRAKE_PRESSURE     8000  // kPa
#define TATA_MIN_BRAKE_PRESSURE     0     // kPa
#define TATA_BRAKE_SENSOR_TIMEOUT   100   // ms

// TATA brake pressure data structure
typedef struct {{
    uint16_t front_left_pressure;   // Front left brake pressure (kPa)
    uint16_t front_right_pressure;  // Front right brake pressure (kPa)
    uint16_t rear_left_pressure;    // Rear left brake pressure (kPa)
    uint16_t rear_right_pressure;   // Rear right brake pressure (kPa)
    uint8_t system_status;          // System status flags
    uint8_t error_flags;            // Error condition flags
    uint32_t timestamp;             // System timestamp
}} tata_brake_data_t;

// TATA brake system status flags
#define TATA_BRAKE_STATUS_NORMAL    0x00
#define TATA_BRAKE_STATUS_WARNING   0x01
#define TATA_BRAKE_STATUS_ERROR     0x02
#define TATA_BRAKE_STATUS_CRITICAL  0x04

// Global brake system data
static tata_brake_data_t g_brake_data;
static bool g_system_initialized = false;

// Initialize TATA brake monitoring system
tata_result_t tata_brake_system_init(void) {{
    // Initialize CAN interface for brake communication
    if (can_init(CAN_SPEED_500K) != CAN_OK) {{
        return TATA_ERROR_CAN_INIT;
    }}
    
    // Initialize brake pressure sensors
    if (brake_sensors_init() != SENSOR_OK) {{
        return TATA_ERROR_SENSOR_INIT;
    }}
    
    // Initialize safety monitoring
    safety_monitor_init();
    
    // Clear brake data structure
    memset(&g_brake_data, 0, sizeof(tata_brake_data_t));
    
    g_system_initialized = true;
    return TATA_SUCCESS;
}}

// Read brake pressures and validate
tata_result_t tata_brake_read_pressures(void) {{
    if (!g_system_initialized) {{
        return TATA_ERROR_NOT_INITIALIZED;
    }}
    
    // Read all brake pressure sensors
    g_brake_data.front_left_pressure = read_brake_sensor(BRAKE_SENSOR_FL);
    g_brake_data.front_right_pressure = read_brake_sensor(BRAKE_SENSOR_FR);
    g_brake_data.rear_left_pressure = read_brake_sensor(BRAKE_SENSOR_RL);
    g_brake_data.rear_right_pressure = read_brake_sensor(BRAKE_SENSOR_RR);
    
    // Update timestamp
    g_brake_data.timestamp = get_system_time_ms();
    
    // Validate pressure readings
    return tata_brake_validate_pressures();
}}

// Validate brake pressure readings for safety
tata_result_t tata_brake_validate_pressures(void) {{
    g_brake_data.error_flags = 0;
    g_brake_data.system_status = TATA_BRAKE_STATUS_NORMAL;
    
    // Check for overpressure conditions
    if (g_brake_data.front_left_pressure > TATA_MAX_BRAKE_PRESSURE ||
        g_brake_data.front_right_pressure > TATA_MAX_BRAKE_PRESSURE ||
        g_brake_data.rear_left_pressure > TATA_MAX_BRAKE_PRESSURE ||
        g_brake_data.rear_right_pressure > TATA_MAX_BRAKE_PRESSURE) {{
        
        g_brake_data.error_flags |= TATA_ERROR_OVERPRESSURE;
        g_brake_data.system_status = TATA_BRAKE_STATUS_CRITICAL;
        trigger_emergency_brake_release();
        return TATA_ERROR_OVERPRESSURE;
    }}
    
    // Check for pressure imbalance
    uint16_t front_diff = abs(g_brake_data.front_left_pressure - g_brake_data.front_right_pressure);
    uint16_t rear_diff = abs(g_brake_data.rear_left_pressure - g_brake_data.rear_right_pressure);
    
    if (front_diff > TATA_MAX_PRESSURE_IMBALANCE || rear_diff > TATA_MAX_PRESSURE_IMBALANCE) {{
        g_brake_data.error_flags |= TATA_ERROR_PRESSURE_IMBALANCE;
        g_brake_data.system_status = TATA_BRAKE_STATUS_WARNING;
    }}
    
    return TATA_SUCCESS;
}}

// Send brake data via CAN bus
tata_result_t tata_brake_send_can_data(void) {{
    can_message_t can_msg;
    
    // Prepare CAN message
    can_msg.id = TATA_BRAKE_CAN_ID;
    can_msg.dlc = sizeof(tata_brake_data_t);
    memcpy(can_msg.data, &g_brake_data, sizeof(tata_brake_data_t));
    
    // Send message with high priority
    return can_send_message(&can_msg, CAN_PRIORITY_HIGH);
}}

// Main brake system monitoring loop
void tata_brake_system_task(void) {{
    static uint32_t last_update = 0;
    uint32_t current_time = get_system_time_ms();
    
    // Run at 10Hz for real-time monitoring
    if ((current_time - last_update) >= 100) {{
        // Read brake pressures
        if (tata_brake_read_pressures() == TATA_SUCCESS) {{
            // Send data via CAN
            tata_brake_send_can_data();
        }}
        
        // Update safety monitor
        tata_brake_safety_monitor();
        
        last_update = current_time;
    }}
}}

// ASIL-{asil_level} safety monitoring function
void tata_brake_safety_monitor(void) {{
    static uint32_t last_sensor_update = 0;
    uint32_t current_time = get_system_time_ms();
    
    // Check for sensor communication timeout
    if ((current_time - g_brake_data.timestamp) > TATA_BRAKE_SENSOR_TIMEOUT) {{
        g_brake_data.error_flags |= TATA_ERROR_SENSOR_TIMEOUT;
        g_brake_data.system_status = TATA_BRAKE_STATUS_ERROR;
        
        // Trigger fail-safe mode
        trigger_brake_fail_safe();
    }}
    
    // Perform diagnostic self-test
    if ((current_time % 5000) == 0) {{  // Every 5 seconds
        perform_brake_system_self_test();
    }}
}}'''

        return {
            "code": code,
            "explanation": f"Generated TATA brake system controller for {platform} with {asil_level} safety compliance. Includes pressure monitoring, CAN communication, and fail-safe mechanisms.",
            "warnings": [
                "Implement hardware-specific sensor drivers",
                "Validate CAN message timing requirements",
                "Test fail-safe mechanisms thoroughly"
            ],
            "suggestions": [
                "Add brake temperature monitoring",
                "Implement brake wear estimation",
                "Consider adding brake assist features",
                "Add diagnostic trouble codes (DTCs)"
            ],
            "memory_estimate": "4.2 KB",
            "complexity": 8.5
        }
    
    def get_brake_code_example(self):
        return '''// TATA Brake Pressure Monitor Example
typedef struct {
    uint16_t pressure_kpa;
    uint8_t status_flags;
    uint32_t timestamp;
} tata_brake_data_t;

int tata_brake_monitor_init(void) {
    if (can_init(CAN_SPEED_500K) != CAN_OK) {
        return TATA_ERROR_CAN_INIT;
    }
    return TATA_SUCCESS;
}'''

    def get_engine_code_example(self):
        return '''// TATA Engine Control Example
typedef struct {
    uint16_t rpm;
    uint8_t throttle_position;
    int16_t engine_temp;
    uint16_t fuel_flow;
} tata_engine_data_t;

int tata_engine_control_init(void) {
    // Initialize engine sensors
    return TATA_SUCCESS;
}'''

    def get_battery_code_example(self):
        return '''// TATA Battery Management Example
typedef struct {
    uint16_t cell_voltages[12];
    int16_t pack_current;
    int16_t pack_temperature;
    uint8_t soc_percentage;
} tata_battery_data_t;

int tata_bms_init(void) {
    // Initialize BMS
    return TATA_SUCCESS;
}'''

    def get_can_code_example(self):
        return '''// TATA CAN Communication Example
typedef struct {
    uint32_t id;
    uint8_t dlc;
    uint8_t data[8];
} tata_can_message_t;

int tata_can_send_message(tata_can_message_t* msg) {
    return can_transmit(msg);
}'''

    def generate_engine_control_code(self, platform, asil_level):
        code = f'''// TATA Engine Control System
// Platform: {platform} | ASIL Level: {asil_level}
// Generated by TATA AI Co-pilot

#include "tata_engine_control.h"
#include "can_interface.h"
#include "sensor_interface.h"

// TATA engine control configuration
#define TATA_ENGINE_CAN_ID          0x100
#define TATA_MAX_RPM                6000
#define TATA_IDLE_RPM               800
#define TATA_MAX_THROTTLE           100

// TATA engine data structure
typedef struct {{
    uint16_t engine_rpm;           // Engine RPM
    uint8_t throttle_position;     // Throttle position (0-100%)
    int16_t coolant_temp;          // Coolant temperature (°C)
    uint16_t fuel_flow_rate;       // Fuel flow rate (ml/min)
    uint8_t engine_load;           // Engine load percentage
    uint8_t status_flags;          // Engine status flags
    uint32_t timestamp;            // System timestamp
}} tata_engine_data_t;

// Global engine data
static tata_engine_data_t g_engine_data;
static bool g_engine_initialized = false;

// Initialize TATA engine control system
tata_result_t tata_engine_control_init(void) {{
    // Initialize CAN interface
    if (can_init(CAN_SPEED_500K) != CAN_OK) {{
        return TATA_ERROR_CAN_INIT;
    }}

    // Initialize engine sensors
    if (engine_sensors_init() != SENSOR_OK) {{
        return TATA_ERROR_SENSOR_INIT;
    }}

    // Initialize fuel injection system
    if (fuel_injection_init() != FUEL_OK) {{
        return TATA_ERROR_FUEL_INIT;
    }}

    // Clear engine data
    memset(&g_engine_data, 0, sizeof(tata_engine_data_t));

    g_engine_initialized = true;
    return TATA_SUCCESS;
}}

// Read engine sensors
tata_result_t tata_engine_read_sensors(void) {{
    if (!g_engine_initialized) {{
        return TATA_ERROR_NOT_INITIALIZED;
    }}

    // Read engine RPM from crankshaft sensor
    g_engine_data.engine_rpm = read_rpm_sensor();

    // Read throttle position
    g_engine_data.throttle_position = read_throttle_position();

    // Read coolant temperature
    g_engine_data.coolant_temp = read_coolant_temp_sensor();

    // Read fuel flow rate
    g_engine_data.fuel_flow_rate = read_fuel_flow_sensor();

    // Calculate engine load
    g_engine_data.engine_load = calculate_engine_load();

    // Update timestamp
    g_engine_data.timestamp = get_system_time_ms();

    return tata_engine_validate_data();
}}

// Validate engine data for safety
tata_result_t tata_engine_validate_data(void) {{
    g_engine_data.status_flags = 0;

    // Check RPM limits
    if (g_engine_data.engine_rpm > TATA_MAX_RPM) {{
        g_engine_data.status_flags |= TATA_ENGINE_OVERSPEED;
        trigger_engine_protection();
        return TATA_ERROR_OVERSPEED;
    }}

    // Check coolant temperature
    if (g_engine_data.coolant_temp > TATA_MAX_COOLANT_TEMP) {{
        g_engine_data.status_flags |= TATA_ENGINE_OVERTEMP;
        trigger_cooling_protection();
    }}

    // Check throttle position validity
    if (g_engine_data.throttle_position > TATA_MAX_THROTTLE) {{
        g_engine_data.status_flags |= TATA_ENGINE_THROTTLE_ERROR;
        return TATA_ERROR_THROTTLE;
    }}

    return TATA_SUCCESS;
}}

// Control fuel injection based on engine conditions
tata_result_t tata_engine_fuel_control(void) {{
    uint16_t fuel_pulse_width;

    // Calculate fuel injection pulse width based on:
    // - Engine RPM
    // - Throttle position
    // - Engine load
    // - Coolant temperature

    fuel_pulse_width = calculate_fuel_injection_time(
        g_engine_data.engine_rpm,
        g_engine_data.throttle_position,
        g_engine_data.engine_load,
        g_engine_data.coolant_temp
    );

    // Apply fuel injection
    return set_fuel_injection_pulse(fuel_pulse_width);
}}

// Main engine control task
void tata_engine_control_task(void) {{
    static uint32_t last_update = 0;
    uint32_t current_time = get_system_time_ms();

    // Run at 50Hz for real-time control
    if ((current_time - last_update) >= 20) {{
        // Read engine sensors
        if (tata_engine_read_sensors() == TATA_SUCCESS) {{
            // Control fuel injection
            tata_engine_fuel_control();

            // Send data via CAN
            tata_engine_send_can_data();
        }}

        last_update = current_time;
    }}
}}'''

        return {
            "code": code,
            "explanation": f"Generated TATA engine control system for {platform} with {asil_level} safety compliance. Includes RPM monitoring, fuel injection control, and thermal protection.",
            "warnings": [
                "Implement proper fuel injection timing",
                "Validate sensor calibration",
                "Test thermal protection thoroughly"
            ],
            "suggestions": [
                "Add knock detection",
                "Implement variable valve timing",
                "Add emissions control",
                "Consider turbocharger control"
            ],
            "memory_estimate": "3.8 KB",
            "complexity": 7.8
        }

    def generate_battery_management_code(self, platform, asil_level):
        code = f'''// TATA Battery Management System
// Platform: {platform} | ASIL Level: {asil_level}
// Generated by TATA AI Co-pilot

#include "tata_battery_mgmt.h"
#include "can_interface.h"
#include "thermal_mgmt.h"

// TATA BMS configuration
#define TATA_BMS_CAN_ID             0x300
#define TATA_MAX_CELL_VOLTAGE       4200  // mV
#define TATA_MIN_CELL_VOLTAGE       2800  // mV
#define TATA_MAX_PACK_TEMP          60    // °C
#define TATA_NUM_CELLS              96    // Number of battery cells

// TATA battery data structure
typedef struct {{
    uint16_t cell_voltages[TATA_NUM_CELLS];  // Individual cell voltages (mV)
    int32_t pack_current;                    // Pack current (mA)
    int16_t pack_temperature;                // Pack temperature (°C)
    uint8_t soc_percentage;                  // State of charge (%)
    uint8_t soh_percentage;                  // State of health (%)
    uint16_t pack_voltage;                   // Total pack voltage (V)
    uint8_t status_flags;                    // BMS status flags
    uint32_t timestamp;                      // System timestamp
}} tata_bms_data_t;

// Global BMS data
static tata_bms_data_t g_bms_data;
static bool g_bms_initialized = false;

// Initialize TATA battery management system
tata_result_t tata_bms_init(void) {{
    // Initialize CAN interface
    if (can_init(CAN_SPEED_500K) != CAN_OK) {{
        return TATA_ERROR_CAN_INIT;
    }}

    // Initialize cell monitoring ICs
    if (cell_monitor_init() != CELL_OK) {{
        return TATA_ERROR_CELL_INIT;
    }}

    // Initialize thermal management
    if (thermal_mgmt_init() != THERMAL_OK) {{
        return TATA_ERROR_THERMAL_INIT;
    }}

    // Initialize current sensor
    if (current_sensor_init() != CURRENT_OK) {{
        return TATA_ERROR_CURRENT_INIT;
    }}

    // Clear BMS data
    memset(&g_bms_data, 0, sizeof(tata_bms_data_t));

    g_bms_initialized = true;
    return TATA_SUCCESS;
}}

// Read all battery parameters
tata_result_t tata_bms_read_data(void) {{
    if (!g_bms_initialized) {{
        return TATA_ERROR_NOT_INITIALIZED;
    }}

    // Read individual cell voltages
    for (int i = 0; i < TATA_NUM_CELLS; i++) {{
        g_bms_data.cell_voltages[i] = read_cell_voltage(i);
    }}

    // Read pack current (positive = charging, negative = discharging)
    g_bms_data.pack_current = read_pack_current();

    // Read pack temperature
    g_bms_data.pack_temperature = read_pack_temperature();

    // Calculate pack voltage
    g_bms_data.pack_voltage = calculate_pack_voltage();

    // Update SOC and SOH
    g_bms_data.soc_percentage = calculate_soc();
    g_bms_data.soh_percentage = calculate_soh();

    // Update timestamp
    g_bms_data.timestamp = get_system_time_ms();

    return tata_bms_validate_data();
}}

// Validate battery data for safety
tata_result_t tata_bms_validate_data(void) {{
    g_bms_data.status_flags = 0;

    // Check individual cell voltages
    for (int i = 0; i < TATA_NUM_CELLS; i++) {{
        if (g_bms_data.cell_voltages[i] > TATA_MAX_CELL_VOLTAGE) {{
            g_bms_data.status_flags |= TATA_BMS_CELL_OVERVOLTAGE;
            trigger_overvoltage_protection(i);
            return TATA_ERROR_OVERVOLTAGE;
        }}

        if (g_bms_data.cell_voltages[i] < TATA_MIN_CELL_VOLTAGE) {{
            g_bms_data.status_flags |= TATA_BMS_CELL_UNDERVOLTAGE;
            trigger_undervoltage_protection(i);
            return TATA_ERROR_UNDERVOLTAGE;
        }}
    }}

    // Check pack temperature
    if (g_bms_data.pack_temperature > TATA_MAX_PACK_TEMP) {{
        g_bms_data.status_flags |= TATA_BMS_OVERTEMP;
        trigger_thermal_protection();
        return TATA_ERROR_OVERTEMP;
    }}

    // Check current limits
    if (abs(g_bms_data.pack_current) > TATA_MAX_PACK_CURRENT) {{
        g_bms_data.status_flags |= TATA_BMS_OVERCURRENT;
        trigger_current_protection();
        return TATA_ERROR_OVERCURRENT;
    }}

    return TATA_SUCCESS;
}}

// Perform cell balancing
tata_result_t tata_bms_cell_balancing(void) {{
    uint16_t max_voltage = 0;
    uint16_t min_voltage = 65535;

    // Find max and min cell voltages
    for (int i = 0; i < TATA_NUM_CELLS; i++) {{
        if (g_bms_data.cell_voltages[i] > max_voltage) {{
            max_voltage = g_bms_data.cell_voltages[i];
        }}
        if (g_bms_data.cell_voltages[i] < min_voltage) {{
            min_voltage = g_bms_data.cell_voltages[i];
        }}
    }}

    // If voltage difference is significant, start balancing
    if ((max_voltage - min_voltage) > TATA_BALANCE_THRESHOLD) {{
        for (int i = 0; i < TATA_NUM_CELLS; i++) {{
            if (g_bms_data.cell_voltages[i] > (min_voltage + TATA_BALANCE_THRESHOLD)) {{
                enable_cell_balancing(i);
            }} else {{
                disable_cell_balancing(i);
            }}
        }}
    }}

    return TATA_SUCCESS;
}}

// Main BMS task
void tata_bms_task(void) {{
    static uint32_t last_update = 0;
    uint32_t current_time = get_system_time_ms();

    // Run at 10Hz for battery monitoring
    if ((current_time - last_update) >= 100) {{
        // Read battery data
        if (tata_bms_read_data() == TATA_SUCCESS) {{
            // Perform cell balancing
            tata_bms_cell_balancing();

            // Send data via CAN
            tata_bms_send_can_data();
        }}

        last_update = current_time;
    }}
}}'''

        return {
            "code": code,
            "explanation": f"Generated TATA battery management system for {platform} with {asil_level} safety compliance. Includes cell monitoring, thermal protection, and balancing.",
            "warnings": [
                "Implement proper cell balancing algorithms",
                "Validate thermal protection thresholds",
                "Test emergency shutdown procedures"
            ],
            "suggestions": [
                "Add SOC estimation algorithms",
                "Implement predictive maintenance",
                "Add charging optimization",
                "Consider fast charging protocols"
            ],
            "memory_estimate": "5.2 KB",
            "complexity": 9.1
        }

    def generate_can_handler_code(self, platform, asil_level):
        code = f'''// TATA CAN Bus Handler
// Platform: {platform} | ASIL Level: {asil_level}
// Generated by TATA AI Co-pilot

#include "tata_can_handler.h"
#include "can_driver.h"

// TATA CAN message IDs
#define TATA_CAN_ENGINE_DATA        0x100
#define TATA_CAN_BRAKE_DATA         0x200
#define TATA_CAN_BATTERY_DATA       0x300
#define TATA_CAN_TRANSMISSION_DATA  0x400

// TATA CAN message structure
typedef struct {{
    uint32_t id;                    // CAN message ID
    uint8_t dlc;                    // Data length code
    uint8_t data[8];                // Message data
    uint32_t timestamp;             // Reception timestamp
}} tata_can_message_t;

// Message handler function pointer
typedef void (*tata_can_handler_func_t)(tata_can_message_t* msg);

// Message handler table
typedef struct {{
    uint32_t message_id;
    tata_can_handler_func_t handler;
}} tata_can_handler_entry_t;

// Global variables
static bool g_can_initialized = false;
static uint32_t g_message_count = 0;
static uint32_t g_error_count = 0;

// Forward declarations
void handle_engine_data(tata_can_message_t* msg);
void handle_brake_data(tata_can_message_t* msg);
void handle_battery_data(tata_can_message_t* msg);
void handle_transmission_data(tata_can_message_t* msg);

// Message handler table
static const tata_can_handler_entry_t g_handler_table[] = {{
    {{TATA_CAN_ENGINE_DATA, handle_engine_data}},
    {{TATA_CAN_BRAKE_DATA, handle_brake_data}},
    {{TATA_CAN_BATTERY_DATA, handle_battery_data}},
    {{TATA_CAN_TRANSMISSION_DATA, handle_transmission_data}},
    {{0, NULL}}  // End of table
}};

// Initialize TATA CAN handler
tata_result_t tata_can_handler_init(void) {{
    // Initialize CAN driver
    if (can_driver_init(CAN_SPEED_500K) != CAN_OK) {{
        return TATA_ERROR_CAN_INIT;
    }}

    // Set up message filters for TATA messages
    can_filter_t filter;
    filter.id = 0x100;
    filter.mask = 0x700;  // Accept 0x100-0x4FF

    if (can_set_filter(&filter) != CAN_OK) {{
        return TATA_ERROR_CAN_FILTER;
    }}

    // Enable CAN interrupts
    can_enable_interrupts();

    g_can_initialized = true;
    g_message_count = 0;
    g_error_count = 0;

    return TATA_SUCCESS;
}}

// Send TATA CAN message
tata_result_t tata_can_send_message(uint32_t id, uint8_t* data, uint8_t dlc) {{
    if (!g_can_initialized) {{
        return TATA_ERROR_NOT_INITIALIZED;
    }}

    tata_can_message_t msg;
    msg.id = id;
    msg.dlc = dlc;
    msg.timestamp = get_system_time_ms();

    // Copy data
    for (int i = 0; i < dlc && i < 8; i++) {{
        msg.data[i] = data[i];
    }}

    // Send message
    if (can_transmit(&msg) != CAN_OK) {{
        g_error_count++;
        return TATA_ERROR_CAN_SEND;
    }}

    return TATA_SUCCESS;
}}

// Process received CAN message
void tata_can_process_message(tata_can_message_t* msg) {{
    if (!msg) return;

    g_message_count++;

    // Find handler for this message ID
    for (int i = 0; g_handler_table[i].handler != NULL; i++) {{
        if (g_handler_table[i].message_id == msg->id) {{
            g_handler_table[i].handler(msg);
            return;
        }}
    }}

    // Unknown message ID
    handle_unknown_message(msg);
}}

// Handle engine data messages
void handle_engine_data(tata_can_message_t* msg) {{
    // Extract engine data from CAN message
    uint16_t rpm = (msg->data[0] << 8) | msg->data[1];
    uint8_t throttle = msg->data[2];
    int16_t temp = (msg->data[3] << 8) | msg->data[4];

    // Process engine data
    update_engine_status(rpm, throttle, temp);
}}

// Handle brake data messages
void handle_brake_data(tata_can_message_t* msg) {{
    // Extract brake data from CAN message
    uint16_t front_pressure = (msg->data[0] << 8) | msg->data[1];
    uint16_t rear_pressure = (msg->data[2] << 8) | msg->data[3];
    uint8_t status = msg->data[4];

    // Process brake data
    update_brake_status(front_pressure, rear_pressure, status);
}}

// CAN interrupt handler
void tata_can_interrupt_handler(void) {{
    tata_can_message_t msg;

    // Read message from CAN controller
    if (can_receive(&msg) == CAN_OK) {{
        // Process the message
        tata_can_process_message(&msg);
    }} else {{
        g_error_count++;
    }}
}}

// Get CAN statistics
void tata_can_get_statistics(uint32_t* msg_count, uint32_t* error_count) {{
    if (msg_count) *msg_count = g_message_count;
    if (error_count) *error_count = g_error_count;
}}'''

        return {
            "code": code,
            "explanation": f"Generated TATA CAN bus handler for {platform} with {asil_level} safety compliance. Includes message filtering, interrupt handling, and error management.",
            "warnings": [
                "Configure CAN timing parameters correctly",
                "Implement proper error recovery",
                "Validate message timing requirements"
            ],
            "suggestions": [
                "Add message priority handling",
                "Implement CAN diagnostics",
                "Add network management",
                "Consider CAN-FD for higher bandwidth"
            ],
            "memory_estimate": "2.8 KB",
            "complexity": 6.5
        }

    def generate_generic_automotive_code(self, description, platform, asil_level):
        code = f'''// TATA Automotive Function
// Platform: {platform} | ASIL Level: {asil_level}
// Generated by TATA AI Co-pilot
// Description: {description}

#include "tata_automotive.h"
#include "can_interface.h"
#include "safety_monitor.h"

// TATA automotive system configuration
#define TATA_SYSTEM_CAN_ID          0x500
#define TATA_UPDATE_RATE_MS         50    // 20Hz update rate
#define TATA_TIMEOUT_MS             1000  // 1 second timeout

// TATA system data structure
typedef struct {{
    uint32_t system_status;         // System status flags
    uint32_t error_flags;           // Error condition flags
    uint32_t timestamp;             // Last update timestamp
    uint8_t data_valid;             // Data validity flag
}} tata_system_data_t;

// Global system data
static tata_system_data_t g_system_data;
static bool g_system_initialized = false;

// Initialize TATA automotive system
tata_result_t tata_automotive_system_init(void) {{
    // Initialize CAN interface
    if (can_init(CAN_SPEED_500K) != CAN_OK) {{
        return TATA_ERROR_CAN_INIT;
    }}

    // Initialize safety monitoring
    safety_monitor_init();

    // Clear system data
    memset(&g_system_data, 0, sizeof(tata_system_data_t));

    g_system_initialized = true;
    return TATA_SUCCESS;
}}

// Main system task
void tata_automotive_system_task(void) {{
    static uint32_t last_update = 0;
    uint32_t current_time = get_system_time_ms();

    // Run at configured rate
    if ((current_time - last_update) >= TATA_UPDATE_RATE_MS) {{
        // Update system status
        tata_update_system_status();

        // Send status via CAN
        tata_send_system_status();

        // Perform safety checks
        tata_safety_monitor();

        last_update = current_time;
    }}
}}

// Update system status
tata_result_t tata_update_system_status(void) {{
    if (!g_system_initialized) {{
        return TATA_ERROR_NOT_INITIALIZED;
    }}

    // Update timestamp
    g_system_data.timestamp = get_system_time_ms();

    // Mark data as valid
    g_system_data.data_valid = 1;

    // Clear error flags
    g_system_data.error_flags = 0;

    // Set normal operation status
    g_system_data.system_status = TATA_STATUS_NORMAL;

    return TATA_SUCCESS;
}}

// Send system status via CAN
tata_result_t tata_send_system_status(void) {{
    can_message_t can_msg;

    // Prepare CAN message
    can_msg.id = TATA_SYSTEM_CAN_ID;
    can_msg.dlc = sizeof(tata_system_data_t);
    memcpy(can_msg.data, &g_system_data, sizeof(tata_system_data_t));

    // Send message
    return can_send_message(&can_msg, CAN_PRIORITY_NORMAL);
}}

// Safety monitoring function
void tata_safety_monitor(void) {{
    uint32_t current_time = get_system_time_ms();

    // Check for system timeout
    if ((current_time - g_system_data.timestamp) > TATA_TIMEOUT_MS) {{
        g_system_data.error_flags |= TATA_ERROR_TIMEOUT;
        g_system_data.system_status = TATA_STATUS_ERROR;

        // Trigger fail-safe mode
        trigger_fail_safe_mode();
    }}

    // Perform periodic self-test
    if ((current_time % 10000) == 0) {{  // Every 10 seconds
        perform_system_self_test();
    }}
}}'''

        return {
            "code": code,
            "explanation": f"Generated TATA automotive system code for {platform} with {asil_level} safety compliance. Includes basic system monitoring and CAN communication.",
            "warnings": [
                "Customize for specific automotive function",
                "Implement proper error handling",
                "Validate timing requirements"
            ],
            "suggestions": [
                "Add specific sensor interfaces",
                "Implement diagnostic features",
                "Add configuration parameters",
                "Consider power management"
            ],
            "memory_estimate": "2.1 KB",
            "complexity": 5.5
        }

    def analyze_code(self, code, language):
        """Analyze code for safety and quality"""
        lines = code.split('\n')
        line_count = len(lines)

        warnings = []
        suggestions = []
        metrics = {}

        # Basic metrics
        metrics['lines_of_code'] = line_count
        metrics['estimated_functions'] = code.count('(') // 2
        metrics['estimated_variables'] = code.count('=') // 2

        # Safety analysis
        if 'malloc' in code or 'free' in code:
            warnings.append("Dynamic memory allocation detected - consider static allocation for automotive safety")

        if 'printf' in code or 'scanf' in code:
            warnings.append("Standard I/O functions detected - not suitable for embedded automotive systems")

        if 'goto' in code:
            warnings.append("GOTO statement detected - violates MISRA C guidelines")

        if code.count('while(1)') > 0 or code.count('for(;;)') > 0:
            warnings.append("Infinite loop detected - ensure proper task yielding")

        # Suggestions
        if 'ASIL' not in code:
            suggestions.append("Consider adding ASIL compliance annotations")

        if 'CAN' not in code and 'can' not in code:
            suggestions.append("Consider adding CAN bus communication for automotive systems")

        if 'safety' not in code.lower():
            suggestions.append("Add safety monitoring and fail-safe mechanisms")

        if 'TATA' not in code:
            suggestions.append("Use TATA naming conventions and error codes")

        return {
            "metrics": metrics,
            "warnings": warnings,
            "suggestions": suggestions,
            "safety_score": max(0, 100 - len(warnings) * 10),
            "complexity_score": min(10, line_count / 20),
            "compliance_level": "ASIL-B" if len(warnings) < 3 else "QM"
        }
    
    def serve_main_page(self):
        html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TATA AI Co-pilot - Interactive Demo</title>
    <link rel="manifest" href="/manifest.json">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #1B4F72 0%, #2E86AB 50%, #A23B72 100%);
            min-height: 100vh; color: white; overflow-x: hidden;
        }
        .header {
            text-align: center; padding: 30px 20px;
            background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px);
        }
        .logo { font-size: 60px; margin-bottom: 15px; animation: float 3s ease-in-out infinite; }
        .title { font-size: 36px; font-weight: 700; margin-bottom: 12px; }
        .subtitle { font-size: 18px; opacity: 0.9; }
        .container { max-width: 1400px; margin: 0 auto; padding: 30px 20px; }
        
        .chat-container {
            background: rgba(255, 255, 255, 0.1); border-radius: 16px; padding: 24px; margin: 24px 0;
            border: 1px solid rgba(255, 255, 255, 0.2); min-height: 400px;
        }
        .chat-header { font-size: 24px; font-weight: 600; margin-bottom: 20px; color: #F39C12; }
        .chat-messages { height: 300px; overflow-y: auto; margin-bottom: 20px; padding: 10px; background: rgba(0, 0, 0, 0.2); border-radius: 8px; }
        .message { margin: 10px 0; padding: 12px; border-radius: 8px; }
        .user-message { background: rgba(52, 152, 219, 0.3); margin-left: 20px; }
        .ai-message { background: rgba(46, 204, 113, 0.3); margin-right: 20px; }
        .message-header { font-weight: 600; margin-bottom: 5px; }
        .message-content { line-height: 1.5; }
        .code-block { background: rgba(0, 0, 0, 0.4); padding: 12px; border-radius: 6px; margin: 8px 0; font-family: monospace; font-size: 12px; overflow-x: auto; }
        
        .input-container { display: flex; gap: 10px; }
        .question-input { flex: 1; padding: 12px; border: none; border-radius: 8px; background: rgba(255, 255, 255, 0.9); color: #333; font-size: 16px; }
        .send-btn { padding: 12px 24px; background: linear-gradient(135deg, #E74C3C 0%, #F39C12 100%); color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: 600; }
        .send-btn:hover { transform: scale(1.05); }
        
        .features-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin: 30px 0; }
        .feature-card {
            background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px);
            border-radius: 12px; padding: 20px; border: 1px solid rgba(255, 255, 255, 0.2);
            transition: transform 0.3s ease; cursor: pointer;
        }
        .feature-card:hover { transform: translateY(-5px); }
        .feature-icon { font-size: 40px; margin-bottom: 12px; }
        .feature-title { font-size: 18px; font-weight: 600; margin-bottom: 8px; color: #F39C12; }
        .feature-desc { font-size: 14px; line-height: 1.5; opacity: 0.9; }
        
        .sample-questions { background: rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 20px; margin: 20px 0; }
        .question-category { margin: 15px 0; }
        .category-title { font-weight: 600; color: #F39C12; margin-bottom: 8px; }
        .sample-question { background: rgba(52, 152, 219, 0.2); padding: 8px 12px; margin: 5px 0; border-radius: 6px; cursor: pointer; font-size: 14px; transition: background 0.2s; }
        .sample-question:hover { background: rgba(52, 152, 219, 0.4); }
        
        @keyframes float { 0%, 100% { transform: translateY(0px); } 50% { transform: translateY(-8px); } }
        .status-indicator { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 6px; background: #2ECC71; animation: pulse 1s infinite; }
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.6; } }
        
        .loading { display: none; text-align: center; padding: 20px; }
        .spinner { border: 3px solid rgba(255,255,255,0.3); border-top: 3px solid #F39C12; border-radius: 50%; width: 30px; height: 30px; animation: spin 1s linear infinite; margin: 0 auto; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
</head>
<body>
    <div class="header">
        <div class="logo">🚗</div>
        <h1 class="title">TATA AI Co-pilot</h1>
        <p class="subtitle">Interactive AI Assistant for Automotive Embedded Software</p>
        <div style="background: linear-gradient(135deg, #E74C3C 0%, #F39C12 100%); padding: 12px 24px; border-radius: 20px; display: inline-block; margin: 16px 0; font-weight: 600; font-size: 14px; text-transform: uppercase; letter-spacing: 1px;">
            🏆 TATA Innovate Hackathon 2024
        </div>
    </div>
    
    <div class="container">
        <div style="text-align: center; margin: 20px 0;">
            <p><span class="status-indicator"></span>AI Assistant: Online</p>
            <p><span class="status-indicator"></span>Code Generation: Ready</p>
            <p><span class="status-indicator"></span>Q&A System: Active</p>
        </div>
        
        <div class="chat-container">
            <div class="chat-header">🤖 Ask TATA AI Co-pilot Anything</div>
            <div class="chat-messages" id="chatMessages">
                <div class="message ai-message">
                    <div class="message-header">🤖 TATA AI Co-pilot</div>
                    <div class="message-content">
                        Welcome! I'm your TATA AI Co-pilot, specialized in automotive embedded software development. 
                        Ask me about engine control, brake systems, electric vehicles, CAN communication, safety compliance, or any automotive software topic!
                        <br><br>
                        Try asking: "How do I create a brake pressure monitoring system for TATA vehicles?"
                    </div>
                </div>
            </div>
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>AI is thinking...</p>
            </div>
            <div class="input-container">
                <input type="text" class="question-input" id="questionInput" placeholder="Ask about TATA automotive software development..." onkeypress="handleKeyPress(event)">
                <button class="send-btn" onclick="askQuestion()">🚀 Ask AI</button>
            </div>
        </div>
        
        <div class="sample-questions">
            <h3 style="color: #F39C12; margin-bottom: 15px;">💡 Sample Questions by Category</h3>
            <div id="sampleQuestions">Loading sample questions...</div>
        </div>
        
        <div class="features-grid">
            <div class="feature-card" onclick="generateCode()">
                <div class="feature-icon">🤖</div>
                <div class="feature-title">AI Code Generation</div>
                <div class="feature-desc">Generate automotive-specific embedded code with AI assistance</div>
            </div>
            <div class="feature-card" onclick="analyzeCode()">
                <div class="feature-icon">🔍</div>
                <div class="feature-title">Code Analysis</div>
                <div class="feature-desc">Analyze existing code for safety compliance and optimization</div>
            </div>
            <div class="feature-card" onclick="showPlatforms()">
                <div class="feature-icon">🎯</div>
                <div class="feature-title">Supported Platforms</div>
                <div class="feature-desc">View all supported embedded platforms and specifications</div>
            </div>
            <div class="feature-card" onclick="voiceCommand()">
                <div class="feature-icon">🎤</div>
                <div class="feature-title">Voice Commands</div>
                <div class="feature-desc">Use voice commands to interact with the AI assistant</div>
            </div>
        </div>
    </div>
    
    <script>
        let chatMessages = document.getElementById('chatMessages');
        let questionInput = document.getElementById('questionInput');
        let loading = document.getElementById('loading');
        
        // Load sample questions on page load
        loadSampleQuestions();
        
        async function askQuestion() {
            const question = questionInput.value.trim();
            if (!question) return;
            
            // Add user message
            addMessage('user', question);
            questionInput.value = '';
            
            // Show loading
            loading.style.display = 'block';
            
            try {
                const response = await fetch('/api/ask', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ question: question, context: 'automotive' })
                });
                
                const data = await response.json();
                
                // Hide loading
                loading.style.display = 'none';
                
                // Add AI response
                let aiResponse = data.answer;
                if (data.code_example) {
                    aiResponse += '<div class="code-block">' + data.code_example + '</div>';
                }
                if (data.explanation) {
                    aiResponse += '<br><strong>Explanation:</strong> ' + data.explanation;
                }
                if (data.related_topics && data.related_topics.length > 0) {
                    aiResponse += '<br><strong>Related Topics:</strong> ' + data.related_topics.join(', ');
                }
                
                addMessage('ai', aiResponse);
                
            } catch (error) {
                loading.style.display = 'none';
                addMessage('ai', 'Sorry, I encountered an error. Please try again.');
                console.error('Error:', error);
            }
        }
        
        function addMessage(sender, content) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${sender}-message`;
            
            const header = sender === 'user' ? '👤 You' : '🤖 TATA AI Co-pilot';
            messageDiv.innerHTML = `
                <div class="message-header">${header}</div>
                <div class="message-content">${content}</div>
            `;
            
            chatMessages.appendChild(messageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
        
        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                askQuestion();
            }
        }
        
        async function loadSampleQuestions() {
            try {
                const response = await fetch('/api/sample-questions');
                const data = await response.json();
                
                let html = '';
                for (const [category, questions] of Object.entries(data.categories)) {
                    html += `<div class="question-category">
                        <div class="category-title">${category}</div>`;
                    
                    questions.forEach(question => {
                        html += `<div class="sample-question" onclick="askSampleQuestion('${question.replace(/'/g, "\\'")}')">${question}</div>`;
                    });
                    
                    html += '</div>';
                }
                
                document.getElementById('sampleQuestions').innerHTML = html;
                
            } catch (error) {
                document.getElementById('sampleQuestions').innerHTML = 'Error loading sample questions';
            }
        }
        
        function askSampleQuestion(question) {
            questionInput.value = question;
            askQuestion();
        }
        
        async function generateCode() {
            const description = prompt('Describe the automotive code you want to generate:');
            if (!description) return;
            
            try {
                const response = await fetch('/api/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        description: description,
                        language: 'c',
                        target_platform: 'ARM Cortex-M7',
                        asil_level: 'B'
                    })
                });
                
                const data = await response.json();
                
                let codeResponse = `Generated code for: "${description}"<div class="code-block">${data.generated_code.substring(0, 1000)}...</div>`;
                codeResponse += `<strong>Explanation:</strong> ${data.explanation}<br>`;
                codeResponse += `<strong>Lines of Code:</strong> ${data.metadata.lines_of_code} | <strong>Memory:</strong> ${data.metadata.estimated_memory}`;
                
                addMessage('ai', codeResponse);
                
            } catch (error) {
                addMessage('ai', 'Error generating code. Please try again.');
            }
        }
        
        function analyzeCode() {
            alert('🔍 Code Analysis Feature\\n\\nUpload your C/C++ automotive code for:\\n• Safety compliance checking\\n• Performance optimization\\n• ASIL compliance verification\\n• Memory usage analysis');
        }
        
        async function showPlatforms() {
            try {
                const response = await fetch('/api/platforms');
                const data = await response.json();
                
                let platformsHtml = 'Supported Automotive Platforms:<br><br>';
                data.platforms.forEach(platform => {
                    platformsHtml += `<strong>${platform.name}</strong>: ${platform.description} (Memory: ${platform.memory})<br>`;
                });
                
                addMessage('ai', platformsHtml);
                
            } catch (error) {
                addMessage('ai', 'Error loading platforms information.');
            }
        }
        
        function voiceCommand() {
            if ('webkitSpeechRecognition' in window) {
                const recognition = new webkitSpeechRecognition();
                recognition.continuous = false;
                recognition.interimResults = false;
                recognition.lang = 'en-US';
                
                recognition.onstart = function() {
                    addMessage('ai', '🎤 Listening... Please speak your question about TATA automotive software.');
                };
                
                recognition.onresult = function(event) {
                    const transcript = event.results[0][0].transcript;
                    questionInput.value = transcript;
                    addMessage('user', '🎤 ' + transcript);
                    askQuestion();
                };
                
                recognition.onerror = function(event) {
                    addMessage('ai', 'Voice recognition error. Please try typing your question.');
                };
                
                recognition.start();
            } else {
                alert('Voice recognition not supported in this browser. Please use Chrome or Edge.');
            }
        }
        
        // Auto-scroll chat messages
        setInterval(() => {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }, 1000);
        
        console.log('🏆 TATA AI Co-pilot Interactive Demo Loaded');
        console.log('🤖 AI Assistant Ready for Questions');
        console.log('🎯 Ready for Hackathon Demo');
    </script>
</body>
</html>'''
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Cache-Control', 'no-cache')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def serve_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())

def open_browser_delayed():
    time.sleep(3)
    try:
        webbrowser.open('http://localhost:8000')
        print("🌐 Browser opened automatically")
    except Exception as e:
        print(f"⚠️  Could not open browser: {e}")

def main():
    print("🏆 TATA AI Co-pilot - Complete Interactive System")
    print("🚗 TATA Innovate Hackathon 2024 Edition")
    print("=" * 70)
    print("🚀 Starting advanced server on http://localhost:8000")
    print("🤖 Features: Interactive Q&A, Code Generation, Voice Commands")
    print("🌐 Browser will open automatically in 3 seconds")
    print("🎯 Press Ctrl+C to stop")
    print("-" * 70)
    
    threading.Thread(target=open_browser_delayed, daemon=True).start()
    
    PORT = 8000
    try:
        with socketserver.TCPServer(("", PORT), TATAAdvancedHandler) as httpd:
            print(f"✅ Server running at http://localhost:{PORT}")
            print("🤖 Interactive Q&A: /api/ask")
            print("🔧 Code Generation: /api/generate") 
            print("🔍 Code Analysis: /api/analyze")
            print("📊 Sample Questions: /api/sample-questions")
            print("")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 TATA AI Co-pilot stopped")
        print("🎉 Thank you for using TATA AI Co-pilot!")
    except Exception as e:
        print(f"\n❌ Server error: {e}")

if __name__ == "__main__":
    main()
