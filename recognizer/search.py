# # -*- coding: utf-8 -*-

import os

import fingerprint
import converter
import config as cf
import HEngine


def search_similar(file_name):
    file_name_new = converter.convert(file_name, cf.FOLDER_BOT)
    fps = fingerprint.get_fingerprint_for_short(file_name_new, save=True)
    os.remove(os.path.join(cf.FOLDER_TEMP, file_name_new))

    ans = []
    similar_global = dict()
    for fp in fps:
        for band_index, fp_band in enumerate(fp):
            similar = HEngine.find_similar(fp_band)
            for k, v in similar.items():
                if similar_global.get(k):
                    similar_global[k] += v
                else:
                    similar_global[k] = v

    if similar_global:
        for k, v in similar_global.items():
            ss = u'{} - {}'.format(k, v)
            ans.append(ss)
            print(ss)
    else:
        ans.append(u'not found')

    return ans
