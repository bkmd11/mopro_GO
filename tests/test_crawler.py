import unittest
import asynctest

from aiohttp import ClientSession
import requests
from bs4 import BeautifulSoup, SoupStrainer

from scraper_tool import crawler


def setUpModule():
    session = ClientSession()


class TestAreaFinder(asynctest.TestCase):
    def setUp(self):
        self.html = requests.get('https://www.mountainproject.com/area/105929413/pawtuckaway')
        self.html_text = self.html.text
        self.mp_sidebar = SoupStrainer(class_='mp-sidebar')
        self.bs4_parsed_area = BeautifulSoup(self.html_text, parse_only=self.mp_sidebar, features='lxml')

    def test_area_finder_ignores_route(self):
        result = self.loop.run_until_complete(crawler.area_finder(self.bs4_parsed_area))

        for i in result:
            self.assertNotIn('com/route', i)

    def test_area_finder_ignores_map(self):
        result = self.loop.run_until_complete(crawler.area_finder(self.bs4_parsed_area))

        for i in result:
            self.assertNotIn('com/map', i)

    def test_area_finder_finds_area(self):
        result = self.loop.run_until_complete(crawler.area_finder(self.bs4_parsed_area))

        for i in result:
            self.assertIn('com/area', i)


class TestClimbFinder(asynctest.TestCase):
    def setUp(self):
        self.html = requests.get('https://www.mountainproject.com/area/106523382/the-split-boulder')
        self.html_text = self.html.text
        self.mp_sidebar = SoupStrainer(class_='mp-sidebar')
        self.bs4_parsed_route = BeautifulSoup(self.html_text, parse_only=self.mp_sidebar, features='lxml')

    def test_climb_finder_ignores_map(self):
        result = self.loop.run_until_complete(crawler.climb_finder(self.bs4_parsed_route))

        for i in result:
            self.assertNotIn('com/map', i)

    def test_climb_finder_finds_climb(self):
        result = self.loop.run_until_complete(crawler.climb_finder(self.bs4_parsed_route))

        for i in result:
            self.assertIn('com/route', i)


class TestGetRequest(asynctest.TestCase):
    async def setUp(self):
        self.session = ClientSession()

    async def test_get_request_returns_string(self):
        result = await crawler.get_request('https://www.mountainproject.com/area/106688566/area-51',
                                           self.session)

        self.assertIsInstance(result, str)

    async def tearDown(self):
        await self.session.close()


class TestParseClimbOrArea(asynctest.TestCase):
    async def setUp(self):
        self.session = ClientSession()

    async def test_parse_returns_area(self):
        result = await crawler.parse_climb_or_area('https://www.mountainproject.com/area/106688566/area-51',
                                                   self.session)

        self.assertIn('area', result)

    async def test_parse_does_not_return_area(self):
        result = await crawler.parse_climb_or_area('https://www.mountainproject.com/route/106306113/fritzs-demise',
                                                   self.session)

        self.assertNotIn('area', result)

    async def test_parse_returns_climb(self):
        result = await crawler.parse_climb_or_area('https://www.mountainproject.com/route/106306113/fritzs-demise',
                                                   self.session)

        self.assertIn('climb', result)
        self.assertTrue(len(result[1]) > 0)

    async def test_parse_ignores_map_link(self):
        result = await crawler.parse_climb_or_area('https://www.mountainproject.com/map/106523382/the-split-boulder',
                                                   self.session)

        self.assertIn('climb', result)
        self.assertTrue(len(result[1]) == 0)

    async def tearDown(self):
        await self.session.close()


class TestWebCrawlerMain(asynctest.TestCase):
    async def setUp(self):
        self.session = ClientSession()

    async def test_main(self):
        result = await crawler.web_crawler_main('https://www.mountainproject.com/area/106523382/the-split-boulder',
                                                self.session)

        self.assertEqual(result, ['https://www.mountainproject.com/route/106104812/anorexorcist',
                                  'https://www.mountainproject.com/route/106041614/bones-to-bits',
                                  'https://www.mountainproject.com/route/112138886/bulemia',
                                  'https://www.mountainproject.com/route/106118276/confident-man',
                                  'https://www.mountainproject.com/route/112272699/flakes-of-life',
                                  'https://www.mountainproject.com/route/106118269/halcyon',
                                  'https://www.mountainproject.com/route/109648266/jaded',
                                  'https://www.mountainproject.com/route/106632408/the-morgue',
                                  'https://www.mountainproject.com/route/106104859/my-little-pony',
                                  'https://www.mountainproject.com/route/112036656/outback',
                                  'https://www.mountainproject.com/route/106632399/rios-problem',
                                  'https://www.mountainproject.com/route/106104828/stegasaurus'])

    async def tearDown(self):
        await self.session.close()


if __name__ == '__main__':
    unittest.main(buffer=False)
