# # -*- coding: utf-8 -*-

import sqlalchemy


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


Engine = create_engine()


def get_task():
    with Engine.connect() as connection:
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
            mark_task_as(row.id, 'ps_processing')

        return rows


def mark_task_as(track_id, status):
    with Engine.connect() as connection:
        connection.execute("""
            INSERT INTO perceptual_queue(id, processing_stage)
            VALUE ('{id}', '{status}')
            ON DUPLICATE KEY UPDATE processing_stage = VALUES(processing_stage)
        """.format(id=track_id, status=status))
