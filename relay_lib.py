"""A module for interacting with the ELEGOO 8 Channel board for the Raspberry Pi."""
# =========================================================
# Raspberry Pi Relay Board Library
#
# by John M. Wargo (www.johnwargo.com)
# https://gpiozero.readthedocs.io/en/stable/
#
# by G. Shaughnessy
# =========================================================

from __future__ import print_function

import time

# Try to import gpiod for Raspberry Pi 5 compatibility
try:
    import gpiod
    GPIO_AVAILABLE = True
    GPIO_LIBRARY = "gpiod"
    print("Using gpiod library for GPIO control")
except ImportError:
    try:
        from gpiozero import OutputDevice
        GPIO_AVAILABLE = True
        GPIO_LIBRARY = "gpiozero"
        print("Using gpiozero library for GPIO control")
    except ImportError:
        try:
            import RPi.GPIO as GPIO
            GPIO_AVAILABLE = True
            GPIO_LIBRARY = "RPi.GPIO"
            print("Using RPi.GPIO library for GPIO control")
            # Turn off GPIO warnings
            GPIO.setwarnings(False)
            # Set the GPIO numbering convention to be header pin numbers
            GPIO.setmode(GPIO.BOARD)
        except (ImportError, RuntimeError) as e:
            print("Warning: GPIO not available:", str(e))
            print("Running in simulation mode - GPIO operations will be logged only")
            GPIO_AVAILABLE = False
            GPIO_LIBRARY = "mock"

# The number of relay ports on the relay board.
# Updated to support 16 relays for Raspberry Pi 5
NUM_RELAY_PORTS = 16
RELAY_PORTS = ()
RELAY_STATUS = NUM_RELAY_PORTS * [0]
RELAY_DEVICES = []  # For gpiozero OutputDevice objects
GPIO_CHIP = None    # For gpiod chip object
GPIO_LINES = []     # For gpiod line objects

def cleanup_gpio():
    """Clean up GPIO resources"""
    global GPIO_LINES, RELAY_DEVICES
    try:
        if GPIO_LIBRARY == "gpiod" and GPIO_LINES:
            print("Cleaning up gpiod resources...")
            for line_request in GPIO_LINES:
                if line_request:
                    try:
                        line_request.release()
                        print("Released gpiod line request")
                    except Exception as e:
                        print(f"Error releasing line request: {e}")
            GPIO_LINES = []
            print("All gpiod lines released")
        elif GPIO_LIBRARY == "gpiozero" and RELAY_DEVICES:
            print("Cleaning up gpiozero resources...")
            for device in RELAY_DEVICES:
                if device:
                    try:
                        device.close()
                    except Exception as e:
                        print(f"Error closing device: {e}")
            RELAY_DEVICES = []
            print("All gpiozero devices closed")
    except Exception as e:
        print(f"Error during GPIO cleanup: {e}")

import atexit
import signal
import json
import os
atexit.register(cleanup_gpio)

# File to store relay states
RELAY_STATE_FILE = '/home/pi/pi-relay-controller-modmypi2025/relay_states.json'

# Also handle signals for proper cleanup
def signal_handler(signum, frame):
    print(f"Received signal {signum}, cleaning up...")
    cleanup_gpio()
    exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def sync_relay_status_with_gpio():
    """Sync the RELAY_STATUS array with actual GPIO pin states"""
    global RELAY_STATUS
    try:
        if GPIO_LIBRARY == "gpiod" and len(GPIO_LINES) > 0:
            line_request = GPIO_LINES[0]
            if line_request:
                print("Syncing relay status with actual GPIO states...")
                for i, gpio_pin in enumerate(RELAY_PORTS):
                    try:
                        # Read current GPIO value
                        current_value = line_request.get_value(gpio_pin)
                        # Convert GPIO value to relay status (remember: active low)
                        # INACTIVE (0) = Relay ON, ACTIVE (1) = Relay OFF
                        if current_value == gpiod.line.Value.INACTIVE:
                            RELAY_STATUS[i] = ON_STATE  # Relay is ON
                        else:
                            RELAY_STATUS[i] = OFF_STATE  # Relay is OFF
                        print(f"GPIO {gpio_pin} (Relay {i+1}): {current_value} -> Status: {RELAY_STATUS[i]}")
                    except Exception as e:
                        print(f"Could not read GPIO {gpio_pin}: {e}")
                        # Keep default status if can't read
                        pass
                print("Relay status sync completed")
        else:
            print("GPIO not available for status sync")
    except Exception as e:
        print(f"Error syncing relay status: {e}")

