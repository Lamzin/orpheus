# # -*- coding: utf-8 -*-

import os
import sqlalchemy
import signal

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

    def run(self):
        signal.signal(
            signal.SIGINT, (lambda signum, frame: self.stop()))

        while not self.is_stopped:
            try:
                tasks = self.get_task()
                if not tasks:
                    continue

                for track_id, url_disk, in tasks:
                    _, file_name = os.path.split(url_disk)
                    fp = self.get_fingerprint(file_name)
                    for fp_band in fp:
                        self.write_parts(track_id, fp_band)
                        print(file_name, len(fp_band), max(fp_band))

            except Exception as e:
                self.mark_as(track_id, 'ps_error')
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

    @staticmethod
    def get_fingerprint(file_name):
        f_new = converter.convert(file_name)
        fp = fingerprint.get_fingerprint(f_new)
        os.remove(os.path.join(cf.FOLDER_TEMP, f_new))
        return fp

    def write_parts(self, track_id, fp):
        length = cf.TRACK_LENGTH * cf.SAMPLE_RATE / cf.WINDOW_SIZE  # примерно 30 секунд
        step = length / 2
        for i in range(0, len(fp), step):
            self.write_fp(track_id, i / step, fp[i:min(i + length, len(fp))])

        self.mark_as(track_id, 'ps_done_fp')

    def write_fp(self, track_id, track_part, fp):
        count = set(fp)
        values = ', '.join([
            "('{}', '{}', '{}')".format(item, track_id, track_part)
            for item in count
        ])

        with self.db.begin() as transaction:
            transaction.execute("""
                INSERT INTO fingerprints(frequency, track_id, track_part)
                VALUES {}
            """.format(values))

    def mark_as(self, track_id, status):
        with self.db.begin() as transaction:
            transaction.execute("""
                INSERT INTO fp_queue(id, processing_stage)
                VALUE ('{id}', '{status}')
                ON DUPLICATE KEY UPDATE processing_stage = VALUES(processing_stage)
            """.format(id=track_id, status=status))

if __name__ == '__main__':
    App().run()






