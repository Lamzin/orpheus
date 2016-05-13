# # -*- coding: utf-8 -*-

import os
import sqlalchemy

import fingerprint
import converter
import config as cf
import haming_dist


MYSQL_DEFAULT_CONFIGS = {
    'user': 'wiki_bot',
    'pass': '31415',
    'host': 'localhost',
    'port': '3306',
    'database': 'orpheus',
}


def create_engine(configs=None):
    configs = configs or MYSQL_DEFAULT_CONFIGS
    url = u'mysql+pymysql://{user}:{pass}@{host}:{port}/' \
          u'{database}?charset=utf8&use_unicode=1'.format(**configs)
    return sqlalchemy.create_engine(url, pool_size=64)


class SearchApp(object):

    def __init__(self):
        self.db = create_engine()
        self.stat = {}

    def run(self, file_name, path):
        file_name_new = converter.convert(file_name, cf.FOLDER_BOT)
        fps = fingerprint.get_fingerprint_for_short(file_name_new, save=True)
        os.remove(os.path.join(cf.FOLDER_TEMP, file_name_new))

        ans = []
        similar_global = dict()
        for fp in fps:
            for band_index, fp_band in enumerate(fp):
                # similar = self.find_similar_tracks(band_index, fp_band)
                # if similar:
                #     ans.append(u'\n'.join([
                #         u'{} | {} - {}'.format(row.cnt, row.author, row.name)
                #         for row in similar
                #     ]))
                # else:
                #     ans.append(u'not found')
                similar = haming_dist.find_similar(self.db, fp_band)
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

        for key, value in self.stat.items():
            print(key, value)

        # ans = []
        return ans

    def find_similar_tracks(self, band_index, fp_band):
        # if band_index < 5:
        #     return None

        with self.db.connect() as connection:
            rows = connection.execute("""
                SELECT hash, track
                FROM orpheus.perceptual_hashes
                WHERE band = {}
            """.format(band_index)).fetchall()

        ans = []
        s = set()
        for cur_hash in fp_band:
            # print('cur_hash = %s' % cur_hash)
            if cur_hash == 0:
                print('cur_hash = 0')
                continue
            for row in rows:
                dist = self.get_hamming_distance(cur_hash, row.hash)
                if dist < 12:
                    print(dist, row.track)
                    ans.append([dist, row.track])
                    s.add(row.track)
                    if self.stat.get(row.track):
                        self.stat[row.track] += 1
                    else:
                        self.stat[row.track] = 1

        # for item in ans:
        #     print(item)

        # for item in s:
        #     track = item
        #     if self.stat.get(track):
        #         self.stat[track] += 1
        #     else:
        #         self.stat[track] = 1

        print(band_index, len(ans))

        return None

    @staticmethod
    def get_hamming_distance(a, b):
        dist, pow2 = 0, 1
        for i in range(64):
            if a & pow2 != b & pow2:
                dist += 1
            pow2 *= 2
        return dist
