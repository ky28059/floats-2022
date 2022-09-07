import RPi.GPIO as GPIO
from constants import FORWARD_LS_PIN, BACKWARD_LS_PIN

GPIO.setmode(GPIO.BOARD)
GPIO.setup([FORWARD_LS_PIN, BACKWARD_LS_PIN], GPIO.IN)


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
