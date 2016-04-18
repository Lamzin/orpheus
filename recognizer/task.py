# # -*- coding: utf-8 -*-

import os

import converter
import fingerprint
import config as cf


class Task(object):

    def __init__(self, db):
        self.db = db
        self.is_stopped = False

    def stop(self):
        self.is_stopped = True

    def run(self):
        while not self.is_stopped:
            try:
                tasks = self._get_task()
                if not tasks:
                    continue

                for track_id, url_disk, in tasks:
                    _, file_name = os.path.split(url_disk)
                    fp = self._get_fingerprint(file_name)
                    self._write_parts(track_id, fp)

            except Exception as e:
                self._mark_as_error(track_id)
                print e

    def _get_fingerprint(self, f):
        f_new = converter.convert(f)
        fp = fingerprint.get_fingerprint(f_new)
        os.remove(os.path.join(cf.FOLDER_TEMP, f_new))
        return fp

    def _get_task(self):
        with self.db.connect() as connection:
            tasks = connection.execute("""
                SELECT t.id, t.url_disk
                FROM track AS t
                LEFT JOIN fp_queue AS fpq ON t.id = fpq.id
                WHERE fpq.id is NULL
                  AND t.processing_stage = 'ps_done'
                ORDER BY t.id
                LIMIT 4
            """).fetchall()

            return tasks

    def _write_parts(self, track_id, fp):
        length = 768  # 768 - примерно 30 секунд, 512 - примерно 20 секунд
        step = length / 2
        for i in range(0, len(fp), step):
            self._write_fp(track_id, i / step, fp[i:min(i + length, len(fp))])

        with self.db.begin() as transaction:
            transaction.execute("""
                INSERT INTO fp_queue(id, processing_stage)
                VALUE ('{}', 'ps_done_fp')
            """.format(track_id))


    def _write_fp(self, track_id, track_part, fp):
        count = {}
        for item in fp:
            count[item] = count[item] + 1 if count.get(item) else 1

        values = ', '.join([
            "('{}', '{}', '{}', '{}')".format(key, value, track_id, track_part)
            for key, value in count.iteritems()
        ])

        with self.db.begin() as transaction:
            transaction.execute("""
                INSERT INTO fingerprints(frequency, count, track_id, track_part)
                VALUES {}
            """.format(values))

    def _mark_as_error(self, track_id):
        with self.db.begin() as transaction:
            transaction.execute("""
                INSERT INTO fp_queue(id, processing_stage)
                VALUE ('{}', 'ps_error')
            """.format(track_id))
