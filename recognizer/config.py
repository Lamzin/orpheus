# -*- coding: utf-8 -*-

# FINGERPRINT_HASH_LENGTH = [
#     11,
#     9,
#     7,
#     6,
#     5,
#     5
# ]

FINGERPRINT_HASH_LENGTH = [
    16,
    13,
    8,
    5,
    4,
    4
]


TRACK_LENGTH = 20

SAMPLE_RATE = 44100  # Hz
WINDOW_SIZE = 4096   # размер окна, в котором делается fft
WINDOW_STEP = 2048   # шаг окна

# TMP:
# WINDOW_SIZE = 2048   # размер окна, в котором делается fft
# WINDOW_STEP = 512   # шаг окна

WINDOW_OVERLAP = WINDOW_SIZE - WINDOW_STEP


FOLDER_DATA = u'/media/oleh/data/orpheus'
FOLDER_TEMP = u'/media/oleh/data/temp'
FOLDER_BOT = u'/home/oleh/git/lamzin/orpheus/recognizer/voices'
