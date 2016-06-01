# # -*- coding: utf-8 -*-

import os

import db
import fingerprint
import converter
import config as cf
import HEngine


def search_similar(file_name):
    file_name_new = converter.convert(file_name, cf.FOLDER_BOT)
    fps = fingerprint.get_fingerprint_for_short(file_name_new, save=True)
    os.remove(os.path.join(cf.FOLDER_TEMP, file_name_new))

    similar_global = dict()

    for fp in fps:
        for band_index, fp_band in enumerate(fp):
            similar = HEngine.find_similar_daemon_hengine(fp_band)
            for k, v in similar.items():
                if similar_global.get(k):
                    similar_global[k] += v
                else:
                    similar_global[k] = v

    ans = []
    if similar_global:
        tracks = db.get_track_names(similar_global.keys())
        tracks = {
            track.id: [0, track.author, track.name]
            for track in tracks
        }

        for k, v in similar_global.items():
            tracks[k][0] = v

        info = "Total candidates {}".format(len(tracks))
        ans.append(info)
        print(info)

        for item in sorted(tracks.values(), key=lambda x: x[0])[:-6:-1]:
            info = u'{} - {} - {}'.format(*item)
            ans.append(info)
            print(info)
    else:
        ans.append(u'not found')

    return ans
