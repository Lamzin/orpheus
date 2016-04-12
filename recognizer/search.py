# # -*- coding: utf-8 -*-

import sys
import sqlalchemy

from fingerprint import Fingerprint


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

    def run(self):
        track_name = sys.argv[1]
        fp = Fingerprint.get(track_name)

        similar = self.find_similar_tracks2(fp)
        # if similar:
        #     for track_id, count in similar:
        #         print track_id, count
        # else:
        #     print 'not found'

    def find_similar_tracks(self, fp):
        values = '({})'.format(', '.join(map(str, fp)))

        with self.db.connect() as connection:
            rows = connection.execute("""
                SELECT track_id, frequency, count(*)
                FROM orpheus.fingerprints
                WHERE frequency in {}
                GROUP BY track_id
                ORDER BY count(*) DESC
                LIMIT 10
            """.format(values)).fetchall()

            return rows

    def find_similar_tracks2(self, fp):
        count = {}
        for item in fp:
            count[item] = count[item] + 1 if count.get(item) else 1
        values = '({})'.format(', '.join(map(str, count.keys())))

        with self.db.connect() as connection:
            rows = connection.execute("""
                SELECT frequency, count, track_id
                FROM orpheus.fingerprints
                WHERE frequency in {}
            """.format(values)).fetchall()

            tracks = {}
            for row in rows:
                if not tracks.get(row.track_id):
                    tracks[row.track_id] = 0
                # tracks[row.track_id] += row.count * count[row.frequency]
                tracks[row.track_id] += 1

            for key, value in tracks.iteritems():
                print key, value
            # return rows

if __name__ == '__main__':
    SearchApp().run()
