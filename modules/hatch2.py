import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import time
import pigpio
from multiprocessing import Event
from constants import TALON_PIN, FORWARD_LS_PIN, BACKWARD_LS_PIN, FM_RELAY_PIN, LED_RELAY_PIN, \
                      CYCLE_TIME, PULSE_FREQUENCY, MAX_MS, MID_MS

GPIO = pigpio.pi()
GPIO.set_mode(TALON_PIN, pigpio.ALT5)
GPIO.set_mode(FORWARD_LS_PIN, pigpio.INPUT)
GPIO.set_mode(BACKWARD_LS_PIN, pigpio.INPUT)

GPIO.set_pull_up_down(FORWARD_LS_PIN, pigpio.PUD_DOWN)
GPIO.set_pull_up_down(BACKWARD_LS_PIN, pigpio.PUD_DOWN)

GPIO.set_mode(FM_RELAY_PIN, pigpio.OUTPUT)
GPIO.set_mode(LED_RELAY_PIN, pigpio.OUTPUT)

print(f"Running with frequency={PULSE_FREQUENCY}Hz, duty cycle min={1.0 / CYCLE_TIME}, max={2.0 / CYCLE_TIME}")


# Runs the talon at a [-1.0, 1.0] percent output with PWM duty cycle.
def run_talon(p: float) -> None:
    constrained = min(1.0, max(-1.0, p))
    duty_cycle = ((constrained * (MAX_MS - MID_MS)) + MID_MS) / CYCLE_TIME * 1000000
    GPIO.hardware_PWM(TALON_PIN, int(PULSE_FREQUENCY), int(duty_cycle))


def hatch(during_school: Event, is_passing: Event):
    run_talon(0)

    try:
        # Close the hatch if it is open on startup (if the forward limit switch is not pressed)
        if not GPIO.read(FORWARD_LS_PIN):
            run_talon(0.3)
            GPIO.wait_for_edge(FORWARD_LS_PIN, pigpio.RISING_EDGE, 1.25)
            run_talon(0)
            time.sleep(3)

        while True:
            # Wait for school and passing period before running
            during_school.wait()
            is_passing.wait()

            # Run the hatch open and wait for the backwards limit switch to trip
            run_talon(-0.15)
            GPIO.write(FM_RELAY_PIN, 1)  # Turn on the fog machine and LEDs
            GPIO.write(LED_RELAY_PIN, 1)
            GPIO.wait_for_edge(BACKWARD_LS_PIN, pigpio.RISING_EDGE, 1.25)

            # Stop the motor when hit and keep the hatch open for 3 seconds
            run_talon(0)
            time.sleep(3)

            # Run the hatch closed and wait for the forward limit switch to trip
            run_talon(0.3)
            GPIO.write(FM_RELAY_PIN, 0)  # Turn off the fog machine and LEDs
            GPIO.write(LED_RELAY_PIN, 0)
            GPIO.wait_for_edge(FORWARD_LS_PIN, pigpio.RISING_EDGE, 1.25)

            # Stop the motor when hit and keep the hatch closed for 3 seconds
            run_talon(0)
            time.sleep(3)

    # Exit loop on keyboard interrupt
    except KeyboardInterrupt:
        pass

    # Clean up and exit
    GPIO.set_PWM_dutycycle(TALON_PIN, 0)
    GPIO.write(FM_RELAY_PIN, 0)
    GPIO.write(LED_RELAY_PIN, 0)
    GPIO.stop()


if __name__ == '__main__':
    from schedule import during_school, is_passing, schedule_process
    schedule_process.start()
    hatch(during_school, is_passing)
