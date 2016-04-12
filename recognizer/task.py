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
                    _, f = os.path.split(url_disk)
                    print f

                    fp = self._get_fingerprint(url_disk)
                    self._write_fp(track_id, fp)

            except Exception as e:
                print e

    def _get_fingerprint(self, f):
        f_new = converter.Converter.convert_file(f)
        fp = fingerprint.Fingerprint.get(f_new)
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

    def _write_fp(self, track_id, fp):
        count = {}
        for item in fp:
            count[item] = count[item] + 1 if count.get(item) else 1

        values = ', '.join([
            "('{}', '{}', '{}')".format(key, value, track_id)
            for key, value in count.iteritems()
        ])

        with self.db.begin() as transaction:
            transaction.execute("""
                INSERT INTO fingerprints(frequency, count, track_id)
                VALUES {}
            """.format(values))

            transaction.execute("""
                INSERT INTO fp_queue(id, processing_stage)
                VALUE ('{}', 'ps_done_fp')
            """.format(track_id))
