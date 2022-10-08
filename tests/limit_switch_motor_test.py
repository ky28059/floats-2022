import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import RPi.GPIO as GPIO
from multiprocessing import Event
from constants import TALON_PIN, FORWARD_LS_PIN, BACKWARD_LS_PIN, CYCLE_TIME, PULSE_FREQUENCY, MAX_MS, MID_MS

GPIO.setmode(GPIO.BCM)
GPIO.setup(TALON_PIN, GPIO.OUT)
GPIO.setup([FORWARD_LS_PIN, BACKWARD_LS_PIN], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

print(f"Running with frequency={PULSE_FREQUENCY}Hz, duty cycle min={1.0 / CYCLE_TIME}, max={2.0 / CYCLE_TIME}")

talon = GPIO.PWM(TALON_PIN, PULSE_FREQUENCY)

forward_ls = Event()
backward_ls = Event()


# Converts more standard [-1.0, 1.0] percent output values to talon duty cycle percentages [0.0, 100.0].
# TODO: abstraction?
def convert_duty_cycle(p: float) -> float:
    constrained = min(1.0, max(-1.0, p))
    return ((constrained * (MAX_MS - MID_MS)) + MID_MS) / CYCLE_TIME * 100.0


# Runs the talon at a percent output with PWM duty cycle.
# TODO: abstraction?
def run_talon(p: float) -> None:
    talon.ChangeDutyCycle(convert_duty_cycle(p))


# Waits for a rising edge on the given limit switch.
def wait_for_edge(ls: Event):
    ls.clear()
    ls.wait()


if __name__ == '__main__':
    GPIO.add_event_detect(FORWARD_LS_PIN, GPIO.RISING, callback=forward_ls.set)
    GPIO.add_event_detect(BACKWARD_LS_PIN, GPIO.RISING, callback=backward_ls.set)

    print("Starting TalonSRX PWM signal.")
    talon.start(convert_duty_cycle(0))

    try:
        while True:
            print(f"Running Talon forwards until rising edge on {FORWARD_LS_PIN}.")
            run_talon(0.5)
            wait_for_edge(forward_ls)

            print(f"Running Talon backwards until rising edge on {BACKWARD_LS_PIN}.")
            run_talon(-0.5)
            wait_for_edge(backward_ls)

    except KeyboardInterrupt:
        print("Test finished, cleaning up.")
        talon.stop()
        GPIO.cleanup()
