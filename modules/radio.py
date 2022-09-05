import time
import json
from datetime import datetime
from os import walk
from random import randrange
from pygame import mixer

with open('../schedule.json') as f:
    schedules = json.load(f)

(_, _, filenames) = next(walk('../music'))
queue = []  # An array of filenames that houses the remaining songs to play
mixer.init()


# Loads and plays a song from the remaining songs in the queue.
def play_random_song_from_queue(curr: str) -> str:
    # Add all files except currently playing song back to queue when it becomes empty
    if len(queue) == 0:
        queue.extend(filter(lambda x: x != curr, filenames))
    index = randrange(len(queue))

    print(f"Playing {queue[index]}: position {index + 1} of {len(queue)}")
    mixer.music.load('../music/' + queue[index])
    mixer.music.play()

    curr = queue[index]
    queue.pop(index)  # Remove the song from queue so it doesn't get replayed
    return curr


def main():
    curr = None  # The filename of the currently playing song, so that it doesn't get played twice
    warn_message_sent = False

    # Tick every 1/2 second
    while True:
        # Get current schedule
        now = datetime.now()
        is_passing = True  # Whether it is passing period or before/after school

        try:
            curr_schedule = schedules[now.weekday()]
            curr_minutes = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds() / 60

            # Don't play if more than 45 minutes before school or 15 minutes after
            if curr_schedule[0]["s"] - curr_minutes >= 45 or curr_minutes - curr_schedule[-1]["e"] > 15:
                if mixer.music.get_busy():
                    mixer.music.fadeout(7500)  # Fade out over 7.5 seconds
                time.sleep(0.5)
                continue

            for per in curr_schedule:
                if per["s"] <= curr_minutes <= per["e"]:
                    is_passing = False
                    break
        except IndexError:
            if not warn_message_sent:  # Perhaps a better approach for only sending these logs once exists, but this works
                print('[WARN] IndexError - Function most likely invoked on the weekend')
                print('[WARN] Fallback will play music at max volume')
                warn_message_sent = True

        # Music logic
        if not mixer.music.get_busy():  # If the music player is idle, queue another track
            curr = play_random_song_from_queue(curr)
        # Adjust right float as needed to determine how quiet it should be during class
        mixer.music.set_volume(1.0 if is_passing else 0.1)

        time.sleep(0.5)


if __name__ == '__main__':
    main()
