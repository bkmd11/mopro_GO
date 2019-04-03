#! python3

import unittest
import route_finder


class TestRouteFinder(unittest.TestCase):
    def test_grade_regex_true(self):
        result = route_finder.regex('5.11')
        self.assertIsNotNone(result.search('5.11A '))

    def test_grade_regex_false(self):
        result = route_finder.regex('5.5')
        self.assertIsNone(result.search('5.12 '))

    def test_grade_regex_escape_character(self):
        result = route_finder.regex('5\.11')
        self.assertIsNone(result.search('105911730'))

    def test_area_regex_true(self):
        result = route_finder.regex('pawtuckaway')
        self.assertIsNotNone(result.search('pawtuckaway'))

    def test_area_regex_false(self):
        result = route_finder.regex('pawtuckaway')
        self.assertIsNone(result.search('cannon'))


if __name__ == '__main__':
    unittest.main()
