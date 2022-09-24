from multiprocessing import Process
from modules.hatch import main as hatch
from modules.radio import main as radio

hatch_process = Process(target=hatch, daemon=True)
radio_process = Process(target=radio, daemon=True)

hatch_process.start()
radio_process.start()

try:
    while True:
        pass
except KeyboardInterrupt:
    hatch_process.join()
    radio_process.join()
