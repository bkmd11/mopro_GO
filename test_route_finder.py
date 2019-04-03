#! python3

import unittest
from route_finder import regex


class TestRouteFinder(unittest.TestCase):
    def test_grade_regex(self):
        result = regex('5.11')

        self.assertIsNotNone(result.search('5.11A '))

    def test_grade_regex_escape_charecter(self):
        result = regex('5.11')
        self.assertIsNone(result.search('105911730'))


if __name__ == '__main__':
    unittest.main()
