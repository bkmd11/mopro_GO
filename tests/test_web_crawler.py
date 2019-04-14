"""I want to figure out how to do these tests without calling all the requests inside
my methods. setup() and tearDown() might be a good place to look"""


import unittest
import requests
from bs4 import BeautifulSoup, SoupStrainer
from scraper import web_crawler


class TestAreaFinder(unittest.TestCase):
    def test_area_finder_true(self):
        request = requests.get('https://www.mountainproject.com/area/105929413/pawtuckaway')
        request.raise_for_status()

        mp_sidebar = SoupStrainer(class_='mp-sidebar')
        page_links = BeautifulSoup(request.text, parse_only=mp_sidebar, features='lxml')

        result = web_crawler.area_finder(page_links)
        self.assertTrue(result)

    def test_area_finder_false(self):
        request = requests.get('https://www.mountainproject.com/route/106250047/four-hole')
        request.raise_for_status()

        mp_sidebar = SoupStrainer(class_='mp-sidebar')
        page_links = BeautifulSoup(request.text, parse_only=mp_sidebar, features='lxml')

        result = web_crawler.area_finder(page_links)
        self.assertFalse(result)


class TestClimbFinder(unittest.TestCase):
    def test_climb_finder_true(self):
        request = requests.get('https://www.mountainproject.com/route/106250047/four-hole')
        request.raise_for_status()

        mp_sidebar = SoupStrainer(class_='mp-sidebar')
        page_links = BeautifulSoup(request.text, parse_only=mp_sidebar, features='lxml')

        result = web_crawler.climb_finder(page_links)
        self.assertTrue(result)

    def test_climb_finder_false(self):
        request = requests.get('https://www.mountainproject.com/area/105929413/pawtuckaway')
        request.raise_for_status()

        mp_sidebar = SoupStrainer(class_='mp-sidebar')
        page_links = BeautifulSoup(request.text, parse_only=mp_sidebar, features='lxml')

        result = web_crawler.climb_finder(page_links)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
