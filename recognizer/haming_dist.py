# -*- coding: utf-8 -*-


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


def write_hashes(db, hashes, track_id):
    try:
        hashes_parts = split_hashes(hashes)

        with db.connect() as connection:
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
    dist, pow2 = 0, 1
    for i in range(64):
        if a & pow2 != b & pow2:
            dist += 1
        pow2 *= 2
    return dist


def find_similar(db, hashes):

    hashes = hashes_extend(hashes)
    hashes_parts = split_hashes(hashes)

    result = dict()
    with db.connect() as connection:
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
                    print('{:b}'.format(f)[::-1])
                    print('{:b}'.format(d[h])[::-1])
                    if result.get(track_id):
                        result[track_id] += 1
                    else:
                        result[track_id] = 1
    return result
