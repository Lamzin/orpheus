# # -*- coding: utf-8 -*-

import numpy
import math
# import hashlib
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


def get_fingerprint_from_data_old(wave_data):
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
        pxx[i:i+32]
        for i in range(0, 512, 32)
    ]


    fps = []
    for band in bands:
        fp = []
        matrix = band.transpose()
        for timeline in matrix:
            # cnt1, cnt2 = 0, 0
            # for i in range(1, len(timeline)):
            #     if timeline[i - 1] < timeline[i]:
            #         cnt1 += 1
            #     else:
            #         cnt2 += 1
            # fp.append(0 if cnt1 < cnt2 else 1)


            # arr = []
            # for i, var in enumerate(timeline):
            #     arr.append((i, var))
            # arr.sort(key=lambda x: x[1])
            #
            # sum_of_index = 0
            # for i, _ in arr[-8:]:
            #     sum_of_index += i
            # sum_of_index /= 8
            # fp.append(0 if 2 * sum_of_index < len(timeline) else 1)

            arr = []
            for i, var in enumerate(timeline):
                arr.append((i, var))
            arr.sort(key=lambda x: x[1])
            arr = arr[-8:]
            arr.sort(key=lambda x: x[0])

            m = 0
            w = 0
            for i, var in arr:
                w += i * var
                m += var
            w /= m

            fp.append(0 if 2 * w < len(timeline) else 1)
            # cnt1, cnt2 = 0, 0
            # for i in range(1, len(arr)):
            #     if timeline[arr[i - 1][0]] < timeline[arr[i][0]]:
            #         cnt1 += 1
            #     else:
            #         cnt2 += 1
            # fp.append(0 if cnt1 < cnt2 else 1)

        fps.append(fp)

    # fps = [
    #     numpy.argmax(band, 0).tolist()  # max в каждый момент времени
    #     for band in bands
    # ]

    return fps


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


def energy(band, time, i):
    e = 0

    sequence_length = get_sequence_length(i)
    for index in range(8 * i, 8 * i + sequence_length):
        e += band[time][index] * band[time][index]
        # e += band[time][index]
    return e


def get_fingerprint_from_data(wave_data):
    # pxx[freq_idx][t] - мощность сигнала
    pxx, _, _ = mlab.specgram(
        wave_data,
        NFFT=cf.WINDOW_SIZE,
        noverlap=cf.WINDOW_OVERLAP,
        Fs=cf.SAMPLE_RATE)

    # 300-2870 | delta = 256 * 10 = 8 * 32 * 10
    bands = [pxx[30*2:300*2].transpose()]

    cnt1, cnt2 = 0, 0

    arr = []
    for band in bands:
        for time, timeline in enumerate(band):
            if time == 0:
                continue

            hash32, pow2 = 0, 1
            for j in range(1, 65):
                # if (band[time][j]**2 - band[time][j - 1]**2) - (band[time - 1][j]**2 - band[time - 1][j - 1]**2) > 0:
                #     hash32 += pow2
                if (energy(band, time, j) - energy(band, time, j - 1)) - (energy(band, time - 1, j) - energy(band, time - 1, j - 1)) > 0:
                    hash32 += pow2
                    cnt1 += 1
                else:
                    cnt2 += 1
                pow2 *= 2
            arr.append(hash32)

    print('Done fingerprinting...', cnt1, cnt2)

    return [arr]

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
    return fps
    return _get_perceptual_hash(fps, 64)


def get_perceptual_hash_short_file(fps):
    return fps
    return _get_perceptual_hash(fps, 1)


def _get_perceptual_hash(fps, step):
    # middle = [4, 4, 8, 12, 26, 100]
    hash_fps = []

    for index, fp in enumerate(fps):
        current = []
        zero = 0
        one = 0
        for i in range(0, len(fp) - 64, step):
            hash64, pow2 = 0, 1
            for j in range(i, i + 64):
                # if fp[j] > middle[index]:
                if fp[j]:
                    hash64 += pow2
                    one += 1
                else:
                    zero += 1
                pow2 *= 2
            current.append(hash64)
            # print(index, hash32, middle[index], fp[i:i+32])
        hash_fps.append(current)
        print (float(zero) / (zero + one), float(one) / (zero + one))

    return hash_fps
