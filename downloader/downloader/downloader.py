import sqlalchemy
import signal

from task import Task


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


class App(object):

    def __init__(self):
        self.db = create_engine()
        self.task = Task(db=self.db)

    def run(self):
        signal.signal(
            signal.SIGINT, (lambda signum, frame: self.task.stop()))

        # self.task._insert_urls_pesni_tut()
        try:
            self.task.run()
        except Exception:
            pass

if __name__ == '__main__':
    App().run()
