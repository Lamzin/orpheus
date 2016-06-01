# # -*- coding: utf-8 -*-

import os
import signal

import db
import HEngine
import converter
import fingerprint
import config as cf


class App(object):

    def __init__(self):
        self.is_stopped = False

    def run(self):
        signal.signal(
            signal.SIGINT, (lambda signum, frame: self.stop()))

        while not self.is_stopped:
            try:
                tasks = db.get_task()
                if not tasks:
                    continue

                for track_id, url_disk, in tasks:
                    try:
                        _, file_name = os.path.split(url_disk)
                        fp = self.get_fingerprint(file_name)
                        for index, fp_band in enumerate(fp):
                            HEngine.write_hashes_all(fp_band, track_id)
                            print(file_name, len(fp_band))
                    except Exception as e:
                        db.mark_task_as(track_id, 'ps_error')
                        print(e)

            except Exception as e:
                print(e)

    def stop(self):
        self.is_stopped = True

    @staticmethod
    def get_fingerprint(file_name):
        f_new = converter.convert(file_name)
        fp = fingerprint.get_fingerprint(f_new)
        os.remove(os.path.join(cf.FOLDER_TEMP, f_new))
        return fp


if __name__ == '__main__':
    App().run()
