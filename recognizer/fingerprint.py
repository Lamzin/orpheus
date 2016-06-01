# # -*- coding: utf-8 -*-

import numpy
import scipy.io.wavfile

from os import path
from matplotlib import pyplot, mlab

import config as cf


def get_fingerprint(file_name, file_path=cf.FOLDER_TEMP, save=False):
    wave_file = path.join(file_path, file_name)
    wave_data = get_wave_data(wave_file)
    fp = get_fingerprint_from_data(wave_data)
    if save:
        save_specgram(wave_data)
    return fp


def get_fingerprint_for_short(file_name, file_path=cf.FOLDER_TEMP, save=False):
    wave_file = path.join(file_path, file_name)
    wave_data = get_wave_data(wave_file)
    if save:
        save_specgram(wave_data)

    fps = []
    # for i in range(0, 333*5 + 1, 333):
    #     wave_data_shift = wave_data[i:]
    #     fp = get_fingerprint_from_data(wave_data_shift)
    #     fps.append(fp)

    for i in range(0, 333*128 + 1, 333):
        wave_data_shift = wave_data[i:min(len(wave_data), i + 4096 * 50)]
        fp = get_fingerprint_from_data(wave_data_shift)
        fps.append(fp)

    return fps


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


def get_sequence_length(i):
    # 512 = 32 * (6) + 16 * (8) + 8 * (11) + 8 * (13)

    if i < 32:
        return 6
    if i < 48:
        return 8
    if i < 56:
        return 11
    if i < 64:
        return 13
    return 13


def energy(matrix, time, i):
    e = 0
    sequence_length = get_sequence_length(i)
    for index in range(8 * i, 8 * i + sequence_length):
        e += matrix[time][index] * matrix[time][index]
    return e


def get_fingerprint_from_data(wave_data):
    # pxx[freq_idx][t] - мощность сигнала
    pxx, _, _ = mlab.specgram(
        wave_data,
        NFFT=cf.WINDOW_SIZE,
        noverlap=cf.WINDOW_OVERLAP,
        Fs=cf.SAMPLE_RATE)

    # 300-2870 | delta = 256 * 10 = 8 * 32 * 10
    matrix = pxx[30*2:300*2].transpose()

    cnt1, cnt2 = 0, 0
    arr = []
    for time, timeline in enumerate(matrix):
        if time == 0:
            continue

        hash64, pow2 = 0, 1
        for j in range(1, 65):
            energy1 = energy(matrix, time, j) - energy(matrix, time, j - 1)
            energy2 = energy(matrix, time - 1, j) - energy(matrix, time - 1, j - 1)
            if energy1 - energy2 > 0:
                hash64 += pow2
                cnt1 += 1
            else:
                cnt2 += 1
            pow2 *= 2
        arr.append(hash64)

    print('Done fingerprinting...', cnt1, cnt2)

    return [arr]
