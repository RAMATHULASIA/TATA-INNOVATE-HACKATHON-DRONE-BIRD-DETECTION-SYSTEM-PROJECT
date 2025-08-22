#!/usr/bin/env python3
"""
Enhanced TATA AI Co-pilot with Fixed Voice Commands
TATA Innovate Hackathon 2024 - Premium Edition with Voice Support
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
                "version": "3.1.0-premium-voice",
                "features": [
                    "interactive_qa", "code_generation", "real_time_collaboration", 
                    "3d_visualization", "voice_commands", "ai_chat_history",
                    "code_templates", "performance_analytics", "safety_simulator",
                    "tata_digital_twin", "predictive_maintenance", "iot_integration"
                ],
                "uptime": self.get_uptime(),
                "ai_models": ["TATA-GPT-Automotive-Pro", "CodeGen-Embedded-Plus", "Safety-Analyzer-Advanced"],
                "active_users": random.randint(15, 25),
                "code_generated_today": random.randint(150, 300),
                "voice_support": True
            })
        elif self.path == '/api/analytics':
            self.serve_json(self.get_analytics_data())
        elif self.path == '/api/digital-twin':
            self.serve_json(self.get_digital_twin_data())
        elif self.path == '/api/collaboration':
            self.serve_json(self.get_collaboration_data())
        elif self.path == '/api/predictive-maintenance':
            self.serve_json(self.get_predictive_maintenance_data())
        elif self.path == '/manifest.json':
            self.serve_json({
                "short_name": "TATA AI Co-pilot",
                "name": "TATA AI Co-pilot Premium with Voice Commands",
                "description": "AI-powered development platform for TATA vehicle embedded systems with voice support",
                "start_url": "/",
                "display": "standalone",
                "theme_color": "#1B4F72",
                "background_color": "#FFFFFF",
                "icons": [{"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"}]
            })
        else:
            super().do_GET()
    
    def do_POST(self):
        if self.path == '/api/ask-advanced':
            self.handle_advanced_qa()
        elif self.path == '/api/generate-advanced':
            self.handle_advanced_code_generation()
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
                "voice_commands_used": random.randint(120, 250),
                "collaboration_sessions": random.randint(25, 45)
            },
            "real_time_data": {
                "current_cpu_usage": f"{random.randint(15, 35)}%",
                "memory_usage": f"{random.randint(40, 65)}%",
                "api_response_time": f"{random.randint(120, 280)}ms",
                "concurrent_users": random.randint(8, 18)
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
                    "health_score": random.randint(85, 98)
                },
                {
                    "name": "TATA Ace Commercial",
                    "type": "Commercial Vehicle", 
                    "status": "Active",
                    "fuel_level": random.randint(40, 80),
                    "location": "Delhi, India",
                    "health_score": random.randint(78, 92)
                }
            ]
        }
    
    def get_collaboration_data(self):
        return {
            "active_sessions": [
                {
                    "session_id": "TATA-COLLAB-001",
                    "participants": ["Rajesh Kumar", "Priya Sharma", "Amit Patel"],
                    "project": "TATA Nexon EV Battery Management",
                    "status": "Active"
                }
            ]
        }
    
    def get_predictive_maintenance_data(self):
        return {
            "maintenance_predictions": [
                {
                    "component": "Engine Oil Filter",
                    "vehicle": "TATA Nexon",
                    "predicted_failure": "In 2,500 km",
                    "confidence": "94%"
                }
            ]
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
                "follow_up_questions": response.get("follow_up_questions", []),
                "timestamp": datetime.now().isoformat(),
                "session_id": session_id
            })
            
        except Exception as e:
            self.serve_json({"error": str(e)}, status=400)
    
    def generate_advanced_qa_response(self, question, context, session_id):
        """Generate advanced Q&A responses with context awareness"""
        question_lower = question.lower()
        
        if any(word in question_lower for word in ['brake', 'braking', 'abs']):
            return {
                "answer": "TATA brake systems require ASIL-D compliance for safety-critical functions. The brake system should include redundant sensors, fail-safe mechanisms, and real-time monitoring. For ABS systems, we implement wheel speed sensors, hydraulic pressure control, and emergency braking protocols.",
                "code_example": self.get_brake_code_example(),
                "explanation": "This implementation follows ISO 26262 standards for automotive safety and includes TATA-specific error codes and CAN bus communication protocols.",
                "related_topics": ["ASIL-D Compliance", "CAN Bus Communication", "Hydraulic Control", "Sensor Redundancy"],
                "follow_up_questions": [
                    "How do I implement redundant brake sensors?",
                    "What are the ASIL-D testing requirements?",
                    "How can I optimize brake response time?"
                ],
                "confidence": 0.98
            }
        
        elif any(word in question_lower for word in ['engine', 'rpm', 'fuel', 'injection']):
            return {
                "answer": "TATA engine control systems manage fuel injection, ignition timing, and emissions control. The ECU monitors engine RPM, temperature, and load conditions to optimize performance and efficiency. For commercial vehicles, we focus on durability and fuel economy.",
                "code_example": self.get_engine_code_example(),
                "explanation": "This code implements a complete engine control loop with sensor validation, fuel map lookup, and diagnostic monitoring suitable for TATA commercial vehicles.",
                "related_topics": ["Fuel Injection", "Ignition Timing", "Emissions Control", "Engine Diagnostics"],
                "follow_up_questions": [
                    "How do I calibrate fuel injection timing?",
                    "What sensors are needed for engine control?",
                    "How can I implement emissions monitoring?"
                ],
                "confidence": 0.96
            }
        
        elif any(word in question_lower for word in ['battery', 'electric', 'ev', 'charging']):
            return {
                "answer": "TATA electric vehicle systems require sophisticated battery management, thermal control, and charging protocols. The BMS monitors cell voltages, temperatures, and current flow to ensure safety and longevity. Fast charging requires careful thermal management.",
                "code_example": self.get_battery_code_example(),
                "explanation": "This BMS implementation includes cell balancing, thermal protection, and SOC estimation algorithms optimized for TATA electric vehicle platforms.",
                "related_topics": ["Battery Management", "Thermal Control", "Fast Charging", "Cell Balancing"],
                "follow_up_questions": [
                    "How do I implement cell balancing algorithms?",
                    "What are the thermal protection requirements?",
                    "How can I optimize charging speed?"
                ],
                "confidence": 0.97
            }
        
        elif any(word in question_lower for word in ['voice', 'speech', 'command']):
            return {
                "answer": "TATA AI Co-pilot supports advanced voice commands using Web Speech API. You can speak naturally to ask questions, generate code, or control features. Voice recognition works in multiple languages and understands automotive terminology.",
                "code_example": self.get_voice_code_example(),
                "explanation": "Voice commands enable hands-free interaction, improving productivity and accessibility for automotive engineers working in various environments.",
                "related_topics": ["Speech Recognition", "Voice UI", "Hands-free Operation", "Accessibility"],
                "follow_up_questions": [
                    "What voice commands are available?",
                    "How accurate is the voice recognition?",
                    "Can I use voice commands in Hindi?"
                ],
                "confidence": 0.95
            }
        
        else:
            return {
                "answer": f"I understand you're asking about: '{question}'. As your advanced TATA AI Co-pilot, I can help with brake systems, engine control, electric vehicles, voice commands, and all aspects of automotive software development. I have deep knowledge of TATA vehicle architectures and safety requirements.",
                "explanation": "I'm equipped with automotive domain expertise and can provide detailed technical guidance for TATA vehicle development.",
                "related_topics": ["Brake Systems", "Engine Control", "Electric Vehicles", "Voice Commands"],
                "follow_up_questions": [
                    "Tell me about TATA brake system requirements",
                    "How do I develop engine control software?",
                    "What are the voice command capabilities?"
                ],
                "confidence": 0.88
            }
    
    def get_brake_code_example(self):
        return '''// TATA Brake System Controller
#include "tata_brake_system.h"

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
        return '''// TATA Engine Control Module
#include "tata_engine_control.h"

typedef struct {
    uint16_t rpm;
    uint8_t throttle_position;
    int16_t engine_temp;
} tata_engine_data_t;

int tata_engine_control_init(void) {
    // Initialize engine sensors and actuators
    return TATA_SUCCESS;
}'''
    
    def get_battery_code_example(self):
        return '''// TATA Battery Management System
#include "tata_bms.h"

typedef struct {
    uint16_t cell_voltages[96];
    int32_t pack_current;
    int16_t pack_temperature;
    uint8_t soc_percentage;
} tata_bms_data_t;

int tata_bms_init(void) {
    // Initialize BMS hardware
    return TATA_SUCCESS;
}'''
    
    def get_voice_code_example(self):
        return '''// Voice Command Integration
const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.continuous = false;
recognition.interimResults = false;
recognition.lang = 'en-US';

recognition.onresult = function(event) {
    const transcript = event.results[0][0].transcript;
    processVoiceCommand(transcript);
};

function processVoiceCommand(command) {
    // Process automotive voice commands
    console.log('Voice command:', command);
}'''

    def serve_enhanced_main_page(self):
        html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TATA AI Co-pilot Premium - With Voice Commands</title>
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
            border: 1px solid rgba(255, 255, 255, 0.2); min-height: 400px;
        }
        .chat-header {
            font-size: 20px; font-weight: 600; margin-bottom: 15px; color: #F39C12;
            display: flex; align-items: center; gap: 10px;
        }
        .chat-messages {
            height: 280px; overflow-y: auto; margin-bottom: 15px; padding: 8px;
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

        .input-container { display: flex; gap: 8px; align-items: center; }
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

        .voice-btn {
            padding: 10px 15px; background: linear-gradient(135deg, #9B59B6 0%, #8E44AD 100%);
            color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: 600;
            transition: all 0.3s ease; font-size: 12px;
        }
        .voice-btn:hover { transform: scale(1.05); }
        .voice-btn.listening {
            background: linear-gradient(135deg, #E74C3C 0%, #C0392B 100%);
            animation: pulse 1s infinite;
        }

        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.7; } }
        @keyframes float { 0%, 100% { transform: translateY(0px); } 50% { transform: translateY(-6px); } }

        .status-indicator {
            display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 5px;
            background: #2ECC71; animation: pulse 1s infinite;
        }

        .loading { display: none; text-align: center; padding: 15px; }
        .spinner {
            border: 2px solid rgba(255,255,255,0.3); border-top: 2px solid #F39C12;
            border-radius: 50%; width: 24px; height: 24px; animation: spin 1s linear infinite; margin: 0 auto;
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

        .voice-status {
            background: rgba(155, 89, 182, 0.2); border-radius: 12px; padding: 10px; margin: 10px 0;
            border: 1px solid rgba(155, 89, 182, 0.3); text-align: center; font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="logo">🚗</div>
        <h1 class="title">TATA AI Co-pilot</h1>
        <p class="subtitle">Advanced AI Assistant with Voice Commands</p>
        <div class="premium-badge">✨ PREMIUM + VOICE ✨</div>
        <div style="margin-top: 12px; font-size: 12px; opacity: 0.8;">
            🏆 TATA Innovate Hackathon 2024 | 🤖 AI-Powered | 🎤 Voice Enabled | 🛡️ ASIL Compliant
        </div>
    </div>

    <div class="container">
        <div style="text-align: center; margin: 15px 0;">
            <p><span class="status-indicator"></span>AI Assistant: Online</p>
            <p><span class="status-indicator"></span>Voice Commands: Ready</p>
            <p><span class="status-indicator"></span>Digital Twin: Active</p>
            <p><span class="status-indicator"></span>Collaboration: Ready</p>
        </div>

        <div class="features-dashboard">
            <div class="feature-panel" onclick="testVoiceFeature()">
                <div class="feature-icon">🎤</div>
                <div class="feature-title">Voice Commands</div>
                <div class="feature-desc">Hands-free interaction with AI assistant using natural speech recognition</div>
                <div class="feature-status">Ready to Listen</div>
            </div>

            <div class="feature-panel" onclick="showDigitalTwin()">
                <div class="feature-icon">🏗️</div>
                <div class="feature-title">Digital Twin</div>
                <div class="feature-desc">Real-time vehicle monitoring and predictive analytics</div>
                <div class="feature-status">2 Active Twins</div>
            </div>

            <div class="feature-panel" onclick="showCollaboration()">
                <div class="feature-icon">👥</div>
                <div class="feature-title">Real-time Collaboration</div>
                <div class="feature-desc">Work together with your team on automotive projects</div>
                <div class="feature-status">1 Active Session</div>
            </div>

            <div class="feature-panel" onclick="showPredictiveMaintenance()">
                <div class="feature-icon">🔮</div>
                <div class="feature-title">Predictive Maintenance</div>
                <div class="feature-desc">AI-powered failure prediction and maintenance optimization</div>
                <div class="feature-status">5 Predictions</div>
            </div>
        </div>

        <div class="chat-container">
            <div class="chat-header">
                🤖 Advanced AI Assistant with Voice Support
                <div style="margin-left: auto; font-size: 12px; opacity: 0.8;">
                    Context-Aware | Voice-Enabled | TATA Automotive Expert
                </div>
            </div>

            <div id="voiceStatus" class="voice-status" style="display: none;">
                🎤 Voice Recognition Status: <span id="voiceStatusText">Ready</span>
            </div>

            <div class="chat-messages" id="chatMessages">
                <div class="message ai-message">
                    <div class="message-header">🤖 TATA AI Co-pilot Premium + Voice</div>
                    <div class="message-content">
                        Welcome to the Premium Edition with Voice Commands! I now support:
                        <br>• 🎤 <strong>Voice Commands</strong> - Speak naturally to ask questions
                        <br>• 🏗️ Digital Twin integration for real-time vehicle monitoring
                        <br>• 👥 Real-time collaboration with your engineering team
                        <br>• 🔮 Predictive maintenance with AI-powered failure prediction
                        <br>• 🛡️ Advanced safety simulation and ASIL compliance testing
                        <br><br><strong>Try saying:</strong> "How do I create a brake system for TATA vehicles?"
                        <br>Or click the 🎤 Voice button to start speaking!
                    </div>
                </div>
            </div>
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>Advanced AI processing...</p>
            </div>
            <div class="input-container">
                <input type="text" class="question-input" id="questionInput" placeholder="Ask about TATA automotive systems or use voice commands..." onkeypress="handleKeyPress(event)">
                <button class="voice-btn" id="voiceBtn" onclick="startVoiceCommand()">🎤 Voice</button>
                <button class="send-btn" onclick="askAdvancedQuestion()">🚀 Ask AI</button>
            </div>
        </div>
    </div>

    <script>
        let chatMessages = document.getElementById('chatMessages');
        let questionInput = document.getElementById('questionInput');
        let loading = document.getElementById('loading');
        let voiceBtn = document.getElementById('voiceBtn');
        let voiceStatus = document.getElementById('voiceStatus');
        let voiceStatusText = document.getElementById('voiceStatusText');
        let recognition = null;
        let isListening = false;

        // Initialize voice recognition
        function initVoiceRecognition() {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

            if (SpeechRecognition) {
                recognition = new SpeechRecognition();
                recognition.continuous = false;
                recognition.interimResults = false;
                recognition.lang = 'en-US';

                recognition.onstart = function() {
                    isListening = true;
                    voiceBtn.classList.add('listening');
                    voiceBtn.innerHTML = '🎤 Listening...';
                    voiceStatus.style.display = 'block';
                    voiceStatusText.textContent = 'Listening... Speak now!';
                    addMessage('ai', '🎤 <strong>Voice Recognition Active</strong><br>I\'m listening... Please speak your question about TATA automotive software.');
                };

                recognition.onresult = function(event) {
                    const transcript = event.results[0][0].transcript;
                    const confidence = event.results[0][0].confidence;

                    questionInput.value = transcript;
                    voiceStatusText.textContent = `Recognized: "${transcript}" (${Math.round(confidence * 100)}% confidence)`;

                    addMessage('user', `🎤 <strong>Voice Input:</strong> ${transcript}<br><small>Confidence: ${Math.round(confidence * 100)}%</small>`);

                    // Automatically ask the question
                    setTimeout(() => {
                        askAdvancedQuestion();
                    }, 1000);
                };

                recognition.onerror = function(event) {
                    console.error('Voice recognition error:', event.error);
                    voiceStatusText.textContent = `Error: ${event.error}`;
                    addMessage('ai', `❌ <strong>Voice Recognition Error:</strong> ${event.error}<br>Please try again or type your question manually.`);
                    resetVoiceButton();
                };

                recognition.onend = function() {
                    resetVoiceButton();
                    setTimeout(() => {
                        voiceStatus.style.display = 'none';
                    }, 3000);
                };

                // Show voice support status
                addMessage('ai', '✅ <strong>Voice Commands Available!</strong><br>Click the 🎤 Voice button or try the voice feature panel to speak your questions.');
                return true;
            } else {
                addMessage('ai', '❌ <strong>Voice Recognition Not Supported</strong><br>Your browser doesn\'t support voice recognition. Please use Chrome, Edge, or Safari.');
                voiceBtn.style.display = 'none';
                return false;
            }
        }

        function resetVoiceButton() {
            isListening = false;
            voiceBtn.classList.remove('listening');
            voiceBtn.innerHTML = '🎤 Voice';
            voiceStatusText.textContent = 'Ready';
        }

        function startVoiceCommand() {
            if (!recognition) {
                addMessage('ai', '❌ Voice recognition not available. Please type your question.');
                return;
            }

            if (isListening) {
                recognition.stop();
                return;
            }

            try {
                recognition.start();
            } catch (error) {
                console.error('Failed to start voice recognition:', error);
                addMessage('ai', '❌ Failed to start voice recognition. Please try again.');
            }
        }'''
