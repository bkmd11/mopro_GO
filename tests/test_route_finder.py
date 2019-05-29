"""I need to figure out how to run tests when a sys.arg is
required"""

import unittest

from route_finder import route_finder


# Testing of my regex searching function
class TestRouteFinderRegex(unittest.TestCase):
    # Tests that it finds grades with extra things after
    def test_grade_regex_true(self):
        result = route_finder.regex('5.11')
        self.assertIsNotNone(result.search('5.11A '))

    # Tests that it fails when there is not a match
    def test_grade_regex_false(self):
        result = route_finder.regex('5.5')
        self.assertIsNone(result.search('5.12 '))

    # Tests that adding an escape character to block '.' works
    def test_grade_regex_escape_character(self):
        result = route_finder.regex('5.11')
        self.assertIsNone(result.search('105911730'))

    # Testing that it matches the string of an area
    def test_area_regex_true(self):
        result = route_finder.regex('pawtuckaway')
        self.assertIsNotNone(result.search('pawtuckaway'))

    # Testing that it fails when a regex isn't a match
    def test_area_regex_false(self):
        result = route_finder.regex('pawtuckaway')
        self.assertIsNone(result.search('cannon'))

    # Tests that the regex is case insensitive
    def test_area_regex_ignore_case(self):
        result = route_finder.regex('PawtuCKaway')
        self.assertIsNotNone(result.search('pawtuckaway'))

    # Tests to see if case matters in item being searched
    def test_area_regex_ignore_case_in_item(self):
        result = route_finder.regex('cannon')
        self.assertIsNotNone(result.search('CannoN'))


# Tests escape_character() function
class TestEscapeCharacter(unittest.TestCase):

    # Tests that it works
    def test_escape_character_works(self):
        result = route_finder.escape_character('5.12')
        self.assertEqual(result, '5\\.12')

    # Tests that it won't add escape character if its not needed
    def test_escape_character_not_added(self):
        result = route_finder.escape_character('spam')
        self.assertEqual(result, 'spam')

    # Tests that it will add multiple escape characters
    def test_escape_character_catches_all_dots(self):
        result = route_finder.escape_character('5.11.3')
        self.assertEqual(result, '5\\.11\\.3')

    # Tests to see what happens if the escape characters get added as input
    def test_escape_characters_already_added(self):
        result = route_finder.escape_character('5\\.11')
        self.assertEqual(result, '5\\.11')


if __name__ == '__main__':
    unittest.main()