def get_relay_actual_status(relay_num):
    """Get the actual GPIO status of a specific relay"""
    try:
        if GPIO_LIBRARY == "gpiod" and len(GPIO_LINES) > 0:
            line_request = GPIO_LINES[0]
            if line_request and 0 < relay_num <= len(RELAY_PORTS):
                gpio_pin = RELAY_PORTS[relay_num - 1]
                current_value = line_request.get_value(gpio_pin)
                # Convert GPIO value to relay status (active low)
                if current_value == gpiod.line.Value.INACTIVE:
                    return ON_STATE  # Relay is ON
                else:
                    return OFF_STATE  # Relay is OFF
    except Exception as e:
        print(f"Error reading actual status for relay {relay_num}: {e}")

    # Fallback to stored status
    return RELAY_STATUS[relay_num - 1] if 0 < relay_num <= len(RELAY_STATUS) else OFF_STATE

def save_relay_states():
    """Save current relay states to file"""
    try:
        states = {}
        for i in range(NUM_RELAY_PORTS):
            states[f"relay_{i+1}"] = RELAY_STATUS[i]

        with open(RELAY_STATE_FILE, 'w') as f:
            json.dump(states, f, indent=2)
        print(f"Relay states saved to {RELAY_STATE_FILE}")
    except Exception as e:
        print(f"Error saving relay states: {e}")

def load_relay_states():
    """Load relay states from file"""
    try:
        if os.path.exists(RELAY_STATE_FILE):
            with open(RELAY_STATE_FILE, 'r') as f:
                states = json.load(f)
            print(f"Relay states loaded from {RELAY_STATE_FILE}")
            return states
        else:
            print("No saved relay states found")
            return {}
    except Exception as e:
        print(f"Error loading relay states: {e}")
        return {}

def restore_relay_states():
    """Restore relay states from saved file"""
    try:
        saved_states = load_relay_states()
        if saved_states:
            print("Restoring previous relay states...")
            for i in range(NUM_RELAY_PORTS):
                relay_key = f"relay_{i+1}"
                if relay_key in saved_states:
                    saved_state = saved_states[relay_key]
                    if saved_state == ON_STATE:
                        print(f"Restoring relay {i+1} to ON state")
                        relay_on(i+1)
                    else:
                        print(f"Restoring relay {i+1} to OFF state")
                        relay_off(i+1)
            print("Relay states restoration completed")
        else:
            print("No states to restore")
    except Exception as e:
        print(f"Error restoring relay states: {e}")

def reset_gpio_pins():
    """Reset GPIO pins if they are stuck"""
    try:
        import subprocess
        # Try to reset GPIO pins using gpioset
        for pin in [10, 12, 13, 14, 15, 6, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]:
            try:
                # Set pin to high (relay off for active-low relays)
                subprocess.run(['gpioset', 'gpiochip0', f'{pin}=1'],
                             timeout=1, capture_output=True)
            except:
                pass
        print("GPIO pins reset completed")
    except Exception as e:
        print(f"Could not reset GPIO pins: {e}")

# Some relay boards have a default on state with a low pin
ON_STATE = 0
OFF_STATE = 1 - ON_STATE

# Delay time between turning on next channels for `all_on` and `all_off` - for stability
DELAY_TIME = 0.2

