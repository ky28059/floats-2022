import time
from os import walk
from random import randrange
from pygame import mixer
from schedule import data


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

    # Tick every 1/2 second
    while True:
        # If it's before or after school, stop the music
        if data['before_school']:
            if mixer.music.get_busy():
                mixer.music.fadeout(7500)  # Fade out over 7.5 seconds
            time.sleep(0.5)
            continue

        if not mixer.music.get_busy():  # If the music player is idle, queue another track
            curr = play_random_song_from_queue(curr)
        # Adjust right float as needed to determine how quiet it should be during class
        mixer.music.set_volume(1.0 if data['is_passing'] else 0.1)

        time.sleep(0.5)


if __name__ == '__main__':
    main()
