import unittest
import testing.postgresql
import psycopg2

from route_finder_tool import select_climb_queries
from scraper_tool import load_to_db


BUILD_QUERY = '''CREATE TABLE IF NOT EXISTS climbs (
                                id SERIAL PRIMARY KEY,
                                climb_name TEXT NOT NULL,
                                url TEXT NOT NULL CONSTRAINT one_url UNIQUE,
                                grade TEXT NOT NULL)
                                ;
                            CREATE TABLE IF NOT EXISTS main_area (
                                id SERIAL PRIMARY KEY,
                                area TEXT NOT NULL CONSTRAINT one_area UNIQUE)
                                ;
                            CREATE TABLE IF NOT EXISTS sub_area (
                                id SERIAL PRIMARY KEY,
                                area TEXT NOT NULL,
                                climb_id INTEGER REFERENCES climbs(id),
                                area_id INTEGER REFERENCES main_area(id))
                                ;
                            CREATE TABLE IF NOT EXISTS climb_style (
                                id SERIAL PRIMARY KEY,
                                climb_style TEXT NOT NULL,
                                climb_id INTEGER REFERENCES climbs(id))
                                ;'''
postgres = testing.postgresql.Postgresql(cache_initialized_db=True)
connection = psycopg2.connect(**postgres.dsn())
connection.autocommit = True
cursor = connection.cursor()
cursor.execute(BUILD_QUERY)


class TestSelectClimbQueries(unittest.TestCase):

    def test_get_climbs_by_grade_query(self):
        result = select_climb_queries.get_main_areas_query(connection)

        self.assertIsInstance(result, list)

    # def test_execute_query(self):
    #    result = select_climb_queries.execute_query(self.connection)

    def tearDown(self):
        postgres.cleanup()
        postgres.stop()


if __name__ == '__main__':
    unittest.main()
