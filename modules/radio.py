import time
from os import walk
from random import randrange
from pygame import mixer
from multiprocessing import Event
from pathlib import Path

music_dir = f'{Path(__file__).parent.parent}/music'

(_, _, filenames) = next(walk(music_dir))
queue = []  # An array of filenames that houses the remaining songs to play
mixer.init()


# Loads and plays a song from the remaining songs in the queue.
def play_random_song_from_queue(curr: str) -> str:
    # Add all files except currently playing song back to queue when it becomes empty
    if len(queue) == 0:
        queue.extend(filter(lambda x: x != curr, filenames))
    index = randrange(len(queue))

    print(f"Playing {queue[index]}: position {index + 1} of {len(queue)}")
    mixer.music.load(f'{music_dir}/{queue[index]}')
    mixer.music.play()

    curr = queue[index]
    queue.pop(index)  # Remove the song from queue so it doesn't get replayed
    return curr


def radio(during_school: Event, is_passing: Event):
    curr = None  # The filename of the currently playing song, so that it doesn't get played twice

    try:
        while True:
            # If it's before or after school, stop the music
            if not during_school.is_set():
                if mixer.music.get_busy():
                    mixer.music.fadeout(7500)  # Fade out over 7.5 seconds
                # Wait for school to begin
                during_school.wait()

            if not mixer.music.get_busy():  # If the music player is idle, queue another track
                curr = play_random_song_from_queue(curr)
            # Adjust right float as needed to determine how quiet it should be during class
            mixer.music.set_volume(1.0 if is_passing.is_set() else 0.1)

            time.sleep(0.5)

    except KeyboardInterrupt:
        mixer.quit()


if __name__ == '__main__':
    from schedule import during_school, is_passing, schedule_process
    schedule_process.start()
    radio(during_school, is_passing)
