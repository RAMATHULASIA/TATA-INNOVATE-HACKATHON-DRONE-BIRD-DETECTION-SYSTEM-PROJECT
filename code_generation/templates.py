"""
Template manager for code generation
"""

from typing import Dict, List, Optional, Any
from pathlib import Path


class TemplateManager:
    """
    Manages code templates for different embedded systems patterns
    """
    
    def __init__(self):
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict[str, str]:
        """Load predefined code templates"""
        return {
            "can_driver": '''
#include <stdint.h>
#include <stdbool.h>

typedef struct {
    uint32_t id;
    uint8_t dlc;
    uint8_t data[8];
} can_message_t;

bool can_init(uint32_t baudrate) {
    // Initialize CAN peripheral
    // Configure filters
    // Enable interrupts
    return true;
}

bool can_transmit(const can_message_t* msg) {
    if (msg == NULL || msg->dlc > 8) {
        return false;
    }
    
    // Transmit message
    return true;
}

bool can_receive(can_message_t* msg) {
    if (msg == NULL) {
        return false;
    }
    
    // Receive message
    return true;
}
''',
            
            "interrupt_handler": '''
#include <stdint.h>
#include <stdbool.h>

// Interrupt service routine template
void __attribute__((interrupt)) timer_isr(void) {
    // Clear interrupt flag
    
    // Minimal processing in ISR
    // Set flags for main loop processing
    
    // Re-enable interrupts if needed
}

// Main loop processing
void process_timer_event(void) {
    // Process timer event in main context
    // Perform time-consuming operations here
}
''',
            
            "state_machine": '''
#include <stdint.h>
#include <stdbool.h>

typedef enum {
    STATE_INIT,
    STATE_IDLE,
    STATE_ACTIVE,
    STATE_ERROR,
    STATE_MAX
} system_state_t;

typedef struct {
    system_state_t current_state;
    system_state_t previous_state;
    uint32_t state_entry_time;
} state_machine_t;

static state_machine_t sm = {STATE_INIT, STATE_INIT, 0};

void state_machine_init(void) {
    sm.current_state = STATE_INIT;
    sm.previous_state = STATE_INIT;
    sm.state_entry_time = get_system_time();
}

void state_machine_update(void) {
    system_state_t next_state = sm.current_state;
    
    switch (sm.current_state) {
        case STATE_INIT:
            // Initialization logic
            next_state = STATE_IDLE;
            break;
            
        case STATE_IDLE:
            // Idle state logic
            break;
            
        case STATE_ACTIVE:
            // Active state logic
            break;
            
        case STATE_ERROR:
            // Error handling logic
            break;
            
        default:
            next_state = STATE_ERROR;
            break;
    }
    
    // State transition
    if (next_state != sm.current_state) {
        sm.previous_state = sm.current_state;
        sm.current_state = next_state;
        sm.state_entry_time = get_system_time();
    }
}
''',
            
            "circular_buffer": '''
#include <stdint.h>
#include <stdbool.h>

#define BUFFER_SIZE 64

typedef struct {
    uint8_t buffer[BUFFER_SIZE];
    uint16_t head;
    uint16_t tail;
    uint16_t count;
} circular_buffer_t;

void buffer_init(circular_buffer_t* cb) {
    if (cb == NULL) return;
    
    cb->head = 0;
    cb->tail = 0;
    cb->count = 0;
}

bool buffer_put(circular_buffer_t* cb, uint8_t data) {
    if (cb == NULL || cb->count >= BUFFER_SIZE) {
        return false;
    }
    
    cb->buffer[cb->head] = data;
    cb->head = (cb->head + 1) % BUFFER_SIZE;
    cb->count++;
    
    return true;
}

bool buffer_get(circular_buffer_t* cb, uint8_t* data) {
    if (cb == NULL || data == NULL || cb->count == 0) {
        return false;
    }
    
    *data = cb->buffer[cb->tail];
    cb->tail = (cb->tail + 1) % BUFFER_SIZE;
    cb->count--;
    
    return true;
}

bool buffer_is_empty(const circular_buffer_t* cb) {
    return (cb != NULL) ? (cb->count == 0) : true;
}

bool buffer_is_full(const circular_buffer_t* cb) {
    return (cb != NULL) ? (cb->count >= BUFFER_SIZE) : true;
}
'''
        }
    
    def get_template(self, template_name: str) -> Optional[str]:
        """Get a template by name"""
        return self.templates.get(template_name)
    
    def list_templates(self) -> List[str]:
        """List available template names"""
        return list(self.templates.keys())
    
    def add_template(self, name: str, template: str) -> None:
        """Add a new template"""
        self.templates[name] = template
    
    def customize_template(self, template_name: str, replacements: Dict[str, str]) -> Optional[str]:
        """Customize a template with replacements"""
        template = self.get_template(template_name)
        if template is None:
            return None
        
        customized = template
        for placeholder, replacement in replacements.items():
            customized = customized.replace(f"{{{placeholder}}}", replacement)
        
        return customized
