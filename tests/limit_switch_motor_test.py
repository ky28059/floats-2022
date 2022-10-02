import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import RPi.GPIO as GPIO
from constants import TALON_PIN, FORWARD_LS_PIN, BACKWARD_LS_PIN

CYCLE_TIME = 10.0  # ms [2.9, 100]
PULSE_FREQUENCY = 1000.0 / CYCLE_TIME  # Hz (up to 100Hz)

GPIO.setmode(GPIO.BCM)
GPIO.setup(TALON_PIN, GPIO.OUT)
GPIO.setup([FORWARD_LS_PIN, BACKWARD_LS_PIN], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

print(f"Running with frequency={PULSE_FREQUENCY}Hz, duty cycle min={1.0 / CYCLE_TIME}, max={2.0 / CYCLE_TIME}")

talon = GPIO.PWM(TALON_PIN, PULSE_FREQUENCY)


# Converts more standard [-1.0, 1.0] percent output values to talon duty cycle percentages [0.0, 100.0].
# TODO: abstraction?
def convert_duty_cycle(p: float) -> float:
    constrained = min(1.0, max(-1.0, p))
    return ((constrained * 0.5) + 1.5) / CYCLE_TIME * 100.0


# Runs the talon at a percent output with PWM duty cycle.
# TODO: abstraction?
def run_talon(p: float) -> None:
    talon.ChangeDutyCycle(convert_duty_cycle(p))


if __name__ == '__main__':
    print("Starting TalonSRX PWM signal.")
    talon.start(convert_duty_cycle(0))

    try:
        while True:
            print(f"Running Talon forwards until rising edge on {FORWARD_LS_PIN}.")
            run_talon(0.5)
            GPIO.wait_for_edge(FORWARD_LS_PIN, GPIO.RISING)

            print(f"Running Talon backwards until rising edge on {BACKWARD_LS_PIN}.")
            run_talon(-0.5)
            GPIO.wait_for_edge(BACKWARD_LS_PIN, GPIO.RISING)

    except KeyboardInterrupt:
        print("Test finished, cleaning up.")
        talon.stop()
        GPIO.cleanup()
