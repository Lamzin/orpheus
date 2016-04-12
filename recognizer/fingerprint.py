# # -*- coding: utf-8 -*-

import numpy
import scipy.io.wavfile

import config as cf

from os import path
from matplotlib import mlab


class Fingerprint(object):

    SAMPLE_RATE = 8000   # Hz
    # WINDOW_SIZE = 2048   # размер окна, в котором делается fft
    # WINDOW_STEP = 512    # шаг окна

    WINDOW_SIZE = 512   # размер окна, в котором делается fft
    WINDOW_STEP = 256   # шаг окна
    # WINDOW_SIZE = 256   # размер окна, в котором делается fft
    # WINDOW_STEP = 128   # шаг окна

    WINDOW_OVERLAP = WINDOW_SIZE - WINDOW_STEP

    @staticmethod
    def get(file_wav_8000):
        wave_file = path.join(cf.FOLDER_TEMP, file_wav_8000)
        wave_data = Fingerprint._get_wave_data(wave_file)
        fp = Fingerprint._get_fingerprint(wave_data)
        print 'len(fp) = ', len(fp)
        return fp

    @staticmethod
    def _get_wave_data(wave_file):
        sample_rate, wave_data = scipy.io.wavfile.read(wave_file)
        assert sample_rate == Fingerprint.SAMPLE_RATE, sample_rate
        if isinstance(wave_data[0], numpy.ndarray):  # стерео
            wave_data = wave_data.mean(1)
        return wave_data

    @staticmethod
    def _get_fingerprint(wave_data):
        # pxx[freq_idx][t] - мощность сигнала
        pxx, _, _ = mlab.specgram(
            wave_data,
            NFFT=Fingerprint.WINDOW_SIZE,
            noverlap=Fingerprint.WINDOW_OVERLAP,
            Fs=Fingerprint.SAMPLE_RATE)
        # return numpy.argmax(pxx, 0)  # max в каждый момент времени
        fp = numpy.argmax(pxx, 0)  # max в каждый момент времени
        return [16777216 * fp[i - 3] + 65536 * fp[i - 2] + 256 * fp[i - 1] + fp[i] for i in range(3, len(fp))]


if __name__ == '__main__':
    fp = Fingerprint.get(u'Muhteem Yzyl - Очень красивая игра на скрипке.wav')
    print len(fp)
    for item in fp:
        print item