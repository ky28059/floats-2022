import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import time
import RPi.GPIO as GPIO
from constants import TALON_PIN, CYCLE_TIME, PULSE_FREQUENCY, MAX_MS, MID_MS

STEP_SECONDS = 0.25  # How long in seconds to wait between each step in power

GPIO.setmode(GPIO.BCM)
GPIO.setup(TALON_PIN, GPIO.OUT)

print(f"Running with frequency={PULSE_FREQUENCY}Hz, duty cycle min={1.0 / CYCLE_TIME}, max={2.0 / CYCLE_TIME}")

talon = GPIO.PWM(TALON_PIN, PULSE_FREQUENCY)


# Converts [-1.0, 1.0] percent output values to talon duty cycle percentages [0.0, 100.0].
# TODO: abstraction?
def convert_duty_cycle(p: float) -> float:
    constrained = min(1.0, max(-1.0, p))
    return ((constrained * (MAX_MS - MID_MS)) + MID_MS) / CYCLE_TIME * 100.0


# Runs the talon at a percent output with PWM duty cycle.
# TODO: abstraction?
def run_talon(p: float) -> None:
    talon.ChangeDutyCycle(convert_duty_cycle(p))


if __name__ == '__main__':
    print("Starting TalonSRX PWM signal.")
    talon.start(convert_duty_cycle(0))

    try:
        # Sweep from 0 -> 1.0
        for p in range(1, 11, 1):
            print(f"Running Talon at {p / 10.0} power.")
            run_talon(p / 10.0)
            time.sleep(STEP_SECONDS)

        # Sweep from 1.0 -> -1.0
        for p in range(10, -11, -1):
            print(f"Running Talon at {p / 10.0} power.")
            run_talon(p / 10.0)
            time.sleep(STEP_SECONDS)

        # Sweep from -1.0 -> 0
        for p in range(-10, 1, 1):
            print(f"Running Talon at {p / 10.0} power.")
            run_talon(p / 10.0)
            time.sleep(STEP_SECONDS)
    except KeyboardInterrupt:
        pass

    print("Test finished, cleaning up.")
    talon.stop()
    GPIO.cleanup()
