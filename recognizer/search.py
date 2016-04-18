# # -*- coding: utf-8 -*-

import os
import sqlalchemy

import fingerprint
import converter
import config as cf


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

    def run(self, file_name, path):
        file_name_new = converter.convert(file_name, cf.FOLDER_BOT)
        fp = fingerprint.get_fingerprint(file_name_new)
        os.remove(os.path.join(cf.FOLDER_TEMP, file_name_new))
        print len(fp), max(fp)

        similar = self.find_similar_tracks3(fp)
        if similar:
            return [
                u'{} | {} - {}'.format(row.cnt, row.author, row.name)
                for row in similar
            ]
        else:
            return [u'not found']

    def find_similar_tracks3(self, fp):
        values = '({})'.format(', '.join(map(str, fp)))

        with self.db.connect() as connection:
            rows = connection.execute("""
                SELECT f.track_id, f.track_part, count(*) AS cnt, t.name, t.author
                FROM orpheus.fingerprints AS f
                JOIN orpheus.track AS t ON t.id = f.track_id
                WHERE frequency IN {}
                GROUP BY track_id, track_part
                ORDER BY count(*) DESC
                LIMIT 30
            """.format(values)).fetchall()

            print len(rows)

            for row in rows:
                print row.name, row.author, row.track_id, row.track_part, row.cnt

            return rows
