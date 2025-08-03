#!/usr/bin/env python3
"""
GPIO Reset Script for Raspberry Pi 5
This script resets all GPIO pins used by the relay controller
"""

import subprocess
import time
import sys

# GPIO pins used by the relay controller
GPIO_PINS = [10, 12, 13, 14, 15, 6, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]

def reset_gpio_with_gpioset():
    """Reset GPIO pins using gpioset command"""
    print("Resetting GPIO pins using gpioset...")
    for pin in GPIO_PINS:
        try:
            # Set pin to high (relay off for active-low relays)
            result = subprocess.run(['gpioset', 'gpiochip0', f'{pin}=1'], 
                                  timeout=2, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"Reset GPIO {pin}")
            else:
                print(f"Failed to reset GPIO {pin}: {result.stderr}")
        except subprocess.TimeoutExpired:
            print(f"Timeout resetting GPIO {pin}")
        except Exception as e:
            print(f"Error resetting GPIO {pin}: {e}")

def reset_gpio_with_gpiod():
    """Reset GPIO pins using gpiod library"""
    try:
        import gpiod
        print("Resetting GPIO pins using gpiod...")
        
        chip_path = '/dev/gpiochip0'
        config = {}
        for pin in GPIO_PINS:
            config[pin] = gpiod.LineSettings(
                direction=gpiod.line.Direction.OUTPUT,
                output_value=gpiod.line.Value.ACTIVE  # High = relay off
            )
        
        try:
            line_request = gpiod.request_lines(
                chip_path,
                consumer="gpio_reset",
                config=config
            )
            print("Successfully reset all GPIO pins with gpiod")
            time.sleep(0.1)
            line_request.release()
            print("Released GPIO lines")
        except Exception as e:
            print(f"Failed to reset with gpiod: {e}")
            
    except ImportError:
        print("gpiod library not available")

def main():
    print("GPIO Reset Tool for Relay Controller")
    print("====================================")
    
    # Try both methods
    reset_gpio_with_gpioset()
    time.sleep(1)
    reset_gpio_with_gpiod()
    
    print("GPIO reset completed")

if __name__ == "__main__":
    main()
