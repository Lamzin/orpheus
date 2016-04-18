# # -*- coding: utf-8 -*-

import numpy
import scipy.io.wavfile

from os import path
from matplotlib import pyplot, mlab

import config as cf

a1 = cf.WINDOW_SIZE ** 1
a2 = cf.WINDOW_SIZE ** 2
a3 = cf.WINDOW_SIZE ** 3
a4 = cf.WINDOW_SIZE ** 4


def get_fingerprint(file_name, file_path=cf.FOLDER_TEMP, save=False):
    wave_file = path.join(file_path, file_name)
    wave_data = get_wave_data(wave_file)
    fp = get_fingerprint_from_data(wave_data)
    if save:
        save_specgram(wave_data)
    return fp


def get_wave_data(wave_file):
    sample_rate, wave_data = scipy.io.wavfile.read(wave_file)
    assert sample_rate == cf.SAMPLE_RATE, sample_rate
    if isinstance(wave_data[0], numpy.ndarray):  # стерео
        wave_data = wave_data.mean(1)
    return wave_data


def save_specgram(wave_data):
    fig = pyplot.figure()
    ax = fig.add_axes((0.1, 0.1, 0.8, 0.8))
    ax.specgram(
        wave_data,
        NFFT=cf.WINDOW_SIZE,
        noverlap=cf.WINDOW_OVERLAP,
        Fs=cf.SAMPLE_RATE)
    pyplot.savefig(path.join(cf.FOLDER_TEMP, 'foo.png'))


def get_fingerprint_from_data(wave_data):
    # pxx[freq_idx][t] - мощность сигнала
    pxx, _, _ = mlab.specgram(
        wave_data,
        NFFT=cf.WINDOW_SIZE,
        noverlap=cf.WINDOW_OVERLAP,
        Fs=cf.SAMPLE_RATE)

    bands = [
        pxx[0:10],
        pxx[10:20],
        pxx[20:40],
        pxx[40:80],
        pxx[80:160],
        pxx[160:511]
    ]

    fps = [
        get_fingerprint_hash(numpy.argmax(band, 0))  # max в каждый момент времени
        for band in bands
    ]

    return fps


def get_fingerprint_hash(fp):
    return [
        a4 * fp[i - 4] + a3 * fp[i - 3] + a2 * fp[i - 2] + a1 * fp[i - 1] + fp[i]
        for i in range(4, len(fp))
    ]
