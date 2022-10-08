import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import pigpio
from constants import FORWARD_LS_PIN, BACKWARD_LS_PIN

GPIO = pigpio.pi()
GPIO.set_mode(FORWARD_LS_PIN, pigpio.INPUT)
GPIO.set_mode(BACKWARD_LS_PIN, pigpio.INPUT)

GPIO.set_pull_up_down(FORWARD_LS_PIN, pigpio.PUD_DOWN)
GPIO.set_pull_up_down(BACKWARD_LS_PIN, pigpio.PUD_DOWN)


# Logs a detected edge on the given channel.
def report_edge(channel, level, tick):
    edge = 'Rising edge' if level == 1 else 'Falling edge' if level == 0 else 'Timeout'
    print(f"{edge} detected on channel {channel}.")


if __name__ == '__main__':
    print(f"Setting up listeners on pins {FORWARD_LS_PIN}, {BACKWARD_LS_PIN}.")
    GPIO.callback(FORWARD_LS_PIN, pigpio.RISING_EDGE, report_edge)
    GPIO.callback(BACKWARD_LS_PIN, pigpio.RISING_EDGE, report_edge)
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Test finished, cleaning up.")
        GPIO.stop()
