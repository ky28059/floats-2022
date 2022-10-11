from multiprocessing import Process
from modules.hatch import hatch
from modules.radio import radio
from modules.schedule import during_school, is_passing, schedule_process

hatch_process = Process(target=hatch, args=(during_school, is_passing), daemon=True)

if __name__ == '__main__':
    schedule_process.start()
    hatch_process.start()

    try:
        radio(during_school, is_passing)
    except KeyboardInterrupt:
        hatch_process.join()
