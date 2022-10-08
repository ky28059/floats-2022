import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import time
import pigpio
from constants import TALON_PIN, CYCLE_TIME, PULSE_FREQUENCY, MAX_MS, MID_MS

STEP_SECONDS = 0.25  # How long in seconds to wait between each step in power

GPIO = pigpio.pi()
GPIO.set_mode(TALON_PIN, pigpio.ALT5)

print(f"Running with frequency={PULSE_FREQUENCY}Hz, duty cycle min={1.0 / CYCLE_TIME}, max={2.0 / CYCLE_TIME}")


# Runs the talon at a [-1.0, 1.0] percent output with PWM duty cycle.
# TODO: abstraction?
def run_talon(p: float) -> None:
    constrained = min(1.0, max(-1.0, p))
    duty_cycle = ((constrained * (MAX_MS - MID_MS)) + MID_MS) / CYCLE_TIME * 1000000
    GPIO.hardware_PWM(TALON_PIN, int(PULSE_FREQUENCY), int(duty_cycle))


if __name__ == '__main__':
    print("Starting TalonSRX PWM signal.")
    run_talon(0)

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
    GPIO.set_PWM_dutycycle(TALON_PIN, 0)
    GPIO.stop()
