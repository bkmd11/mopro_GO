import unittest
import requests
from bs4 import BeautifulSoup, SoupStrainer
import mountain_project


class TestAreaFinder(unittest.TestCase):
    def test_area_finder_true(self):
        request = requests.get('https://www.mountainproject.com/area/105929413/pawtuckaway')
        request.raise_for_status()

        mp_sidebar = SoupStrainer(class_='mp-sidebar')
        page_links = BeautifulSoup(request.text, parse_only=mp_sidebar, features='lxml')

        result = mountain_project.area_finder(page_links)
        self.assertTrue(result)

    def test_area_finder_false(self):
        request = requests.get('https://www.mountainproject.com/route/106250047/four-hole')
        request.raise_for_status()

        mp_sidebar = SoupStrainer(class_='mp-sidebar')
        page_links = BeautifulSoup(request.text, parse_only=mp_sidebar, features='lxml')

        result = mountain_project.area_finder(page_links)
        self.assertFalse(result)


if __name__== '__main__':
    unittest.main()