import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import time
import pigpio
from constants import TALON_PIN, CYCLE_TIME, PULSE_FREQUENCY, MAX_MS, MID_MS, PWM_RANGE

STEP_SECONDS = 0.25  # How long in seconds to wait between each step in power

GPIO = pigpio.pi()
GPIO.set_mode(TALON_PIN, pigpio.ALT5)
GPIO.set_PWM_range(TALON_PIN, PWM_RANGE)

print(f"Running with frequency={PULSE_FREQUENCY}Hz, duty cycle min={1.0 / CYCLE_TIME}, max={2.0 / CYCLE_TIME}")


# Converts more standard [-1.0, 1.0] percent output values to a pigpio duty cycle range.
# TODO: abstraction?
def convert_duty_cycle(p: float) -> float:
    constrained = min(1.0, max(-1.0, p))
    return int(((constrained * (MAX_MS - MID_MS)) + MID_MS) / CYCLE_TIME * PWM_RANGE)


# Runs the talon at a percent output with PWM duty cycle.
# TODO: abstraction?
def run_talon(p: float) -> None:
    GPIO.set_PWM_dutycycle(TALON_PIN, convert_duty_cycle(p))


if __name__ == '__main__':
    print("Starting TalonSRX PWM signal.")
    GPIO.hardware_PWM(TALON_PIN, PULSE_FREQUENCY, int(MID_MS / CYCLE_TIME * 1000000))

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
    GPIO.stop()