def board_to_bcm_pin(board_pin):
    """Convert board pin number to BCM pin number for gpiozero

    Note: If the provided pins are already BCM numbers, this function
    will return them as-is if they're valid BCM pins.
    """
    # Mapping for Raspberry Pi board pins to BCM pins
    board_to_bcm = {
        3: 2, 5: 3, 7: 4, 8: 14, 10: 15, 11: 17, 12: 18, 13: 27,
        15: 22, 16: 23, 18: 24, 19: 10, 21: 9, 22: 25, 23: 11, 24: 8,
        26: 7, 29: 5, 31: 6, 32: 12, 33: 13, 35: 19, 36: 16, 37: 26,
        38: 20, 40: 21
    }

    # Check if it's a board pin first
    if board_pin in board_to_bcm:
        return board_to_bcm[board_pin]

    # If not found in board mapping, assume it's already a BCM pin
    # Valid BCM pins for Pi 5: 0-27
    if 0 <= board_pin <= 27:
        return board_pin

    return None

def init_relay(port_list):
    """Initialize the module

    Args:
        port_list: A list containing the relay port assignments (BCM pin numbers)
    """
    global RELAY_PORTS, RELAY_DEVICES, GPIO_CHIP, GPIO_LINES
    print("\nInitializing relay")
    print(f"Using {GPIO_LIBRARY} library")
    # Get the relay port list from the main application
    # assign the local variable with the value passed into init
    RELAY_PORTS = port_list
    print("Relay port list:", RELAY_PORTS)

    # setup the relay ports for output
    try:
        if GPIO_LIBRARY == "gpiod":
            # Use gpiod for Raspberry Pi 5 (modern approach)
            # gpiod 2.x uses different API - request all lines at once
            try:
                # Try to open the main GPIO chip
                chip_path = '/dev/gpiochip0'  # Primary GPIO chip

                # Create config for all GPIO lines at once
                config = {}
                for port in RELAY_PORTS:
                    config[port] = gpiod.LineSettings(
                        direction=gpiod.line.Direction.OUTPUT,
                        output_value=gpiod.line.Value.ACTIVE  # Start with relay OFF (active low)
                    )

                # Request all lines at once
                GPIO_LINES = [gpiod.request_lines(
                    chip_path,
                    consumer="relay_controller",
                    config=config
                )]

                print(f"Successfully initialized {len(RELAY_PORTS)} GPIO lines")

                # Read current GPIO states to sync with physical reality
                sync_relay_status_with_gpio()

                # Restore previous relay states
                restore_relay_states()

            except Exception as e:
                print(f"Failed to initialize gpiod: {e}")
                print("Attempting to reset GPIO pins...")
                reset_gpio_pins()

                # Try again after reset
                try:
                    time.sleep(1)  # Wait a bit
                    config = {}
                    for port in RELAY_PORTS:
                        config[port] = gpiod.LineSettings(
                            direction=gpiod.line.Direction.OUTPUT,
                            output_value=gpiod.line.Value.ACTIVE
                        )

                    GPIO_LINES = [gpiod.request_lines(
                        chip_path,
                        consumer="relay_controller",
                        config=config
                    )]

                    print(f"Successfully initialized {len(RELAY_PORTS)} GPIO lines after reset")

                except Exception as e2:
                    print(f"Failed to initialize gpiod even after reset: {e2}")
                    raise
        elif GPIO_LIBRARY == "gpiozero":
            # Use gpiozero fallback
            RELAY_DEVICES = []
            for port in RELAY_PORTS:
                try:
                    device = OutputDevice(port, active_high=False)  # Relay boards are usually active low
                    RELAY_DEVICES.append(device)
                    print(f"Initialized GPIO {port} with gpiozero")
                except Exception as e:
                    print(f"Failed to initialize GPIO {port}: {e}")
                    RELAY_DEVICES.append(None)
        elif GPIO_LIBRARY == "RPi.GPIO":
            # Use RPi.GPIO for older Pi models
            for relay in enumerate(RELAY_PORTS):
                GPIO.setup(relay[1], GPIO.OUT)

        # return true if the number of passed ports equals the number of ports
        return len(RELAY_PORTS) == NUM_RELAY_PORTS
    except Exception as e:
        print(f"GPIO setup failed: {e}")
        if not GPIO_AVAILABLE:
            print("Running in simulation mode")
            return len(RELAY_PORTS) == NUM_RELAY_PORTS
        else:
            raise


