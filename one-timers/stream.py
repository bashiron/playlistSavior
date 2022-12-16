import psycopg, os, sys

if __name__ == '__main__':
    with psycopg.connect('dbname=playlist user=bashiron') as conn:
        with conn.cursor() as cursor:
            for elem in cursor.stream('SELECT * FROM "Videos"'):
                print('name: ' + elem[1] + ' playlists: ' + str(elem[2]))
