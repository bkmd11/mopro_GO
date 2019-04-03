#! python3

import unittest
import route_finder


class TestRouteFinder(unittest.TestCase):
    def test_grade_regex(self):
        result = route_finder.regex('5.11')

        self.assertIsNotNone(result.search('5.11A '))

    def test_grade_regex_escape_character(self):
        result = route_finder.regex('5\.11')
        self.assertIsNone(result.search('105911730'))

    def TestFindByCriteria(self):
        list_of_climbs = ['pawtuckaway', 'rumney']
        result = route_finder.find_by_criteria(list_of_climbs)

        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
