# # -*- coding: utf-8 -*-

import numpy
import hashlib
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

    # bands = [
    #     pxx[0:10],
    #     pxx[10:20],
    #     pxx[20:40],
    #     pxx[40:80],
    #     pxx[80:160],
    #     pxx[160:511]
    # ]

    bands = [
        pxx[i:i+16]
        for i in range(0, 512, 16)
    ]

    fps = [
        numpy.argmax(band, 0).tolist()  # max в каждый момент времени
        for band in bands
    ]

    return fps


# def get_fingerprint_hash(fps):
#     hash_fps = []
#
#     for index, fp in enumerate(fps):
#         hash_fps.append([
#             int(hashlib.md5(str(fp[i:i+cf.FINGERPRINT_HASH_LENGTH[index] + 1]).encode()).hexdigest(), 16) & 0xFFFFFFFFFFFFFFFF
#             for i in range(0, len(fp) - cf.FINGERPRINT_HASH_LENGTH[index])
#         ])
#
#     return hash_fps


def get_perceptual_hash_long_file(fps):
    return _get_perceptual_hash(fps, 64)


def get_perceptual_hash_short_file(fps):
    return _get_perceptual_hash(fps, 1)


def _get_perceptual_hash(fps, step):
    # middle = [4, 4, 8, 12, 26, 100]
    hash_fps = []

    for index, fp in enumerate(fps):
        current = []
        zero = 0
        one = 0
        for i in range(0, len(fp) - 64, step):
            hash32, pow2 = 0, 1
            for j in range(i, i + 64):
                # if fp[j] > middle[index]:
                if fp[j] > 7:
                    hash32 += pow2
                    one += 1
                else:
                    zero += 1
                pow2 *= 2
            current.append(hash32)
            # print(index, hash32, middle[index], fp[i:i+32])
        hash_fps.append(current)
        print (float(zero) / (zero + one), float(one) / (zero + one))

    return hash_fps
