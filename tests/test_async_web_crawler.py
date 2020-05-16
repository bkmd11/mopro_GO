import unittest
import asynctest
import asyncio

import json

from scraper_tool import async_web_crawler


with open(r'C:\Users\Brian Kendall\Desktop\off_width_scraper\tests\test_database_data.json', 'r') as file:
    mountain_proj_list = json.load(file)


class TestAreaFinder(asynctest.TestCase):
    def test_area_finder_ignores_route(self):
        result = self.loop.run_until_complete(async_web_crawler.area_finder(mountain_proj_list))

        for i in result:
            self.assertNotIn('com/route', i)

    def test_area_finder_ignores_map(self):
        result = self.loop.run_until_complete(async_web_crawler.area_finder(mountain_proj_list))

        for i in result:
            self.assertNotIn('com/map', i)

    def test_area_finder_finds_area(self):
        result = self.loop.run_until_complete(async_web_crawler.area_finder(mountain_proj_list))

        for i in result:
            self.assertIn('com/area', i)


class TestClimbFinder(asynctest.TestCase):
    def test_climb_finder_ignores_map(self):
        result = self.loop.run_until_complete(async_web_crawler.climb_finder(mountain_proj_list))

        for i in result:
            self.assertNotIn('com/map', i)

    def test_climb_finder_finds_climb(self):
        result = self.loop.run_until_complete(async_web_crawler.climb_finder(mountain_proj_list))

        for i in result:
            self.assertIn('com/route', i)



if __name__ == '__main__':
    unittest.main()
