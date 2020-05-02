import unittest

import json

from route_finder_tool import route_finder_gui
from route_finder_tool import select_climb_queries


class TestLoadClimb(unittest.TestCase):
    def setUp(self):
        with open(r'C:\Users\Brian Kendall\Desktop\off_width_scraper\db_credentials.json', 'r') as file:
            credentials = json.load(file)
        connection = select_climb_queries.create_connection(credentials[0], credentials[1])

    def test_load_climb(self):
        pass


if __name__ == '__main__':
    unittest.main()
