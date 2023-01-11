from playlist_savior import *
from mockdb import MockDB

db = 'test_playlist'
user = 'bashiron'

class TestSavior(MockDB):

    def test_db_write(self):
        with self.mock_db_config:
            savior = Savior()
            with psycopg.connect(f'dbname={db} user={user}') as conn:
                with conn.cursor() as cursor:
                    cursor.execute('SELECT * FROM "Videos"')
                    vids = cursor.fetchall()
                    self.assertTrue(True)

    def test_db_read(self):
        with self.mock_db_config:
            self.assertTrue(True)
