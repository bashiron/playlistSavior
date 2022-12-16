import psycopg, os, sys

if __name__ == '__main__':
    with psycopg.connect('dbname=playlist user=bashiron') as conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT tmp_playlist, id FROM "Videos"')
            entirety = cursor.fetchall()
            processed = [('{' + x + '}', y) for x,y in entirety]
            cursor.executemany('UPDATE "Videos" SET playlist = (%s) WHERE id = (%s)', processed)
