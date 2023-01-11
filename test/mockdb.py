from unittest import TestCase
from unittest.mock import patch
import subprocess as sub
import psycopg
import playlist_savior

db = 'test_playlist'
user = 'bashiron'

class MockDB(TestCase):

    @classmethod
    def setUpClass(cls):
        # drop database if it already exists
        sub.run(f'dropdb {db}', shell=True, text=True)

        # create database
        sub.run(f'createdb {db}', shell=True, text=True)

        # create database structure
        sub.run(f'pg_dump playlist -s | psql {db}', shell=True, text=True, capture_output=True)

        # insert data
        conn = psycopg.connect(f'dbname={db} user={user}')
        cursor = conn.cursor()
        try:
            data = [
                ('Incursione', '{smash}', '{ost}'),
                ('Minagiru Chikara', '{smash}', '{ost}'),
                ('in the blue shirt', '{music}', '{music}'),
                ('Dark Souls 2: All Over Now', '{favs}', '{none}'),
                ("il vento d'oro", '{music}', '{music}')
            ]
            # en_data holds the values in data but adds a "counter" as the first item
            en_data = []
            for n in range(1, len(data)):
                en_data.append(tuple([str(n)] + list(data[n])))

            cursor.executemany(
                ''' INSERT INTO "Videos" (id, name, playlist, category)
                    VALUES (%s, %s, %s, %s)
                ''',
                en_data
            )
            conn.commit()
        except psycopg.Error as err:
            print("Data insertion to test_table failed \n" + err)
        cursor.close()
        conn.close()

        # patch config
        test_conf = {'dbname': db, 'user': user}
        cls.mock_db_config = patch.dict(playlist_savior.conn_conf, test_conf)

    @classmethod
    def tearDownClass(cls):

        # drop test database
        sub.run(f'dropdb {db}', shell=True, text=True)
