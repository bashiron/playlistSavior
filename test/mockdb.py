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
        # conn = psycopg.connect(f'dbname=postgres user={user}')
        # cursor = conn.cursor()
        # try:
        #     cursor.execute("DROP DATABASE {}".format(db))
        #     cursor.close()
        #     conn.close()
        #     print("DB dropped")
        # except psycopg.Error as err:
        #     print("{} - {}".format(db, err))

        # create database
        sub.run(f'createdb {db}', shell=True, text=True)
        # conn = psycopg.connect(f'dbname=postgres user={user}')
        # cursor = conn.cursor()
        # try:
        #     cursor.execute(
        #         "CREATE DATABASE {} WITH ENCODING 'UTF8'".format(db))
        #     cursor.close()
        #     conn.close()
        # except psycopg.Error as err:
        #     print("Failed creating database: {}".format(err))
        #     exit(1)

        # create database structure
        sub.run(f'pg_dump playlist -s | psql {db}', shell=True, text=True, capture_output=True)

        # insert data
        conn = psycopg.connect(f'dbname={db} user={user}')
        cursor = conn.cursor()
        try:
            cursor.execute(
                ''' INSERT INTO "Videos" (id, name, playlist, category)
                    VALUES (%s, %s, %s, %s)
                ''',
                (1, 'Incursione', '{smash}', '{ost}')
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
        # conn = psycopg.connect(f'dbname={db} user={user}')
        # cursor = conn.cursor()
        # try:
        #     cursor.execute('DROP DATABASE {}'.format(db))
        #     conn.commit()
        #     cursor.close()
        # except psycopg.Error as err:
        #     print("Database {} does not exist. Dropping db failed".format(db))
        # conn.close()
