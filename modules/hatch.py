import time
import RPi.GPIO as GPIO
from constants import TALON_PIN, FORWARD_LS_PIN, BACKWARD_LS_PIN, FM_RELAY_PIN, LED_RELAY_PIN

CYCLE_TIME = 10.0  # ms [2.9, 100]
PULSE_FREQUENCY = 1000.0 / CYCLE_TIME  # Hz (up to 100Hz)

GPIO.setmode(GPIO.BCM)
GPIO.setup(TALON_PIN, GPIO.OUT)
GPIO.setup([FORWARD_LS_PIN, BACKWARD_LS_PIN], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup([FM_RELAY_PIN, LED_RELAY_PIN], GPIO.OUT)

print(f"Running with frequency={PULSE_FREQUENCY}Hz, duty cycle min={1.0 / CYCLE_TIME}, max={2.0 / CYCLE_TIME}")

talon = GPIO.PWM(TALON_PIN, PULSE_FREQUENCY)


# Converts more standard [-1.0, 1.0] percent output values to talon duty cycle percentages [0.0, 100.0].
def convert_duty_cycle(p: float) -> float:
    constrained = min(1.0, max(-1.0, p))
    return ((constrained * 0.5) + 1.5) / CYCLE_TIME


# Runs the talon at a percent output with PWM duty cycle.
def run_talon(p: float) -> None:
    talon.ChangeDutyCycle(convert_duty_cycle(p))


def main():
    talon.start(convert_duty_cycle(0))
    try:
        while True:
            # Run forward and wait for the forward limit switch to trip
            run_talon(0.3)
            GPIO.output([FM_RELAY_PIN, LED_RELAY_PIN], GPIO.HIGH)  # Turn on the fog machine and LEDs
            GPIO.wait_for_edge(FORWARD_LS_PIN, GPIO.RISING, timeout=5000)

            # Stop the motor when hit and keep the hatch open for 3 seconds
            run_talon(0)
            time.sleep(3)

            # Run backwards and wait for the backwards limit switch to trip
            run_talon(-0.3)
            GPIO.output([FM_RELAY_PIN, LED_RELAY_PIN], GPIO.LOW)  # Turn off the fog machine and LEDs
            GPIO.wait_for_edge(BACKWARD_LS_PIN, GPIO.RISING, timeout=5000)

            # Stop the motor when hit and keep the hatch closed for 3 seconds
            run_talon(0)
            time.sleep(3)

    # Clean up and exit on keyboard interrupt
    except KeyboardInterrupt:
        talon.stop()
        GPIO.cleanup()


if __name__ == '__main__':
    main()
