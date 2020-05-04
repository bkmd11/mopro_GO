import unittest
import testing.postgresql

from scraper_tool import load_to_db

"""
Postgres = testing.postgresql.PostgresqlFactory(cache_initialized=True)


class TestBuildQuerries(unittest.TestCase):
    def setUp(self):
        self.postgresql = Postgres()

        self.connection = self.postgresql

    def tearDown(self):
        self.postgresql.stop()

   # def test_insert_climb(self):
    #    result = load_to_db.insert_climb(('spam', 'spam.com', 3), self.connection)

     #   self.assertEqual(result, 1)

    def test_execute_query(self):
        query = '''SELECT
                    COLUMN_NAME
                FROM
                    information_schema.COLUMNS'''
        result = load_to_db.execute_query(self.connection, query)

        self.assertTrue(result)





if __name__ == '__main__':
    unittest.main()
"""