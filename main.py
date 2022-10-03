from multiprocessing import Process
from modules.hatch import hatch
from modules.radio import radio
from modules.schedule import during_school, is_passing, schedule_process

hatch_process = Process(target=hatch, args=(during_school, is_passing), daemon=True)
radio_process = Process(target=radio, args=(during_school, is_passing), daemon=True)

if __name__ == '__main__':
    schedule_process.start()
    hatch_process.start()
    radio_process.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        hatch_process.join()
        radio_process.join()
