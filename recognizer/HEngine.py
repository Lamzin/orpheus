# -*- coding: utf-8 -*-


import db


MAX_HAMMING_DISTANCE = 11
TWO_10 = 2 ** 10
TWO_11 = 2 ** 11


def split_hashes(hashes):
    hashes_parts = [[], [], [], [], [], []]
    for t in hashes:
        hashes_parts[0].append(t % TWO_10)
        t /= TWO_10

        hashes_parts[1].append(t % TWO_10)
        t /= TWO_10

        hashes_parts[2].append(t % TWO_11)
        t /= TWO_11

        hashes_parts[3].append(t % TWO_11)
        t /= TWO_11

        hashes_parts[4].append(t % TWO_11)
        t /= TWO_11

        hashes_parts[5].append(t % TWO_11)
        t /= TWO_11
    return hashes_parts


def hashes_extend(hashes):
    result = []
    result.extend(hashes)
    for item in hashes:
        pow = 1
        for i in range(64):
            result.append(item | pow)
            pow *= 2

    return result


def write_hashes(hashes, track_id):
    try:
        hashes_parts = split_hashes(hashes)

        with db.Engine.connect() as connection:
            for i in range(6):
                values = ', '.join([
                    "('{}', '{}', '{}')".format(item, hashes[index], track_id)
                    for index, item in enumerate(hashes_parts[i])
                ])

                connection.execute("""
                    INSERT INTO hashes{}(hash, full_hash, track_id)
                    VALUES {}
                """.format(i, values))

    except Exception as e:
        print(e)


def get_hamming_distance(a, b):
    n = a ^ b
    n = (n & 0x5555555555555555) + ((n & 0xAAAAAAAAAAAAAAAA) >> 1)
    n = (n & 0x3333333333333333) + ((n & 0xCCCCCCCCCCCCCCCC) >> 2)
    n = (n & 0x0F0F0F0F0F0F0F0F) + ((n & 0xF0F0F0F0F0F0F0F0) >> 4)
    n = (n & 0x00FF00FF00FF00FF) + ((n & 0xFF00FF00FF00FF00) >> 8)
    n = (n & 0x0000FFFF0000FFFF) + ((n & 0xFFFF0000FFFF0000) >> 16)
    n = (n & 0x00000000FFFFFFFF) + ((n & 0xFFFFFFFF00000000) >> 32)  # This last & isn't strictly necessary.
    return n


def find_similar(hashes):

    hashes = hashes_extend(hashes)
    hashes_parts = split_hashes(hashes)

    result = dict()
    with db.Engine.connect() as connection:
        for i in range(6):
            d = dict()
            for index, item in enumerate(hashes_parts[i]):
                d[item] = hashes[index]

            values = ', '.join(map(str, hashes_parts[i]))

            rows = connection.execute("""
                SELECT hash, full_hash, track_id
                FROM hashes{}
                WHERE hash IN ({})
            """.format(i, values)).fetchall()

            for h, f, track_id, in rows:
                hdist = get_hamming_distance(f, d[h])
                if hdist < 12:
                    print(track_id, hdist)
                    if result.get(track_id):
                        result[track_id] += 1
                    else:
                        result[track_id] = 1
    return result
