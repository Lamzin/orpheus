# -*- coding: utf-8 -*-


import subprocess
import signal
import time


def handler(signum, frame):
    print 'Start kill "recognizer/recognizer.py" ...'
    subprocess.Popen(['pkill', '-SIGINT', 'recognizer/recognizer.py'])


if __name__ == "__main__":

    process_count = 4
    for i in range(process_count):
        subprocess.Popen(['python', 'recognizer/recognizer.py'])
        time.sleep(10)

    signal.signal(signal.SIGINT, handler)

    while True:
        time.sleep(1)
