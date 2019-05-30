import unittest
import requests
from bs4 import BeautifulSoup, SoupStrainer

from scraper_tool import page_search


# This tests page_search functions for off_width regex
class TestRegexSearchOffWidth(unittest.TestCase):
    def setUp(self):
        self.res = requests.get('https://www.mountainproject.com/route/105941462/climbers-corner')
        self.res.raise_for_status()

        # Pulls out just the description
        strainer = SoupStrainer(class_='col-xs-12')
        climb_text = BeautifulSoup(self.res.text, parse_only=strainer, features='lxml')
        self.description = climb_text.find_all(class_='fr-view')

    # Tests that it finds off-width
    def test_regex_search_off_width(self):
        result = page_search.regex_search(self.description)
        self.assertEqual(result, 'send_it')

    # Tests that it finds the right grade.
    def test_grade_finder(self):
        result = page_search.grade_finder(self.res)
        self.assertEqual(result, '5.10 ')

    # Tests that it pulls what I want out of the navigation tree
    def test_nav_tree(self):
        result = page_search.navigation_tree(self.res)
        self.assertEqual(result, ["pawtuckaway", "upper-cliff"])

    # This is an integration test of my list_maker()
    def test_list_maker(self):
        result = page_search.list_maker("https://www.mountainproject.com/route/105941462/climbers-corner", self.res)
        self.assertEqual(result,
                         ["https://www.mountainproject.com/route/105941462/climbers-corner", "pawtuckaway",
                          "upper-cliff", "5.10 "])


if __name__ == '__main__':
    unittest.main()
