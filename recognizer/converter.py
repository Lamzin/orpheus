# -*- coding: utf-8 -*-

import os
import subprocess

import config as cf

from subprocess import PIPE, STDOUT


def convert(file_name, folder_path=cf.FOLDER_DATA):
    input_file = os.path.join(folder_path, file_name)
    file_name = os.path.splitext(file_name)[0] + '.wav'
    output_file = os.path.join(cf.FOLDER_TEMP, file_name)

    command = u'ffmpeg -i "{}" -ar {} -y "{}"'.format(input_file, cf.SAMPLE_RATE, output_file)
    res = subprocess.call(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    return output_file
