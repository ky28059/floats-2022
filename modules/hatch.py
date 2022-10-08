import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import time
import RPi.GPIO as GPIO
from multiprocessing import Event
from constants import TALON_PIN, FORWARD_LS_PIN, BACKWARD_LS_PIN, FM_RELAY_PIN, LED_RELAY_PIN, \
                      CYCLE_TIME, PULSE_FREQUENCY, MAX_MS, MID_MS

GPIO.setmode(GPIO.BCM)
GPIO.setup(TALON_PIN, GPIO.OUT)
GPIO.setup([FORWARD_LS_PIN, BACKWARD_LS_PIN], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup([FM_RELAY_PIN, LED_RELAY_PIN], GPIO.OUT)

print(f"Running with frequency={PULSE_FREQUENCY}Hz, duty cycle min={1.0 / CYCLE_TIME}, max={2.0 / CYCLE_TIME}")

talon = GPIO.PWM(TALON_PIN, PULSE_FREQUENCY)

forward_ls = Event()
backward_ls = Event()


# Converts [-1.0, 1.0] percent output values to talon duty cycle percentages [0.0, 100.0].
def convert_duty_cycle(p: float) -> float:
    constrained = min(1.0, max(-1.0, p))
    return ((constrained * (MAX_MS - MID_MS)) + MID_MS) / CYCLE_TIME * 100.0


# Runs the talon at a percent output with PWM duty cycle.
def run_talon(p: float) -> None:
    talon.ChangeDutyCycle(convert_duty_cycle(p))


# Waits for a rising edge on the given limit switch, timing out after 5 seconds.
def wait_for_edge(ls: Event):
    ls.clear()
    ls.wait(timeout=5.0)


def hatch(during_school: Event, is_passing: Event):
    GPIO.add_event_detect(FORWARD_LS_PIN, GPIO.RISING, callback=lambda c: forward_ls.set())
    GPIO.add_event_detect(BACKWARD_LS_PIN, GPIO.RISING, callback=lambda c: backward_ls.set())

    talon.start(convert_duty_cycle(0))

    try:
        while True:
            # Wait for school and passing period before running
            during_school.wait()
            is_passing.wait()

            # Run forward and wait for the forward limit switch to trip
            run_talon(0.3)
            GPIO.output([FM_RELAY_PIN, LED_RELAY_PIN], GPIO.HIGH)  # Turn on the fog machine and LEDs
            wait_for_edge(forward_ls)

            # Stop the motor when hit and keep the hatch open for 3 seconds
            run_talon(0)
            time.sleep(3)

            # Run backwards and wait for the backwards limit switch to trip
            run_talon(-0.3)
            GPIO.output([FM_RELAY_PIN, LED_RELAY_PIN], GPIO.LOW)  # Turn off the fog machine and LEDs
            wait_for_edge(backward_ls)

            # Stop the motor when hit and keep the hatch closed for 3 seconds
            run_talon(0)
            time.sleep(3)

    # Exit loop on keyboard interrupt
    except KeyboardInterrupt:
        pass

    # Clean up and exit
    talon.stop()
    GPIO.cleanup()


if __name__ == '__main__':
    from schedule import during_school, is_passing, schedule_process
    schedule_process.start()
    hatch(during_school, is_passing)
