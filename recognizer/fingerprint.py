# # -*- coding: utf-8 -*-

import numpy
import scipy.io.wavfile

from os import path
from matplotlib import mlab

import config as cf

a1 = cf.WINDOW_SIZE ** 1
a2 = cf.WINDOW_SIZE ** 2
a3 = cf.WINDOW_SIZE ** 3
a4 = cf.WINDOW_SIZE ** 4


def get_fingerprint(file_name, file_path=cf.FOLDER_TEMP):
    wave_file = path.join(file_path, file_name)
    wave_data = get_wave_data(wave_file)
    fp = get_fingerprint_from_data(wave_data)
    return fp


def get_wave_data(wave_file):
    sample_rate, wave_data = scipy.io.wavfile.read(wave_file)
    assert sample_rate == cf.SAMPLE_RATE, sample_rate
    if isinstance(wave_data[0], numpy.ndarray):  # стерео
        wave_data = wave_data.mean(1)
    return wave_data


def get_fingerprint_from_data(wave_data):
    # pxx[freq_idx][t] - мощность сигнала
    pxx, _, _ = mlab.specgram(
        wave_data,
        NFFT=cf.WINDOW_SIZE,
        noverlap=cf.WINDOW_OVERLAP,
        Fs=cf.SAMPLE_RATE)
    fp = numpy.argmax(pxx, 0)  # max в каждый момент времени
    return get_fingerprint_hash(fp)


def get_fingerprint_hash(fp):
    # return [
    #     16777216 * fp[i - 3] + 65536 * fp[i - 2] + 256 * fp[i - 1] + fp[i]
    #     for i in range(3, len(fp))
    # ]
    return [
        a4 * fp[i - 4] + a3 * fp[i - 3] + a2 * fp[i - 2] + a1 * fp[i - 1] + fp[i]
        for i in range(4, len(fp))
    ]
