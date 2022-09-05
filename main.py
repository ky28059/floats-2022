from threading import Thread
from modules.hatch import main as hatch
from modules.radio import main as radio

hatch_thread = Thread(target=hatch, daemon=True)
radio_thread = Thread(target=radio, daemon=True)

hatch_thread.start()
radio_thread.start()
