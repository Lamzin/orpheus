# -*- coding: utf-8 -*-

import os
import pydub
import random
import string
import subprocess

import config as cf

from os import path
from subprocess import PIPE, STDOUT


class Converter(object):

    @staticmethod
    def convert_file(path_to_file_mp3_44100):
        _, file_mp3_44100 = path.split(path_to_file_mp3_44100)
        file_wav_44100 = path.join(cf.FOLDER_TEMP, Converter._get_random_name())
        file_wav_8000 = path.join(cf.FOLDER_TEMP, u''.join(file_mp3_44100.split(u'.')[:-1]) + u'.wav')

        sound = pydub.AudioSegment.from_mp3(path_to_file_mp3_44100)
        sound.export(path.join(cf.FOLDER_TEMP, file_wav_44100), format='wav')

        Converter._down_sample(file_wav_44100, file_wav_8000)

        os.remove(file_wav_44100)

        return file_wav_8000

    @staticmethod
    def _get_random_name():
        return u''.join(
            random.choice(string.ascii_uppercase + string.digits)
            for _ in range(20))

    @staticmethod
    def _down_sample(file_input, file_output):
        sox_call = u'sox "{}" "{}" rate 8k'.format(file_input, file_output)
        subprocess.call(sox_call, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)


if __name__ == '__main__':
    Converter.convert_file(u'/home/oleh/git/lamzin/orpheus/recognizer/temp/Chelsi_-_Ty_prosto_pover.mp3')