def relay_on(relay_num):
    """Turn the specified relay (by relay #) on.

    Call this function to turn a single relay on.

    Args:
        relay_num (int): The relay number that you want turned on.
    """
    if isinstance(relay_num, int):
        # do we have a valid relay number?
        if 0 < relay_num <= NUM_RELAY_PORTS:
            print('Turning relay', relay_num, 'ON')
            try:
                if GPIO_LIBRARY == "gpiod" and len(GPIO_LINES) > 0:
                    line_request = GPIO_LINES[0]  # We have one request object for all lines
                    if line_request:
                        # Turn on the relay (active low) - set to 0
                        line_request.set_value(RELAY_PORTS[relay_num - 1], gpiod.line.Value.INACTIVE)
                elif GPIO_LIBRARY == "gpiozero" and len(RELAY_DEVICES) >= relay_num:
                    device = RELAY_DEVICES[relay_num - 1]
                    if device:
                        device.on()  # Turn on the relay (active low)
                elif GPIO_LIBRARY == "RPi.GPIO":
                    GPIO.output(RELAY_PORTS[relay_num - 1], ON_STATE)
                else:
                    print(f"MOCK: Relay {relay_num} turned ON")

                # set the status for this relay to 'on'
                RELAY_STATUS[relay_num - 1] = ON_STATE
                # Save state to file
                save_relay_states()
            except Exception as e:
                print(f"GPIO error for relay {relay_num}: {e}")
                # In simulation mode, just update the status
                RELAY_STATUS[relay_num - 1] = ON_STATE
                save_relay_states()
        else:
            print('Invalid relay #:', relay_num)
    else:
        print('Relay number must be an Integer value')


def relay_off(relay_num):
    """Turn the specified relay (by relay #) off.

    Call this function to turn a single relay off.

    Args:
        relay_num (int): The relay number that you want turned off.
    """
    if isinstance(relay_num, int):
        # do we have a valid relay number?
        if 0 < relay_num <= NUM_RELAY_PORTS:
            print('Turning relay', relay_num, 'OFF')
            try:
                if GPIO_LIBRARY == "gpiod" and len(GPIO_LINES) > 0:
                    line_request = GPIO_LINES[0]  # We have one request object for all lines
                    if line_request:
                        # Turn off the relay (active low) - set to 1
                        line_request.set_value(RELAY_PORTS[relay_num - 1], gpiod.line.Value.ACTIVE)
                elif GPIO_LIBRARY == "gpiozero" and len(RELAY_DEVICES) >= relay_num:
                    device = RELAY_DEVICES[relay_num - 1]
                    if device:
                        device.off()  # Turn off the relay
                elif GPIO_LIBRARY == "RPi.GPIO":
                    GPIO.output(RELAY_PORTS[relay_num - 1], OFF_STATE)
                else:
                    print(f"MOCK: Relay {relay_num} turned OFF")

                # set the status for this relay to 'off'
                RELAY_STATUS[relay_num - 1] = OFF_STATE
                # Save state to file
                save_relay_states()
            except Exception as e:
                print(f"GPIO error for relay {relay_num}: {e}")
                # In simulation mode, just update the status
                RELAY_STATUS[relay_num - 1] = OFF_STATE
                save_relay_states()
        else:
            print('Invalid relay #:', relay_num)
    else:
        print('Relay number must be an Integer value')


