from threading import Thread
import time
from datetime import datetime
import json

with open('../schedule.json') as f:
    schedules = json.load(f)

data = {
    'before_school': False,  # Whether it is before the start or after the end of the school day
    'is_passing': True  # Whether no class is currently ongoing
}


# Continually updates the schedule data, ticking every 0.5 seconds and warning on index errors.
def update_schedule_data():
    warn_message_sent = False

    while True:
        now = datetime.now()

        try:
            # Get current schedule
            curr_schedule = schedules[now.weekday()]
            curr_minutes = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds() / 60

            # Don't run electronics if more than 45 minutes before school or 15 minutes after
            if curr_schedule[0]["s"] - curr_minutes >= 45 or curr_minutes - curr_schedule[-1]["e"] > 15:
                data['before_school'] = True
                time.sleep(0.5)
                continue
            else:
                data['before_school'] = False

            for per in curr_schedule:
                if per["s"] <= curr_minutes <= per["e"]:
                    data['is_passing'] = False
                    break
        except IndexError:
            if not warn_message_sent:  # Perhaps a better approach for only sending these logs once exists, but this works
                print('[WARN] IndexError - Function most likely invoked on the weekend')
                print('[WARN] Fallback will play music at max volume')
                warn_message_sent = True

        time.sleep(0.5)


# Automatically start auto-updating background thread on import
thread = Thread(target=update_schedule_data, daemon=True)
thread.start()
