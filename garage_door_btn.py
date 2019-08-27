import RPi.GPIO as GPIO
import time
from pathlib import Path
import os
import sys

relay_signal = 4

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay_signal, GPIO.OUT)


# pulls the signal pin high signalling the relay switch to close
def garage_btn_down(pin):
    GPIO.output(pin, GPIO.HIGH)  # Close OSC


# pulls the signal pin low signalling the relay switch to open
def garage_btn_up(pin):
    GPIO.output(pin, GPIO.LOW)  # Open OSC


# presses the garage door button for 1 second
def press_button():
    garage_btn_down(relay_signal)
    time.sleep(1)
    garage_btn_up(relay_signal)


# returns true if garage_is_open status file exists
def garage_is_open():
    return os.path.exists('/home/pi/garage_is_open')


# returns true if garage_is_moving status file exists
def garage_is_moving():
    return os.path.exists('/home/pi/garage_is_moving')


# reverses the garage while in motion
def reverse_door():
    press_button()
    print("garage button pressed (stopping)")
    press_button()
    print("garage button pressed (reversing)")


# main entry point
if __name__ == '__main__':
    try:
        if "--open" in sys.argv:
            if not garage_is_open() and not garage_is_moving():
                press_button()
                print("garage button pressed (opening)")
                Path('/home/pi/garage_is_moving').touch()
            elif not garage_is_open() and garage_is_moving():
                reverse_door()
            else:
                print("ignoring since garage is already open or in transit")
        elif "--close" in sys.argv:
            if garage_is_open() and not garage_is_moving():
                Path('/home/pi/garage_is_moving').touch()
                press_button()
                print("garage button pressed (closing)")
            else:
                print("ignoring since garage is already closed or in transit")
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
