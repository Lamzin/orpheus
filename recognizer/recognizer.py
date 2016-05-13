# # -*- coding: utf-8 -*-

import os
import sqlalchemy
import signal
import json

import converter
import fingerprint
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
    return sqlalchemy.create_engine(url, pool_size=16)


class App(object):

    def __init__(self):
        self.db = create_engine()
        self.is_stopped = False

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
                        for index, fp_band in enumerate(fp):
                            # self.write(track_id, index, fp_band)
                            haming_dist.write_hashes(self.db, fp_band, track_id)
                            print(file_name, len(fp_band))
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
                LEFT JOIN perceptual_queue AS fpq ON t.id = fpq.id
                WHERE fpq.id is NULL
                  AND t.processing_stage = 'ps_done'
                ORDER BY t.id
                LIMIT 1
            """).fetchall()

            for row in rows:
                self.mark_as(row.id, 'ps_processing')

            return rows

    def get_fingerprint(self, track_id, file_name):
        # fp = self.get_fingerprint_saved(track_id)
        # if fp is None:
        #     f_new = converter.convert(file_name)
        #     fp = fingerprint.get_fingerprint(f_new)
        #     self.write_fingerprint(track_id, fp)
        #     os.remove(os.path.join(cf.FOLDER_TEMP, f_new))
        # else:
        #     print('Meta from database')
        #
        # fp = fingerprint.get_perceptual_hash_long_file(fp)
        # return fp

        f_new = converter.convert(file_name)
        fp = fingerprint.get_fingerprint(f_new)
        # self.write_fingerprint(track_id, fp)
        os.remove(os.path.join(cf.FOLDER_TEMP, f_new))
        fp = fingerprint.get_perceptual_hash_long_file(fp)
        return fp

    # def get_fingerprint_saved(self, track_id):
    #     with self.db.connect() as connection:
    #         text = connection.execute("""
    #             SELECT fingerprints
    #             FROM fp_perceptual_data
    #             WHERE id = {}
    #         """.format(track_id)).scalar()
    #         return None if text is None else json.loads(text)

    def write_fingerprint(self, track_id, fp):
        with self.db.connect() as connection:
            text = json.dumps(fp)
            connection.execute("""
                INSERT INTO fp_data(id, fingerprints)
                VALUES ('{}', '{}')
            """.format(track_id, text))

    def write(self, track_id, band, fp_band):
        values = ', '.join([
            "('{}', '{}', '{}')".format(perceptual_hash, track_id, band)
            for perceptual_hash in fp_band
        ])

        with self.db.connect() as connection:
            connection.execute("""
                INSERT INTO perceptual_hashes(hash, track, band)
                VALUES {}
            """.format(values))

        self.mark_as(track_id, 'ps_done_fp')

    def mark_as(self, track_id, status):
        with self.db.connect() as connection:
            connection.execute("""
                INSERT INTO perceptual_queue(id, processing_stage)
                VALUE ('{id}', '{status}')
                ON DUPLICATE KEY UPDATE processing_stage = VALUES(processing_stage)
            """.format(id=track_id, status=status))

if __name__ == '__main__':
    App().run()
