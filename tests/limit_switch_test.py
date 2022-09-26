import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import RPi.GPIO as GPIO
from constants import FORWARD_LS_PIN, BACKWARD_LS_PIN

GPIO.setmode(GPIO.BCM)
GPIO.setup([FORWARD_LS_PIN, BACKWARD_LS_PIN], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


# Logs a detected edge on the given channel.
def report_edge(channel):
    print(f"Rising edge detected on channel {channel}.")


if __name__ == '__main__':
    print(f"Setting up listeners on pins {FORWARD_LS_PIN}, {BACKWARD_LS_PIN}.")
    GPIO.add_event_detect(FORWARD_LS_PIN, GPIO.RISING, callback=report_edge)
    GPIO.add_event_detect(BACKWARD_LS_PIN, GPIO.RISING, callback=report_edge)
    try:
        while True:
            pass
    except KeyboardInterrupt:
        GPIO.cleanup()
