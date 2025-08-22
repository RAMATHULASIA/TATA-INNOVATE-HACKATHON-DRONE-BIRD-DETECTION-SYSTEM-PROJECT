#include <stdio.h>
#include <stdlib.h>

// Problematic embedded code for demonstration
void unsafe_brake_control() {
    char large_buffer[2000];  // Too large for embedded stack
    int* dynamic_ptr = malloc(500);  // Dynamic allocation without null check
    
    printf("Brake system active\n");  // Not suitable for embedded/real-time
    
    while(1) {  // Infinite loop without yield - will starve other tasks
        // Process brake data
        if (dynamic_ptr[100] > 50) {  // Potential buffer overflow
            goto error_exit;  // MISRA C violation
        }
    }
    
    error_exit:
    // Missing free(dynamic_ptr) - memory leak
    return;
}

float calculate_brake_force(float pedal_position) {  // Floating point in embedded
    return pedal_position * 1.5;  // Magic number
}
