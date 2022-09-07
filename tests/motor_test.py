import time
import RPi.GPIO as GPIO
from constants import TALON_PIN

CYCLE_TIME = 10.0  # ms [2.9, 100]
PULSE_FREQUENCY = 1000.0 / CYCLE_TIME  # Hz (up to 100Hz)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(TALON_PIN, GPIO.OUT)

print(f"Running with frequency={PULSE_FREQUENCY}Hz, duty cycle min={1.0 / CYCLE_TIME}, max={2.0 / CYCLE_TIME}")

talon = GPIO.PWM(TALON_PIN, PULSE_FREQUENCY)


# Converts more standard [-1.0, 1.0] percent output values to talon duty cycle percentages [0.0, 100.0].
# TODO: abstraction?
def convert_duty_cycle(p: float) -> float:
    constrained = min(1.0, max(-1.0, p))
    return ((constrained * 0.5) + 1.5) / CYCLE_TIME


# Runs the talon at a percent output with PWM duty cycle.
# TODO: abstraction?
def run_talon(p: float) -> None:
    talon.ChangeDutyCycle(convert_duty_cycle(p))


if __name__ == '__main__':
    print("Starting TalonSRX PWM signal.")
    talon.start(convert_duty_cycle(0))

    print("Running Talon at 0.2 power.")
    run_talon(0.2)
    time.sleep(3.5)

    print("Running Talon at -0.2 power.")
    run_talon(-0.2)
    time.sleep(3.5)

    print("Test finished, cleaning up.")
    talon.stop()
    GPIO.cleanup()