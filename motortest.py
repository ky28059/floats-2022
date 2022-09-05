import time
from hatch import start_talon, run_talon, cleanup_io

if __name__ == '__main__':
    print("Starting TalonSRX PWM signal.")
    start_talon()

    print("Running Talon at 0.2 power.")
    run_talon(0.2)
    time.sleep(3.5)

    print("Running Talon at -0.2 power.")
    run_talon(-0.2)
    time.sleep(3.5)

    print("Test finished, cleaning up.")
    cleanup_io()
