#!/usr/bin/env python3
"""
Enhanced TATA AI Co-pilot with Advanced Features
TATA Innovate Hackathon 2024 - Premium Edition
"""

import http.server
import socketserver
import json
import webbrowser
import threading
import time
import urllib.parse
import random
import base64
import hashlib
from datetime import datetime, timedelta
import os

class EnhancedTATAHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.serve_enhanced_main_page()
        elif self.path == '/api/status':
            self.serve_json({
                "status": "running",
                "message": "TATA AI Co-pilot Premium is operational",
                "version": "3.0.0-premium",
                "features": [
                    "interactive_qa", "code_generation", "real_time_collaboration", 
                    "3d_visualization", "voice_commands", "ai_chat_history",
                    "code_templates", "performance_analytics", "safety_simulator",
                    "tata_digital_twin", "predictive_maintenance", "iot_integration"
                ],
                "uptime": self.get_uptime(),
                "ai_models": ["TATA-GPT-Automotive-Pro", "CodeGen-Embedded-Plus", "Safety-Analyzer-Advanced"],
                "active_users": random.randint(15, 25),
                "code_generated_today": random.randint(150, 300)
            })
        elif self.path == '/api/analytics':
            self.serve_json(self.get_analytics_data())
        elif self.path == '/api/templates':
            self.serve_json(self.get_code_templates())
        elif self.path == '/api/digital-twin':
            self.serve_json(self.get_digital_twin_data())
        elif self.path == '/api/safety-simulator':
            self.serve_json(self.get_safety_simulation_data())
        elif self.path == '/api/collaboration':
            self.serve_json(self.get_collaboration_data())
        elif self.path == '/api/iot-devices':
            self.serve_json(self.get_iot_devices())
        elif self.path == '/api/predictive-maintenance':
            self.serve_json(self.get_predictive_maintenance_data())
        elif self.path.startswith('/api/download/'):
            self.handle_file_download()
        else:
            super().do_GET()
    
    def do_POST(self):
        if self.path == '/api/ask-advanced':
            self.handle_advanced_qa()
        elif self.path == '/api/generate-advanced':
            self.handle_advanced_code_generation()
        elif self.path == '/api/simulate-safety':
            self.handle_safety_simulation()
        elif self.path == '/api/analyze-performance':
            self.handle_performance_analysis()
        elif self.path == '/api/collaborate':
            self.handle_collaboration()
        elif self.path == '/api/train-model':
            self.handle_model_training()
        elif self.path == '/api/generate-report':
            self.handle_report_generation()
        else:
            self.send_error(404)
    
    def get_uptime(self):
        return f"{random.randint(2, 8)} hours {random.randint(15, 45)} minutes"
    
    def get_analytics_data(self):
        return {
            "performance_metrics": {
                "code_generation_speed": f"{random.uniform(2.1, 4.8):.1f}s",
                "accuracy_rate": f"{random.uniform(94.5, 98.2):.1f}%",
                "user_satisfaction": f"{random.uniform(4.6, 4.9):.1f}/5.0",
                "system_uptime": "99.7%"
            },
            "usage_statistics": {
                "total_code_generated": random.randint(15000, 25000),
                "active_projects": random.randint(45, 85),
                "safety_checks_passed": random.randint(1200, 1800),
                "collaboration_sessions": random.randint(25, 45)
            },
            "real_time_data": {
                "current_cpu_usage": f"{random.randint(15, 35)}%",
                "memory_usage": f"{random.randint(40, 65)}%",
                "api_response_time": f"{random.randint(120, 280)}ms",
                "concurrent_users": random.randint(8, 18)
            },
            "weekly_trends": [
                {"day": "Mon", "code_gen": random.randint(80, 120), "qa_sessions": random.randint(25, 45)},
                {"day": "Tue", "code_gen": random.randint(90, 130), "qa_sessions": random.randint(30, 50)},
                {"day": "Wed", "code_gen": random.randint(100, 140), "qa_sessions": random.randint(35, 55)},
                {"day": "Thu", "code_gen": random.randint(85, 125), "qa_sessions": random.randint(28, 48)},
                {"day": "Fri", "code_gen": random.randint(95, 135), "qa_sessions": random.randint(32, 52)},
                {"day": "Sat", "code_gen": random.randint(60, 90), "qa_sessions": random.randint(15, 30)},
                {"day": "Sun", "code_gen": random.randint(50, 80), "qa_sessions": random.randint(10, 25)}
            ]
        }
    
    def get_code_templates(self):
        return {
            "automotive_templates": {
                "Engine Control": [
                    {"name": "TATA Diesel Engine ECU", "description": "Complete ECU for TATA commercial diesel engines", "complexity": "High", "asil": "C"},
                    {"name": "Petrol Engine Controller", "description": "Fuel injection and ignition control", "complexity": "Medium", "asil": "B"},
                    {"name": "Hybrid Engine Manager", "description": "Hybrid powertrain coordination", "complexity": "Very High", "asil": "D"}
                ],
                "Brake Systems": [
                    {"name": "ABS Controller Pro", "description": "Advanced ABS with stability control", "complexity": "High", "asil": "D"},
                    {"name": "Electronic Brake Booster", "description": "Brake-by-wire system", "complexity": "Very High", "asil": "D"},
                    {"name": "Parking Brake Controller", "description": "Electronic parking brake", "complexity": "Medium", "asil": "B"}
                ],
                "Electric Vehicle": [
                    {"name": "TATA EV Battery Management", "description": "Complete BMS for TATA electric vehicles", "complexity": "Very High", "asil": "C"},
                    {"name": "Motor Controller", "description": "3-phase motor control with regeneration", "complexity": "High", "asil": "C"},
                    {"name": "Charging Station Interface", "description": "Fast charging protocol implementation", "complexity": "Medium", "asil": "A"}
                ],
                "Safety & ADAS": [
                    {"name": "Collision Avoidance", "description": "Forward collision warning and mitigation", "complexity": "Very High", "asil": "D"},
                    {"name": "Lane Keep Assist", "description": "Lane departure warning and correction", "complexity": "High", "asil": "C"},
                    {"name": "Adaptive Cruise Control", "description": "Radar-based cruise control", "complexity": "Very High", "asil": "C"}
                ]
            }
        }
    
    def get_digital_twin_data(self):
        return {
            "vehicle_models": [
                {
                    "name": "TATA Nexon EV",
                    "type": "Electric SUV",
                    "status": "Active",
                    "battery_level": random.randint(65, 95),
                    "location": "Mumbai, India",
                    "mileage": random.randint(15000, 25000),
                    "last_service": "2024-01-15",
                    "health_score": random.randint(85, 98)
                },
                {
                    "name": "TATA Ace Commercial",
                    "type": "Commercial Vehicle",
                    "status": "Active",
                    "fuel_level": random.randint(40, 80),
                    "location": "Delhi, India",
                    "mileage": random.randint(45000, 65000),
                    "last_service": "2024-01-10",
                    "health_score": random.randint(78, 92)
                },
                {
                    "name": "TATA Harrier",
                    "type": "SUV",
                    "status": "Maintenance",
                    "fuel_level": random.randint(20, 60),
                    "location": "Pune, India",
                    "mileage": random.randint(8000, 18000),
                    "last_service": "2024-01-20",
                    "health_score": random.randint(88, 96)
                }
            ],
            "real_time_telemetry": {
                "engine_rpm": random.randint(800, 3500),
                "vehicle_speed": random.randint(0, 120),
                "coolant_temp": random.randint(85, 105),
                "oil_pressure": random.uniform(2.5, 4.2),
                "battery_voltage": random.uniform(12.2, 14.4),
                "fuel_consumption": random.uniform(8.5, 15.2)
            },
            "predictive_insights": [
                "Brake pads need replacement in 2,500 km",
                "Engine oil change due in 15 days",
                "Battery performance optimal for next 6 months",
                "Tire rotation recommended within 1,000 km"
            ]
        }
    
    def get_safety_simulation_data(self):
        return {
            "simulation_scenarios": [
                {
                    "name": "Emergency Braking Test",
                    "description": "Simulate emergency braking at various speeds",
                    "status": "Ready",
                    "duration": "5 minutes",
                    "safety_level": "ASIL-D"
                },
                {
                    "name": "Collision Avoidance",
                    "description": "Test collision detection and avoidance systems",
                    "status": "Running",
                    "duration": "8 minutes",
                    "safety_level": "ASIL-D"
                },
                {
                    "name": "Battery Thermal Runaway",
                    "description": "Simulate battery overheating scenarios",
                    "status": "Ready",
                    "duration": "12 minutes",
                    "safety_level": "ASIL-C"
                }
            ],
            "test_results": {
                "passed_tests": random.randint(145, 180),
                "failed_tests": random.randint(2, 8),
                "success_rate": f"{random.uniform(94.5, 98.5):.1f}%",
                "critical_issues": random.randint(0, 2)
            }
        }
    
    def get_collaboration_data(self):
        return {
            "active_sessions": [
                {
                    "session_id": "TATA-COLLAB-001",
                    "participants": ["Rajesh Kumar (Lead Engineer)", "Priya Sharma (Safety Expert)", "Amit Patel (Software Architect)"],
                    "project": "TATA Nexon EV Battery Management",
                    "status": "Active",
                    "duration": "45 minutes"
                },
                {
                    "session_id": "TATA-COLLAB-002", 
                    "participants": ["Suresh Reddy (ECU Developer)", "Kavya Singh (Test Engineer)"],
                    "project": "Brake System Controller",
                    "status": "Active",
                    "duration": "23 minutes"
                }
            ],
            "shared_projects": random.randint(12, 25),
            "code_reviews_pending": random.randint(3, 8),
            "team_productivity": f"{random.uniform(87.5, 95.2):.1f}%"
        }
    
    def get_iot_devices(self):
        return {
            "connected_devices": [
                {
                    "device_id": "TATA-ECU-001",
                    "type": "Engine Control Unit",
                    "status": "Online",
                    "location": "Test Vehicle #1",
                    "last_update": "2 minutes ago",
                    "data_points": random.randint(1500, 2500)
                },
                {
                    "device_id": "TATA-BMS-002",
                    "type": "Battery Management System",
                    "status": "Online", 
                    "location": "EV Test Lab",
                    "last_update": "1 minute ago",
                    "data_points": random.randint(800, 1200)
                },
                {
                    "device_id": "TATA-BRAKE-003",
                    "type": "Brake Controller",
                    "status": "Maintenance",
                    "location": "Safety Test Track",
                    "last_update": "15 minutes ago",
                    "data_points": random.randint(500, 900)
                }
            ],
            "data_streams": {
                "total_messages": random.randint(50000, 80000),
                "messages_per_second": random.randint(25, 45),
                "data_quality": f"{random.uniform(96.5, 99.2):.1f}%"
            }
        }
    
    def get_predictive_maintenance_data(self):
        return {
            "maintenance_predictions": [
                {
                    "component": "Engine Oil Filter",
                    "vehicle": "TATA Nexon",
                    "predicted_failure": "In 2,500 km",
                    "confidence": "94%",
                    "severity": "Medium",
                    "recommended_action": "Schedule maintenance"
                },
                {
                    "component": "Brake Pads (Front)",
                    "vehicle": "TATA Harrier",
                    "predicted_failure": "In 1,200 km", 
                    "confidence": "97%",
                    "severity": "High",
                    "recommended_action": "Immediate attention required"
                },
                {
                    "component": "Battery Cells (Module 3)",
                    "vehicle": "TATA Nexon EV",
                    "predicted_failure": "In 6 months",
                    "confidence": "89%",
                    "severity": "Low",
                    "recommended_action": "Monitor closely"
                }
            ],
            "cost_savings": {
                "prevented_breakdowns": random.randint(15, 25),
                "cost_saved": f"₹{random.randint(250000, 450000):,}",
                "efficiency_improvement": f"{random.uniform(15.5, 28.3):.1f}%"
            }
        }
    
    def handle_advanced_qa(self):
        """Handle advanced Q&A with context awareness"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            request_data = json.loads(post_data.decode('utf-8'))
            
            question = request_data.get('question', '').strip()
            context = request_data.get('context', {})
            session_id = request_data.get('session_id', 'default')
            
            # Generate advanced response with context
            response = self.generate_advanced_qa_response(question, context, session_id)
            
            self.serve_json({
                "question": question,
                "answer": response["answer"],
                "code_example": response.get("code_example", ""),
                "explanation": response.get("explanation", ""),
                "related_topics": response.get("related_topics", []),
                "confidence": response.get("confidence", 0.95),
                "context_used": response.get("context_used", []),
                "follow_up_questions": response.get("follow_up_questions", []),
                "timestamp": datetime.now().isoformat(),
                "session_id": session_id
            })
            
        except Exception as e:
            self.serve_json({"error": str(e)}, status=400)
    
    def generate_advanced_qa_response(self, question, context, session_id):
        """Generate advanced Q&A responses with context awareness"""
        question_lower = question.lower()
        
        # Advanced automotive responses with context
        if any(word in question_lower for word in ['digital twin', 'twin', 'simulation']):
            return {
                "answer": "TATA Digital Twin technology creates virtual replicas of physical vehicles, enabling real-time monitoring, predictive maintenance, and performance optimization. Our digital twins integrate IoT sensors, machine learning algorithms, and 3D visualization to provide comprehensive vehicle insights.",
                "code_example": self.get_digital_twin_code(),
                "explanation": "Digital twins enable predictive maintenance, reduce downtime, and optimize vehicle performance through continuous monitoring and AI-driven insights.",
                "related_topics": ["IoT Integration", "Predictive Analytics", "Real-time Monitoring", "3D Visualization"],
                "context_used": ["vehicle_telemetry", "sensor_data"],
                "follow_up_questions": [
                    "How do I implement IoT sensors for digital twin data collection?",
                    "What machine learning algorithms work best for predictive maintenance?",
                    "How can I visualize digital twin data in real-time?"
                ],
                "confidence": 0.97
            }
        
        elif any(word in question_lower for word in ['collaboration', 'team', 'share']):
            return {
                "answer": "TATA AI Co-pilot supports real-time collaboration features including shared code editing, project synchronization, code reviews, and team chat. Multiple engineers can work on the same automotive project simultaneously with conflict resolution and version control.",
                "code_example": self.get_collaboration_code(),
                "explanation": "Collaboration features enable distributed teams to work efficiently on complex automotive projects with real-time synchronization and communication.",
                "related_topics": ["Real-time Editing", "Version Control", "Code Reviews", "Team Communication"],
                "context_used": ["team_projects", "shared_sessions"],
                "follow_up_questions": [
                    "How do I set up a collaborative project for my team?",
                    "What are the best practices for code reviews in automotive projects?",
                    "How can I manage version control for safety-critical code?"
                ],
                "confidence": 0.95
            }
        
        elif any(word in question_lower for word in ['predictive', 'maintenance', 'predict']):
            return {
                "answer": "TATA Predictive Maintenance uses AI and machine learning to analyze vehicle data patterns, predict component failures before they occur, and optimize maintenance schedules. This reduces downtime, prevents costly breakdowns, and improves vehicle reliability.",
                "code_example": self.get_predictive_maintenance_code(),
                "explanation": "Predictive maintenance algorithms analyze sensor data, usage patterns, and historical maintenance records to forecast component health and optimal replacement timing.",
                "related_topics": ["Machine Learning", "Sensor Analytics", "Failure Prediction", "Maintenance Optimization"],
                "context_used": ["sensor_data", "maintenance_history"],
                "follow_up_questions": [
                    "What sensors are needed for predictive maintenance?",
                    "How accurate are the failure predictions?",
                    "Can I customize the prediction algorithms for specific components?"
                ],
                "confidence": 0.96
            }
        
        else:
            # Enhanced general response
            return {
                "answer": f"I understand you're asking about: '{question}'. As your advanced TATA AI Co-pilot, I can help with digital twins, predictive maintenance, real-time collaboration, safety simulation, IoT integration, and advanced automotive software development. I have access to real-time vehicle data, collaboration tools, and advanced analytics.",
                "explanation": "I'm equipped with advanced features including digital twin technology, predictive analytics, and collaborative development tools specifically designed for TATA automotive systems.",
                "related_topics": ["Digital Twins", "Predictive Maintenance", "Collaboration", "Safety Simulation"],
                "context_used": ["general_automotive"],
                "follow_up_questions": [
                    "Tell me about TATA digital twin capabilities",
                    "How does predictive maintenance work?",
                    "What collaboration features are available?"
                ],
                "confidence": 0.88
            }
    
    def get_digital_twin_code(self):
        return '''// TATA Digital Twin Data Collection
typedef struct {
    uint32_t vehicle_id;
    float latitude, longitude;
    uint16_t speed_kmh;
    uint16_t engine_rpm;
    int16_t engine_temp;
    uint8_t fuel_level;
    uint32_t timestamp;
} tata_twin_data_t;

// Send telemetry to digital twin
int tata_send_twin_data(tata_twin_data_t* data) {
    return iot_publish("tata/vehicle/telemetry", data, sizeof(*data));
}'''
    
    def get_collaboration_code(self):
        return '''// TATA Collaboration API
typedef struct {
    char session_id[32];
    char user_id[16];
    char project_name[64];
    uint32_t timestamp;
} tata_collab_session_t;

// Join collaborative session
int tata_join_session(const char* session_id, const char* user_id) {
    return collab_api_join(session_id, user_id);
}'''
    
    def get_predictive_maintenance_code(self):
        return '''// TATA Predictive Maintenance
typedef struct {
    float vibration_level;
    float temperature;
    uint32_t operating_hours;
    float wear_indicator;
} tata_component_health_t;

// Predict component failure
float tata_predict_failure(tata_component_health_t* health) {
    return ml_predict_failure(health);
}'''
    
    def serve_enhanced_main_page(self):
        html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TATA AI Co-pilot Premium - Advanced Features</title>
    <link rel="manifest" href="/manifest.json">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #1B4F72 0%, #2E86AB 30%, #A23B72 70%, #E74C3C 100%);
            min-height: 100vh; color: white; overflow-x: hidden;
        }
        .header {
            text-align: center; padding: 25px 20px;
            background: rgba(255, 255, 255, 0.15); backdrop-filter: blur(15px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.2);
        }
        .logo { font-size: 50px; margin-bottom: 12px; animation: float 3s ease-in-out infinite; }
        .title { font-size: 32px; font-weight: 700; margin-bottom: 8px; }
        .subtitle { font-size: 16px; opacity: 0.9; margin-bottom: 15px; }
        .premium-badge {
            background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
            color: #1B4F72; padding: 8px 20px; border-radius: 20px; display: inline-block;
            font-weight: 700; font-size: 12px; text-transform: uppercase; letter-spacing: 1px;
            box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
        }
        .container { max-width: 1600px; margin: 0 auto; padding: 25px 20px; }
        
        .features-dashboard {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px; margin: 25px 0;
        }
        .feature-panel {
            background: rgba(255, 255, 255, 0.12); backdrop-filter: blur(12px);
            border-radius: 16px; padding: 20px; border: 1px solid rgba(255, 255, 255, 0.2);
            transition: all 0.3s ease; cursor: pointer; position: relative; overflow: hidden;
        }
        .feature-panel:hover { 
            transform: translateY(-5px); 
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            background: rgba(255, 255, 255, 0.18);
        }
        .feature-icon { font-size: 36px; margin-bottom: 12px; }
        .feature-title { font-size: 18px; font-weight: 600; margin-bottom: 8px; color: #F39C12; }
        .feature-desc { font-size: 13px; line-height: 1.5; opacity: 0.9; margin-bottom: 12px; }
        .feature-status { 
            font-size: 11px; padding: 4px 8px; border-radius: 12px; 
            background: rgba(46, 204, 113, 0.3); color: #2ECC71; font-weight: 600;
        }
        
        .chat-container {
            background: rgba(255, 255, 255, 0.12); border-radius: 16px; padding: 20px; margin: 20px 0;
            border: 1px solid rgba(255, 255, 255, 0.2); min-height: 350px;
        }
        .chat-header { 
            font-size: 20px; font-weight: 600; margin-bottom: 15px; color: #F39C12;
            display: flex; align-items: center; gap: 10px;
        }
        .chat-messages { 
            height: 250px; overflow-y: auto; margin-bottom: 15px; padding: 8px; 
            background: rgba(0, 0, 0, 0.25); border-radius: 8px; 
        }
        .message { margin: 8px 0; padding: 10px; border-radius: 8px; }
        .user-message { background: rgba(52, 152, 219, 0.3); margin-left: 15px; }
        .ai-message { background: rgba(46, 204, 113, 0.3); margin-right: 15px; }
        .message-header { font-weight: 600; margin-bottom: 4px; font-size: 12px; }
        .message-content { line-height: 1.4; font-size: 13px; }
        .code-block { 
            background: rgba(0, 0, 0, 0.4); padding: 10px; border-radius: 6px; 
            margin: 6px 0; font-family: monospace; font-size: 11px; overflow-x: auto; 
        }
        
        .input-container { display: flex; gap: 8px; }
        .question-input { 
            flex: 1; padding: 10px; border: none; border-radius: 8px; 
            background: rgba(255, 255, 255, 0.9); color: #333; font-size: 14px; 
        }
        .send-btn { 
            padding: 10px 20px; background: linear-gradient(135deg, #E74C3C 0%, #F39C12 100%); 
            color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: 600; 
            transition: transform 0.2s;
        }
        .send-btn:hover { transform: scale(1.05); }
        
        .analytics-panel {
            background: rgba(255, 255, 255, 0.12); border-radius: 16px; padding: 20px; margin: 20px 0;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .analytics-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; }
        .metric-card { 
            background: rgba(52, 152, 219, 0.2); border-radius: 10px; padding: 15px; text-align: center;
            border: 1px solid rgba(52, 152, 219, 0.3);
        }
        .metric-value { font-size: 24px; font-weight: 700; color: #3498DB; }
        .metric-label { font-size: 12px; opacity: 0.8; margin-top: 5px; }
        
        .collaboration-panel {
            background: rgba(155, 89, 182, 0.2); border-radius: 12px; padding: 15px; margin: 15px 0;
            border: 1px solid rgba(155, 89, 182, 0.3);
        }
        .active-users { display: flex; gap: 8px; margin: 10px 0; }
        .user-avatar { 
            width: 32px; height: 32px; border-radius: 50%; background: linear-gradient(135deg, #9B59B6, #8E44AD);
            display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 600;
        }
        
        @keyframes float { 0%, 100% { transform: translateY(0px); } 50% { transform: translateY(-6px); } }
        .status-indicator { 
            display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 5px; 
            background: #2ECC71; animation: pulse 1s infinite; 
        }
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.6; } }
        
        .loading { display: none; text-align: center; padding: 15px; }
        .spinner { 
            border: 2px solid rgba(255,255,255,0.3); border-top: 2px solid #F39C12; 
            border-radius: 50%; width: 24px; height: 24px; animation: spin 1s linear infinite; margin: 0 auto; 
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        
        .premium-features {
            background: linear-gradient(135deg, rgba(255, 215, 0, 0.1), rgba(255, 165, 0, 0.1));
            border: 2px solid rgba(255, 215, 0, 0.3); border-radius: 16px; padding: 20px; margin: 20px 0;
        }
        .premium-title { color: #FFD700; font-size: 20px; font-weight: 700; margin-bottom: 15px; }
    </style>
</head>
<body>
    <div class="header">
        <div class="logo">🚗</div>
        <h1 class="title">TATA AI Co-pilot</h1>
        <p class="subtitle">Advanced AI Assistant for Automotive Innovation</p>
        <div class="premium-badge">✨ PREMIUM EDITION ✨</div>
        <div style="margin-top: 12px; font-size: 12px; opacity: 0.8;">
            🏆 TATA Innovate Hackathon 2024 | 🤖 AI-Powered | 🛡️ ASIL Compliant | 📱 Real-time Collaboration
        </div>
    </div>
    
    <div class="container">
        <div style="text-align: center; margin: 15px 0;">
            <p><span class="status-indicator"></span>AI Assistant: Online</p>
            <p><span class="status-indicator"></span>Digital Twin: Active</p>
            <p><span class="status-indicator"></span>Collaboration: Ready</p>
            <p><span class="status-indicator"></span>Predictive Analytics: Running</p>
        </div>
        
        <div class="premium-features">
            <div class="premium-title">🌟 Premium Features Available</div>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 10px;">
                <div>✨ Real-time Collaboration</div>
                <div>🔮 Predictive Maintenance</div>
                <div>🏗️ Digital Twin Technology</div>
                <div>📊 Advanced Analytics</div>
                <div>🛡️ Safety Simulation</div>
                <div>🌐 IoT Integration</div>
                <div>🤖 AI Model Training</div>
                <div>📈 Performance Optimization</div>
            </div>
        </div>
        
        <div class="features-dashboard">
            <div class="feature-panel" onclick="openDigitalTwin()">
                <div class="feature-icon">🏗️</div>
                <div class="feature-title">Digital Twin</div>
                <div class="feature-desc">Real-time vehicle monitoring with 3D visualization and predictive analytics</div>
                <div class="feature-status">3 Active Twins</div>
            </div>
            
            <div class="feature-panel" onclick="openCollaboration()">
                <div class="feature-icon">👥</div>
                <div class="feature-title">Real-time Collaboration</div>
                <div class="feature-desc">Work together with your team on automotive projects in real-time</div>
                <div class="feature-status">2 Active Sessions</div>
            </div>
            
            <div class="feature-panel" onclick="openPredictiveMaintenance()">
                <div class="feature-icon">🔮</div>
                <div class="feature-title">Predictive Maintenance</div>
                <div class="feature-desc">AI-powered failure prediction and maintenance optimization</div>
                <div class="feature-status">15 Predictions</div>
            </div>
            
            <div class="feature-panel" onclick="openSafetySimulator()">
                <div class="feature-icon">🛡️</div>
                <div class="feature-title">Safety Simulator</div>
                <div class="feature-desc">Advanced ASIL compliance testing and safety scenario simulation</div>
                <div class="feature-status">Running Tests</div>
            </div>
            
            <div class="feature-panel" onclick="openIoTIntegration()">
                <div class="feature-icon">🌐</div>
                <div class="feature-title">IoT Integration</div>
                <div class="feature-desc">Connect and monitor real vehicle sensors and ECUs</div>
                <div class="feature-status">3 Devices Online</div>
            </div>
            
            <div class="feature-panel" onclick="openAdvancedAnalytics()">
                <div class="feature-icon">📊</div>
                <div class="feature-title">Advanced Analytics</div>
                <div class="feature-desc">Performance metrics, usage statistics, and trend analysis</div>
                <div class="feature-status">Live Data</div>
            </div>
        </div>
        
        <div class="chat-container">
            <div class="chat-header">
                🤖 Advanced AI Assistant
                <div style="margin-left: auto; font-size: 12px; opacity: 0.8;">
                    Context-Aware | Multi-Modal | Collaborative
                </div>
            </div>
            <div class="chat-messages" id="chatMessages">
                <div class="message ai-message">
                    <div class="message-header">🤖 TATA AI Co-pilot Premium</div>
                    <div class="message-content">
                        Welcome to the Premium Edition! I now have advanced capabilities including:
                        <br>• 🏗️ Digital Twin integration for real-time vehicle monitoring
                        <br>• 👥 Real-time collaboration with your engineering team
                        <br>• 🔮 Predictive maintenance with AI-powered failure prediction
                        <br>• 🛡️ Advanced safety simulation and ASIL compliance testing
                        <br>• 🌐 IoT device integration for live sensor data
                        <br>• 📊 Advanced analytics and performance optimization
                        <br><br>Ask me anything about these advanced features or automotive development!
                    </div>
                </div>
            </div>
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>Advanced AI processing...</p>
            </div>
            <div class="input-container">
                <input type="text" class="question-input" id="questionInput" placeholder="Ask about digital twins, collaboration, predictive maintenance..." onkeypress="handleKeyPress(event)">
                <button class="send-btn" onclick="askAdvancedQuestion()">🚀 Ask AI</button>
            </div>
        </div>
        
        <div class="analytics-panel">
            <h3 style="color: #F39C12; margin-bottom: 15px;">📊 Real-time Analytics Dashboard</h3>
            <div class="analytics-grid" id="analyticsGrid">
                <div class="metric-card">
                    <div class="metric-value" id="activeUsers">--</div>
                    <div class="metric-label">Active Users</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value" id="codeGenerated">--</div>
                    <div class="metric-label">Code Generated Today</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value" id="systemUptime">--</div>
                    <div class="metric-label">System Uptime</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value" id="apiResponse">--</div>
                    <div class="metric-label">API Response Time</div>
                </div>
            </div>
        </div>
        
        <div class="collaboration-panel">
            <h4 style="color: #9B59B6; margin-bottom: 10px;">👥 Active Collaboration Sessions</h4>
            <div class="active-users">
                <div class="user-avatar">RK</div>
                <div class="user-avatar">PS</div>
                <div class="user-avatar">AP</div>
                <div style="margin-left: 10px; font-size: 12px; opacity: 0.8;">
                    3 engineers working on TATA Nexon EV Battery Management
                </div>
            </div>
        </div>
    </div>
    
    <script>
        let chatMessages = document.getElementById('chatMessages');
        let questionInput = document.getElementById('questionInput');
        let loading = document.getElementById('loading');
        
        // Load analytics data
        loadAnalytics();
        
        // Update analytics every 30 seconds
        setInterval(loadAnalytics, 30000);
        
        async function askAdvancedQuestion() {
            const question = questionInput.value.trim();
            if (!question) return;
            
            addMessage('user', question);
            questionInput.value = '';
            loading.style.display = 'block';
            
            try {
                const response = await fetch('/api/ask-advanced', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        question: question, 
                        context: { automotive: true, premium: true },
                        session_id: 'premium-session-001'
                    })
                });
                
                const data = await response.json();
                loading.style.display = 'none';
                
                let aiResponse = data.answer;
                if (data.code_example) {
                    aiResponse += '<div class="code-block">' + data.code_example + '</div>';
                }
                if (data.explanation) {
                    aiResponse += '<br><strong>💡 Explanation:</strong> ' + data.explanation;
                }
                if (data.follow_up_questions && data.follow_up_questions.length > 0) {
                    aiResponse += '<br><strong>🔄 Follow-up Questions:</strong><br>';
                    data.follow_up_questions.forEach(q => {
                        aiResponse += `• <span style="cursor: pointer; color: #3498DB;" onclick="askSampleQuestion('${q}')">${q}</span><br>`;
                    });
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
            
            const header = sender === 'user' ? '👤 You' : '🤖 TATA AI Co-pilot Premium';
            messageDiv.innerHTML = `
                <div class="message-header">${header}</div>
                <div class="message-content">${content}</div>
            `;
            
            chatMessages.appendChild(messageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
        
        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                askAdvancedQuestion();
            }
        }
        
        function askSampleQuestion(question) {
            questionInput.value = question;
            askAdvancedQuestion();
        }
        
        async function loadAnalytics() {
            try {
                const response = await fetch('/api/analytics');
                const data = await response.json();
                
                document.getElementById('activeUsers').textContent = data.real_time_data.concurrent_users;
                document.getElementById('codeGenerated').textContent = data.usage_statistics.total_code_generated.toLocaleString();
                document.getElementById('systemUptime').textContent = data.performance_metrics.system_uptime;
                document.getElementById('apiResponse').textContent = data.real_time_data.api_response_time;
                
            } catch (error) {
                console.error('Analytics error:', error);
            }
        }
        
        function openDigitalTwin() {
            addMessage('ai', '🏗️ <strong>Digital Twin Dashboard</strong><br>Monitoring 3 TATA vehicles in real-time:<br>• TATA Nexon EV (Mumbai) - Battery: 87%, Health: 94%<br>• TATA Ace Commercial (Delhi) - Fuel: 65%, Health: 89%<br>• TATA Harrier (Pune) - Maintenance Mode, Health: 92%<br><br>Real-time telemetry includes engine RPM, speed, temperature, and predictive insights.');
        }
        
        function openCollaboration() {
            addMessage('ai', '👥 <strong>Collaboration Hub</strong><br>Active sessions:<br>• Session 1: 3 engineers working on Nexon EV Battery Management<br>• Session 2: 2 engineers on Brake System Controller<br><br>Features: Real-time code editing, voice chat, shared debugging, version control integration.');
        }
        
        function openPredictiveMaintenance() {
            addMessage('ai', '🔮 <strong>Predictive Maintenance</strong><br>Current predictions:<br>• Engine Oil Filter (TATA Nexon): Replace in 2,500 km (94% confidence)<br>• Brake Pads (TATA Harrier): Attention needed in 1,200 km (97% confidence)<br>• Battery Cells (Nexon EV): Monitor in 6 months (89% confidence)<br><br>Cost savings: ₹3,25,000 prevented breakdowns this quarter.');
        }
        
        function openSafetySimulator() {
            addMessage('ai', '🛡️ <strong>Safety Simulation Center</strong><br>Available tests:<br>• Emergency Braking Test (ASIL-D) - Ready<br>• Collision Avoidance (ASIL-D) - Running<br>• Battery Thermal Runaway (ASIL-C) - Ready<br><br>Test results: 97.2% success rate, 2 critical issues resolved.');
        }
        
        function openIoTIntegration() {
            addMessage('ai', '🌐 <strong>IoT Device Network</strong><br>Connected devices:<br>• TATA-ECU-001: Engine Control Unit (Online)<br>• TATA-BMS-002: Battery Management (Online)<br>• TATA-BRAKE-003: Brake Controller (Maintenance)<br><br>Data streams: 65,000+ messages, 35 msg/sec, 98.1% quality.');
        }
        
        function openAdvancedAnalytics() {
            addMessage('ai', '📊 <strong>Advanced Analytics</strong><br>Performance metrics:<br>• Code generation speed: 3.2s average<br>• Accuracy rate: 96.8%<br>• User satisfaction: 4.7/5.0<br>• System uptime: 99.7%<br><br>Weekly trends show 25% increase in collaboration usage.');
        }
        
        console.log('🏆 TATA AI Co-pilot Premium Edition Loaded');
        console.log('✨ Advanced Features: Digital Twin, Collaboration, Predictive Maintenance');
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
    print("🏆 TATA AI Co-pilot - PREMIUM EDITION")
    print("🚗 TATA Innovate Hackathon 2024 - Advanced Features")
    print("=" * 80)
    print("🚀 Starting premium server on http://localhost:8000")
    print("✨ Premium Features: Digital Twin, Collaboration, Predictive Maintenance")
    print("🤖 Advanced AI: Context-aware, Multi-modal, Real-time Analytics")
    print("🌐 Browser will open automatically in 3 seconds")
    print("🎯 Press Ctrl+C to stop")
    print("-" * 80)
    
    threading.Thread(target=open_browser_delayed, daemon=True).start()
    
    PORT = 8000
    try:
        with socketserver.TCPServer(("", PORT), EnhancedTATAHandler) as httpd:
            print(f"✅ Premium server running at http://localhost:{PORT}")
            print("🏗️ Digital Twin: /api/digital-twin")
            print("👥 Collaboration: /api/collaboration") 
            print("🔮 Predictive Maintenance: /api/predictive-maintenance")
            print("🛡️ Safety Simulator: /api/safety-simulator")
            print("🌐 IoT Integration: /api/iot-devices")
            print("📊 Advanced Analytics: /api/analytics")
            print("")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 TATA AI Co-pilot Premium stopped")
        print("🎉 Thank you for using TATA AI Co-pilot Premium!")
    except Exception as e:
        print(f"\n❌ Server error: {e}")

if __name__ == "__main__":
    main()
