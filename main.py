import time
import simpleaudio as sa
from pydub import AudioSegment
from pydub.playback import play



def timer() -> None:
    print("Hello from timer!")
    times = 0
    interval = input("please input interval that reminds you(minutes): ")
    while True:
        time.sleep(int(interval) * 60)
        times = times + 1
        # play alert
        obj = AudioSegment.from_mp3("./alert.mp3")
        play(obj)

        print(f"It's time to take a break!,you have finished {times} times!")
        exit_ = input("exit?")
        if exit_ == "yes" or exit_ == "y":
            print("Goodbye!")
            break


def main() -> None:
    timer()
if __name__ == "__main__":
    timer()