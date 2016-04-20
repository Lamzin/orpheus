# # -*- coding: utf-8 -*-

import os
import sqlalchemy
import signal
import json

import converter
import fingerprint
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
    return sqlalchemy.create_engine(url, pool_size=16)


class App(object):

    def __init__(self):
        self.db = create_engine()
        self.is_stopped = False
        self.values = []

    def run(self):
        signal.signal(
            signal.SIGINT, (lambda signum, frame: self.stop()))

        while not self.is_stopped:
            try:
                tasks = self.get_task()
                if not tasks:
                    continue

                for track_id, url_disk, in tasks:
                    try:
                        _, file_name = os.path.split(url_disk)
                        fp = self.get_fingerprint(track_id, file_name)
                        for fp_band in fp:
                            self.write_parts(track_id, fp_band)
                            print(file_name, len(fp_band), max(fp_band))
                        self.write_values()
                    except Exception as e:
                        self.mark_as(track_id, 'ps_error')
                        print(e)

            except Exception as e:
                print(e)

    def stop(self):
        self.is_stopped = True

    def get_task(self):
        with self.db.connect() as connection:
            rows = connection.execute("""
                SELECT t.id, t.url_disk
                FROM track AS t
                LEFT JOIN fp_queue AS fpq ON t.id = fpq.id
                WHERE fpq.id is NULL
                  AND t.processing_stage = 'ps_done'
                ORDER BY t.id
                LIMIT 1
            """).fetchall()

            for row in rows:
                self.mark_as(row.id, 'ps_processing')

            return rows

    def get_fingerprint(self, track_id, file_name):
        fp = self.get_fingerprint_saved(track_id)
        if fp is None:
            f_new = converter.convert(file_name)
            fp = fingerprint.get_fingerprint(f_new)
            self.write_fingerprint(track_id, fp)
            os.remove(os.path.join(cf.FOLDER_TEMP, f_new))
        else:
            print('Meta from database')

        fp = fingerprint.get_fingerprint_hash(fp)
        return fp

    def get_fingerprint_saved(self, track_id):
        with self.db.connect() as connection:
            text = connection.execute("""
                SELECT fingerprints
                FROM fp_data
                WHERE id = {}
            """.format(track_id)).scalar()
            return None if text is None else json.loads(text)

    def write_fingerprint(self, track_id, fp):
        with self.db.connect() as connection:
            text = json.dumps(fp)
            connection.execute("""
                INSERT INTO fp_data(id, fingerprints)
                VALUES ('{}', '{}')
            """.format(track_id, text))

    def write_parts(self, track_id, fp):
        length = cf.TRACK_LENGTH * (cf.SAMPLE_RATE / cf.WINDOW_SIZE) * (cf.WINDOW_SIZE / cf.WINDOW_STEP)  # примерно TRACK_LENGTH секунд
        step = length / 2
        for i in range(0, len(fp), step):
            self.write_fp(track_id, i / step, fp[i:min(i + length, len(fp))])

        self.mark_as(track_id, 'ps_done_fp')

    def write_fp(self, track_id, track_part, fp):
        track = (track_id * 256 + track_part) & 0xFFFFFFFF
        count = set(fp)
        self.values += [
            (item, track)
            for item in count
        ]

    def write_values(self):
        values = ', '.join([
            "('{}', '{}')".format(hash, track)
            for hash, track in self.values
        ])

        with self.db.connect() as connection:
            connection.execute("""
                INSERT INTO fingerprints(hash, track)
                VALUES {}
            """.format(values))
            self.values = []

    def mark_as(self, track_id, status):
        with self.db.connect() as connection:
            connection.execute("""
                INSERT INTO fp_queue(id, processing_stage)
                VALUE ('{id}', '{status}')
                ON DUPLICATE KEY UPDATE processing_stage = VALUES(processing_stage)
            """.format(id=track_id, status=status))

if __name__ == '__main__':
    App().run()
