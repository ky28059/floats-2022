import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import time
import pigpio
from constants import FM_RELAY_PIN, LED_RELAY_PIN

GPIO = pigpio.pi()
GPIO.set_mode(FM_RELAY_PIN, pigpio.OUTPUT)
GPIO.set_mode(LED_RELAY_PIN, pigpio.OUTPUT)

if __name__ == '__main__':
    print(f"Starting relay on pins {FM_RELAY_PIN} and {LED_RELAY_PIN}.")
    GPIO.write(FM_RELAY_PIN, 1)
    GPIO.write(LED_RELAY_PIN, 1)

    try:
        time.sleep(5)
    except KeyboardInterrupt:
        pass

    print("Stopping relays.")
    GPIO.write(FM_RELAY_PIN, 0)
    GPIO.write(LED_RELAY_PIN, 0)
    GPIO.stop()