def relay_all_on(relay_ports=RELAY_PORTS):
    """Turn all of the relays on.

     Call this function to turn all of the relays on.
     """
    print('Turning all relays ON')
    for i_relay, relay in enumerate(relay_ports):
        try:
            if GPIO_LIBRARY == "gpiod" and len(GPIO_LINES) > 0:
                line_request = GPIO_LINES[0]  # We have one request object for all lines
                if line_request:
                    line_request.set_value(relay, gpiod.line.Value.INACTIVE)  # Turn on the relay (active low)
            elif GPIO_LIBRARY == "gpiozero" and len(RELAY_DEVICES) > i_relay:
                device = RELAY_DEVICES[i_relay]
                if device:
                    device.on()  # Turn on the relay
            elif GPIO_LIBRARY == "RPi.GPIO":
                GPIO.output(relay, ON_STATE)
            else:
                print(f"MOCK: Relay {i_relay + 1} turned ON")

            RELAY_STATUS[i_relay] = ON_STATE
        except Exception as e:
            print(f"GPIO error for relay {i_relay + 1}: {e}")
            # In simulation mode, just update the status
            RELAY_STATUS[i_relay] = ON_STATE
        time.sleep(DELAY_TIME)


def relay_all_off(relay_ports=RELAY_PORTS):
    """Turn all of the relays off.

    Call this function to turn all of the relays off.
    """
    print('Turning all relays OFF')
    for i_relay, relay in enumerate(relay_ports):
        try:
            if GPIO_LIBRARY == "gpiod" and len(GPIO_LINES) > 0:
                line_request = GPIO_LINES[0]  # We have one request object for all lines
                if line_request:
                    line_request.set_value(relay, gpiod.line.Value.ACTIVE)  # Turn off the relay (active low)
            elif GPIO_LIBRARY == "gpiozero" and len(RELAY_DEVICES) > i_relay:
                device = RELAY_DEVICES[i_relay]
                if device:
                    device.off()  # Turn off the relay
            elif GPIO_LIBRARY == "RPi.GPIO":
                GPIO.output(relay, OFF_STATE)
            else:
                print(f"MOCK: Relay {i_relay + 1} turned OFF")

            # set the status for this relay to 'off'
            RELAY_STATUS[i_relay] = OFF_STATE
        except Exception as e:
            print(f"GPIO error for relay {i_relay + 1}: {e}")
            # In simulation mode, just update the status
            RELAY_STATUS[i_relay] = OFF_STATE
        time.sleep(DELAY_TIME)


def relay_toggle_port(relay_num):
    """Toggle the specified relay (on to off, or off to on).

    Call this function to toggle the status of a specific relay.

    Args:
        relay_num (int): The relay number to toggle.
    """
    print('Toggling relay:', relay_num)
    if relay_get_port_status(relay_num):
        # it's on, so turn it off
        relay_off(relay_num)
    else:
        # it's off, so turn it on
        relay_on(relay_num)


def relay_toggle_all_port(relay_num):
    """Toggle the specified relay (on to off, or off to on).

    Call this function to toggle the status of a specific relay.

    Args:
        relay_num (int): The relay number to toggle.
    """
    for i_relay, relay in enumerate(relay_ports):
        print('Toggling relay:', relay_num)
        if relay_get_port_status(relay_num):
            relay_off(relay_num)
        else:
            relay_on(relay_num)


def relay_get_port_status(relay_num):
    """Returns the status of the specified relay (True for on, False for off)

    Call this function to retrieve the status of a specific relay.

    Args:
        relay_num (int): The relay number to query.
    """
    # determines whether the specified port is ON/OFF
    print('Checking status of relay', relay_num)

    # Get actual GPIO status and update stored status
    actual_status = get_relay_actual_status(relay_num)
    if 0 < relay_num <= len(RELAY_STATUS):
        RELAY_STATUS[relay_num - 1] = actual_status

    return actual_status == ON_STATE
