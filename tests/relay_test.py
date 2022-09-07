import time
import RPi.GPIO as GPIO
from constants import FM_RELAY_PIN

GPIO.setmode(GPIO.BOARD)
GPIO.setup(FM_RELAY_PIN, GPIO.OUT)

if __name__ == '__main__':
    print(f"Starting relay on pin {FM_RELAY_PIN}.")
    GPIO.output(FM_RELAY_PIN, GPIO.HIGH)
    time.sleep(5)

    print("Stopping relay.")
    GPIO.output(FM_RELAY_PIN, GPIO.LOW)
    GPIO.cleanup()
