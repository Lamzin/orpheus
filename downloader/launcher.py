# -*- coding: utf-8 -*-


import subprocess
import signal
import time


def handler(signum, frame):
    print 'Start kill "downloader/downloader.py" ...'
    subprocess.Popen(['pkill', '-SIGINT', 'downloader/downloader.py'])


if __name__ == "__main__":

    process_count = 50
    for i in range(process_count):
        subprocess.Popen(['python', 'downloader/downloader.py'])

    signal.signal(signal.SIGINT, handler)

    while True:
        time.sleep(1)
