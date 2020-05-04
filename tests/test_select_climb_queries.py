import unittest
import testing.postgresql

import json

from route_finder_tool import select_climb_queries
'''
Postgres = testing.postgresql.PostgresqlFactory(cache_initialized=True,
                                                copy_data_from=r'C:\Program Files\PostgreSQL\12\data\base\32950')


def tear_down_module():
    Postgres.clear_cache()


class TestSelectClimbQueries(unittest.TestCase):
    def setUp(self):
        self.postgresql = Postgres()

        self.connection = self.postgresql

    def tearDown(self):
        self.postgresql.stop()

   # def test_get_climbs_by_grade_query(self):
    #    result = select_climb_queries.get_main_areas_query(self.connection)

     #   self.assertEqual(result, 'spam')
   # def test_execute_query(self):
    #    result = select_climb_queries.execute_query(self.connection,
     #                                               )

if __name__ == '__main__':
    unittest.main()
'''