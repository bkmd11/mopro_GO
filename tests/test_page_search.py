import unittest
import requests
from bs4 import BeautifulSoup, SoupStrainer

from scraper import page_search


class TestRegexSearch(unittest.TestCase):
    def setUp(self, i):
        self.test_list = ['https://www.mountainproject.com/route/105945178/lakeside-jam',
                          'https://www.mountainproject.com/route/106041614/bones-to-bits',
                          'https://www.mountainproject.com/route/106991711/squeeze-play',
                          'https://www.mountainproject.com/route/110679886/the-edge',
                          'https://www.mountainproject.com/route/111819525/friend-of-the-devil'
                          ]
        res = requests.get(i)
        res.raise_for_status()

        strainer = SoupStrainer(class_='col-xs-12')
        climb_text = BeautifulSoup(res.text, parse_only=strainer, features='lxml')
        self.description = climb_text.find_all(class_='fr-view')

    def test_regex_offwidth(self):
        result = page_search.regex_search(self.setUp(i='https://www.mountainproject.com/route/105945178/lakeside-jam'))

        self.assertIsNotNone(result)
