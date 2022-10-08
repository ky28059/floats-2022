import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import pigpio
from multiprocessing import Event
from constants import TALON_PIN, FORWARD_LS_PIN, BACKWARD_LS_PIN, CYCLE_TIME, PULSE_FREQUENCY, MAX_MS, MID_MS

GPIO = pigpio.pi()
GPIO.set_mode(TALON_PIN, pigpio.ALT5)
GPIO.set_mode(FORWARD_LS_PIN, pigpio.INPUT)
GPIO.set_mode(BACKWARD_LS_PIN, pigpio.INPUT)

GPIO.set_pull_up_down(FORWARD_LS_PIN, pigpio.PUD_DOWN)
GPIO.set_pull_up_down(BACKWARD_LS_PIN, pigpio.PUD_DOWN)

print(f"Running with frequency={PULSE_FREQUENCY}Hz, duty cycle min={1.0 / CYCLE_TIME}, max={2.0 / CYCLE_TIME}")

forward_ls = Event()
backward_ls = Event()


# Runs the talon at a [-1.0, 1.0] percent output with PWM duty cycle.
# TODO: abstraction?
def run_talon(p: float) -> None:
    constrained = min(1.0, max(-1.0, p))
    duty_cycle = ((constrained * (MAX_MS - MID_MS)) + MID_MS) / CYCLE_TIME * 1000000
    GPIO.hardware_PWM(TALON_PIN, int(PULSE_FREQUENCY), int(duty_cycle))


# Waits for a rising edge on the given limit switch.
def wait_for_edge(ls: Event):
    ls.clear()
    ls.wait()


if __name__ == '__main__':
    # GPIO.callback(FORWARD_LS_PIN, pigpio.RISING_EDGE, lambda c, l, t: forward_ls.set())
    # GPIO.callback(BACKWARD_LS_PIN, pigpio.RISING_EDGE, lambda c, l, t: backward_ls.set())

    print("Starting TalonSRX PWM signal.")
    run_talon(0)

    try:
        while True:
            print(f"Running Talon forwards until rising edge on {FORWARD_LS_PIN}.")
            run_talon(0.5)
            # wait_for_edge(forward_ls)
            GPIO.wait_for_edge(FORWARD_LS_PIN, pigpio.RISING_EDGE)

            print(f"Running Talon backwards until rising edge on {BACKWARD_LS_PIN}.")
            run_talon(-0.5)
            # wait_for_edge(backward_ls)
            GPIO.wait_for_edge(BACKWARD_LS_PIN, pigpio.RISING_EDGE)

    except KeyboardInterrupt:
        print("Test finished, cleaning up.")
        GPIO.set_PWM_dutycycle(TALON_PIN, 0)
        GPIO.stop()
