""" This set of tests is integration testing of my database building queries and of my selecting queries.
I assume there must be a better way to go about testing a database, but this is the only way I could figure out.
"""

import unittest
import testing.postgresql
import psycopg2
import json

from route_finder_tool import select_climb_queries
from scraper_tool import load_to_db

with open(r'C:\Users\Brian Kendall\Desktop\off_width_scraper\tests\test_database_data.json', 'r') as file:
    test_data = json.load(file)

postgres = testing.postgresql.Postgresql()
connection = psycopg2.connect(**postgres.dsn())

connection.autocommit = True
cursor = connection.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS climb_style (
                    id SERIAL PRIMARY KEY,
                    climb_style TEXT NOT NULL CONSTRAINT one_style UNIQUE)
                    ;
                CREATE TABLE IF NOT EXISTS climbs (
                    id SERIAL PRIMARY KEY,
                    climb_name TEXT NOT NULL,
                    url TEXT NOT NULL CONSTRAINT one_url UNIQUE,
                    grade TEXT NOT NULL)
                    ;
                CREATE TABLE IF NOT EXISTS style_guide (
                    climb_name INTEGER REFERENCES climbs(id),
                    style INTEGER REFERENCES climb_style(id),
                    PRIMARY KEY (climb_name, style))
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
                                    ''')


class TestLoadToDB(unittest.TestCase):
    # TODO: check against multiple styles
    def test_1_style_query(self):
        result = load_to_db.style_query((test_data[0][5],), connection)

        self.assertIsInstance(result, int)

    def test_1_style_query_wont_repeat(self):
        result = load_to_db.style_query((test_data[0][5],), connection)

        self.assertEqual(result, 1)

    def test_insert_climb(self):
        result = load_to_db.insert_climb((test_data[0][1], test_data[0][0], test_data[0][4]), connection)

        self.assertIsInstance(result, int)

    def test_insert_climb_wont_repeat(self):
        result = load_to_db.insert_climb((test_data[0][1], test_data[0][0], test_data[0][4]), connection)

        self.assertEqual(result, 1)

    def test_insert_main_area(self):
        result = load_to_db.insert_main_area((test_data[0][2],), connection)

        self.assertIsInstance(result, int)

    def test_main_area_wont_repeat(self):
        result = load_to_db.insert_main_area((test_data[0][2],), connection)

        self.assertEqual(result, 1)

    def test_sub_area_query(self):
        result = load_to_db.sub_area_query((test_data[0][3], 1, 1), connection)

        self.assertIsInstance(result, int)

    def test_insert_style_guide_query(self):
        result = load_to_db.insert_style_guide_query((1, 1), connection)

        self.assertEqual(result, 1)

    def test_insert_style_guide_query_wont_repeat(self):
        result = load_to_db.insert_style_guide_query((1, 1), connection)

        self.assertEqual(result, '(1,1)')


class TestSelectClimbQueries(unittest.TestCase):

    def test_get_main_areas_query(self):
        result = select_climb_queries.get_main_areas_query(connection)

        self.assertEqual(result, [('pawtuckaway',)])

    def test_get_sub_areas_query(self):
        result = select_climb_queries.get_sub_areas_query(connection, 'pawtuckaway')

        self.assertEqual(result, [('boulder-natural',)])

    def test_get_main_area_id(self):
        result = select_climb_queries.get_main_area_id_query(connection, 'pawtuckaway')

        self.assertEqual(result, [(1,)])

    def test_get_climbs_by_sub_area(self):
        result = select_climb_queries.get_climbs_by_sub_area(connection, 'boulder-natural')

        self.assertEqual(result, [('Fritz\'s Demise', 'V0 ')])

    def test_get_climb_url(self):
        result = select_climb_queries.get_climb_url_query(connection, 'Fritz\'s Demise')

        self.assertEqual(result, [('https://www.mountainproject.com/route/106306113/fritzs-demise',)])


if __name__ == '__main__':
    unittest.main()
