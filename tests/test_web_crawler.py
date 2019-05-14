import unittest
import requests
from bs4 import BeautifulSoup, SoupStrainer
from scraper import web_crawler


# This tests my area_finder() function.
# I may look into the setUpClass() method as each test method uses the setUP()
# idk though. More learning required
class TestAreaFinder(unittest.TestCase):
    # This is to setup my request to feed links into area_finder()
    def setUp(self):
        request = requests.get('https://www.mountainproject.com/area/105929413/pawtuckaway')
        request.raise_for_status()

        mp_sidebar = SoupStrainer(class_='lef-nav-row')
        self.page_links = BeautifulSoup(request.text, parse_only=mp_sidebar, features='lxml')

    # Goes through once to verify its matching the correct link
    def test_area_finder_works(self):
        gen_obj = web_crawler.area_finder(self.page_links)
        result = next(gen_obj)

        self.assertEqual('https://www.mountainproject.com/area/106688566/area-51', result)

    # Goes through the generator object twice to verify that it pulls multiple links
    def test_area_finder_iteration(self):
        gen_obj = web_crawler.area_finder(self.page_links)
        next(gen_obj)
        result = next(gen_obj)

        self.assertEqual('https://www.mountainproject.com/area/105946021/blair-woods', result)


# Testing of my climb_finder() to make sure it finds climbs
class TestClimbFinderFindingClimbs(unittest.TestCase):
    # Sets up my requests to see if climb_finder() iterates through a page
    def setUp(self):
        request = requests.get('https://www.mountainproject.com/area/106964318/crack-boulder-area')
        request.raise_for_status()

        mp_sidebar = SoupStrainer(class_='mp-sidebar')
        self.page_links = BeautifulSoup(request.text, parse_only=mp_sidebar, features='lxml')

    # Tests that climb_finder() finds the climbs
    def test_climb_finder_works(self):
        gen_obj = web_crawler.climb_finder(self.page_links)
        result = next(gen_obj)

        self.assertEqual('https://www.mountainproject.com/route/105960892/bake-sale', result)

    # Tests a second iteration of climb_finder()
    def test_climb_finder_iteration(self):
        gen_obj = web_crawler.climb_finder(self.page_links)
        next(gen_obj)
        result = next(gen_obj)

        self.assertEqual('https://www.mountainproject.com/route/112895271/bayou-delta', result)


# This makes sure climb_finder() doesn't add non route links
class TestClimbFinderIgnoresNonRouteLinks(unittest.TestCase):
    # Setting up my requests for non route links
    def setUp(self):
        request = requests.get('https://www.mountainproject.com/area/105929413/pawtuckaway')
        request.raise_for_status()

        mp_sidebar = SoupStrainer(class_='mp-sidebar')
        self.page_links = BeautifulSoup(request.text, parse_only=mp_sidebar, features='lxml')

    # Tests that nothing gets put into the generator object when the links aren't a route
    def test_climb_finder_skipping_non_route_links(self):
        gen_obj = web_crawler.climb_finder(self.page_links)
        with self.assertRaises(StopIteration):
            next(gen_obj)


if __name__ == '__main__':
    unittest.main()
