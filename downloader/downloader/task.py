# -*- coding: utf-8 -*-

import time

from parser import Parser


class Task(object):

    def __init__(self, db):
        self.db = db
        self.parser = Parser()
        self.is_stopped = False

    def stop(self):
        self.is_stopped = True
        print 'Downloader is stoping...'

    def run(self):
        while True:
            if self.is_stopped:
                return
            tasks = self._get_new_task(limit=2)
            if tasks:
                for task in tasks:
                    try:
                        result = self.parser.proceed(task['url_page'])
                        result['id'] = task['id']
                        self._mark_as_done(result)
                        print 'done: ', result['author'], result['name']
                    except Exception as e:
                        self._mark_as_failed(task['id'])
                        print e
            else:
                time.sleep(5)

    def _get_new_task(self, **kwargs):
        with self.db.connect() as connection:
            rows = connection.execute("""
                SELECT id, url_page
                FROM track
                WHERE processing_stage = 'ps_new'
                  AND site_id = 2
                LIMIT {limit}
                FOR UPDATE
            """.format(**kwargs)).fetchall()

            if rows:
                connection.execute("""
                    UPDATE track
                    SET processing_stage = 'ps_processing'
                    WHERE id in ({})
                """.format(','.join([str(row['id']) for row in rows])))

                return rows

    def _mark_as_done(self, kwargs):
        with self.db.connect() as connection:
            connection.execute(u"""
                UPDATE track
                SET processing_stage = 'ps_done',
                    name = '{name}',
                    author = '{author}',
                    url_disk = '{url_disk}'
                WHERE id = {id}
            """.format(**kwargs))

    def _mark_as_failed(self, track_id):
        with self.db.connect() as connection:
            connection.execute(u"""
                UPDATE track
                SET processing_stage = 'ps_not_found'
                WHERE id = '{id}'
            """.format(id=track_id))

    def _insert_urls_best_muzon(self):
        with self.db.connect() as connection:
            for i in range(71193):
                url = 'http://best-muzon.com/popsa/{}-.html'.format(i)
                connection.execute("""
                    INSERT INTO track(url_page, site_id)
                    VALUES ('{}', '{}')
                """.format(url, 1))

    def _insert_urls_pesni_tut(self):
        with self.db.connect() as connection:
            for i in range(241304):
                url = 'http://pesni-tut.net/download_song-{}.html'.format(i)
                connection.execute("""
                    INSERT INTO track(url_page, site_id)
                    VALUES ('{}', '{}')
                """.format(url, 2))
