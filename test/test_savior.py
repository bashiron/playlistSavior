import playlist_savior
from mockdb import MockDB
from unittest.mock import patch

class TestUtils(MockDB):

    def test_db_write(self):
        with self.mock_db_config:
            self.assertEqual(1, 1)

    def test_db_read(self):
        with self.mock_db_config:
            self.assertTrue(True)
