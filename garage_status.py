import RPi.GPIO as GPIO
import time
import os
from pathlib import Path

GPIO.setmode(GPIO.BCM)

# photo resistor pin 1
open_led = 17

# photo resistor pin 2
close_led = 27


def rc_time(pin):
    count = 0

    # Output on the pin
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(0.1)

    # Change the pin back to input
    GPIO.setup(pin, GPIO.IN)

    # Count until the pin goes high
    while GPIO.input(pin) == GPIO.LOW:
        count += 1
    return count


try:
    # Main loop
    while True:
        open_led_lux = rc_time(open_led)
        close_led_lux = rc_time(close_led)

        print('open_led_lux=', open_led_lux)
        print('close_led_lux=', close_led_lux)

        # It's only when the open led is lit that the garage is neither closed or in transit.
        if open_led_lux < 800:
            print('door open led is lit:', open_led_lux)
            Path('/home/pi/garage_is_open').touch()
            if os.path.exists('/home/pi/garage_is_moving'):
                os.remove("/home/pi/garage_is_moving")

        # It's only when the closed led is lit that the garage is neither open or in transit.
        if close_led_lux < 200:
            print('door closed is lit:', close_led_lux)
            if os.path.exists('/home/pi/garage_is_open'):
                os.remove("/home/pi/garage_is_open")
            if os.path.exists('/home/pi/garage_is_moving'):
                os.remove("/home/pi/garage_is_moving")

        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
