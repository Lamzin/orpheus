# # -*- coding: utf-8 -*-

import numpy
import scipy.io.wavfile
from matplotlib import pyplot, mlab
from collections import defaultdict

# SAMPLE_RATE = 8000   # Hz
# # WINDOW_SIZE = 2048   # размер окна, в котором делается fft
# # WINDOW_STEP = 512    # шаг окна
#
# # WINDOW_SIZE = 512    # размер окна, в котором делается fft
# # WINDOW_STEP = 256    # шаг окна
# WINDOW_SIZE = 256    # размер окна, в котором делается fft
# WINDOW_STEP = 128    # шаг окна

SAMPLE_RATE = 44100  # Hz
WINDOW_SIZE = 4096   # размер окна, в котором делается fft
WINDOW_STEP = 4096   # шаг окна


WINDOW_OVERLAP = WINDOW_SIZE - WINDOW_STEP


def get_wave_data(wave_filename):
    sample_rate, wave_data = scipy.io.wavfile.read(wave_filename)
    assert sample_rate == SAMPLE_RATE, sample_rate
    if isinstance(wave_data[0], numpy.ndarray):  # стерео
        wave_data = wave_data.mean(1)
    return wave_data


def show_specgram(wave_data):
    fig = pyplot.figure()
    ax = fig.add_axes((0.1, 0.1, 0.8, 0.8))
    ax.specgram(
        wave_data,
        NFFT=WINDOW_SIZE,
        noverlap=WINDOW_OVERLAP,
        Fs=SAMPLE_RATE)
    pyplot.show()


def get_fingerprint(wave_data):
    # pxx[freq_idx][t] - мощность сигнала
    pxx, _, _ = mlab.specgram(
        wave_data,
        NFFT=WINDOW_SIZE,
        noverlap=WINDOW_OVERLAP,
        Fs=SAMPLE_RATE)
    # band = pxx[15:250]  # наиболее интересные частоты от 60 до 1000 Hz
    band = pxx  # все частоты
    return numpy.argmax(band, 0)  # max в каждый момент времени


def compare_fingerprints(base_fp, fp):
    base_fp_hash = defaultdict(list)
    for time_index, freq_index in enumerate(base_fp):
        base_fp_hash[freq_index].append(time_index)

    matches = [
        t - time_index # разницы времен совпавших частот
        for time_index, freq_index in enumerate(fp)
        for t in base_fp_hash[freq_index]
    ]

    pyplot.clf()
    pyplot.hist(matches, 1000)
    pyplot.show()


if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print 'python demo.py file1.wav [file2.wav]'
    else:
        d1 = get_wave_data(sys.argv[1])
        show_specgram(d1)
        fp1 = get_fingerprint(d1)
        print len(fp1), max(fp1)
        if len(sys.argv) > 2:
            d2 = get_wave_data(sys.argv[2])
            show_specgram(d2)
            fp2 = get_fingerprint(d2)
            print len(fp2), max(fp2)
            compare_fingerprints(fp1, fp2)

            count = {}
            for item in fp1:
                if count.get(item):
                    count[item] += 1
                else:
                    count[item] = 1

            ans = 0
            for item in fp2:
                ans += count[item] if count.get(item) else 0

            print ans
