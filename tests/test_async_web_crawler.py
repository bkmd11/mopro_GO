import unittest
import asynctest

import json
from aiohttp import ClientSession

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


class TestGetRequest(asynctest.TestCase):
    async def setUp(self):
        self.session = ClientSession()

    async def test_get_request_returns_string(self):
        result = await async_web_crawler.get_request('https://www.mountainproject.com/area/106688566/area-51',
                                                     self.session)

        self.assertIsInstance(result, str)

    async def tearDown(self):
        await self.session.close()


class TestParseClimbOrArea(asynctest.TestCase):
    async def setUp(self):
        self.session = ClientSession()

    async def test_parse_returns_area(self):
        result = await async_web_crawler.parse_climb_or_area('https://www.mountainproject.com/area/106688566/area-51',
                                                             self.session)
        self.assertIn('area', result)

    async def test_parse_returns_climb(self):
        result = await async_web_crawler.parse_climb_or_area('https://www.mountainproject.com/map/107112720/bermuda-triangle-boulder',
                                                             self.session)

        self.assertIn('climb', result)

    async def tearDown(self):
        await self.session.close()


if __name__ == '__main__':
    unittest.main(buffer=True)
