#! python3
import unittest
import json

from route_finder_tool import option_finder


# Testing that things actually work for this feature
class TestOptionFinder(unittest.TestCase):

    def setUp(self):
        with open('test.json', 'r') as file:
            self.json_file = json.load(file)

    # Testing area_options
    def test_area_options_pulls_all_options(self):
        result = option_finder.area_options(self.json_file)

        self.assertEqual(len(result), 2)

    # Tests that it will pull out different areas
    def test_area_options_gets_multiple_areas(self):
        result = option_finder.area_options(self.json_file)

        self.assertIn('pawtuckaway', result)
        self.assertIn('cannon-cliff', result)

    # Testing that the sub_area options works
    def test_sub_area_options_works(self):
        result = option_finder.sub_area_options([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

        self.assertEqual(result, [3, 6, 9])

    # Tests that it indexes my list correctly
    def test_sub_area_options_returns_right_thing(self):
        result = option_finder.sub_area_options([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

        self.assertEqual(result, [3, 6, 9])

    # Tests my grade_option finder pulls the right grade in a given area
    def test_grade_options_area(self):
        result = option_finder.grade_options([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

        self.assertEqual(result, [3, 6, 9])

    # Tests that grade_options will only pull from one sub_area under a given area
    def test_grade_options_sub_area(self):
        result = option_finder.grade_options([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

        self.assertEqual(result, [3, 6, 9])

    # Tests that it will pull all the grade options from an area
    def test_grade_options_returns_multiple_grades(self):
        result = option_finder.grade_options([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

        self.assertEqual(result, [3, 6, 9])


if __name__ == '__main__':
    unittest.main()
