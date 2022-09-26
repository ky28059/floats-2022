import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import time
import RPi.GPIO as GPIO
from constants import FM_RELAY_PIN, LED_RELAY_PIN

GPIO.setmode(GPIO.BCM)
GPIO.setup([FM_RELAY_PIN, LED_RELAY_PIN], GPIO.OUT)

if __name__ == '__main__':
    print(f"Starting relay on pins {FM_RELAY_PIN} and {LED_RELAY_PIN}.")
    GPIO.output([FM_RELAY_PIN, LED_RELAY_PIN], GPIO.HIGH)
    time.sleep(5)

    print("Stopping relays.")
    GPIO.output([FM_RELAY_PIN, LED_RELAY_PIN], GPIO.LOW)
    GPIO.cleanup()
