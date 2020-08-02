import unittest
import unittest.mock

import mopro_scraper


class TestVerifyLink(unittest.TestCase):
    """Tests verify_link_input function"""
    def test_verify_link_accepts_area(self):
        """Tests that an actual link will pass"""
        with unittest.mock.patch('builtins.input', return_value='https://www.mountainproject.com/area/105867829/rumney'):
            result = mopro_scraper.verify_link_input()

        self.assertEqual(result, 'https://www.mountainproject.com/area/105867829/rumney')

    def test_verify_link_refuses_route(self):
        """Tests that it will refuse a mountain project route link"""
        with unittest.mock.patch('builtins.input', return_value='https://www.mountainproject.com/route/106137609/cream'):
            result = mopro_scraper.verify_link_input()

        self.assertIsNone(result)

    def test_verify_link_refuses_non_mountain_project_links(self):
        """Tests that a non mountain project link fails"""
        with unittest.mock.patch('builtins.input', return_value='https://www.backcountry.com/'):
            result = mopro_scraper.verify_link_input()

        self.assertIsNone(result)

    def test_verify_link_fails_for_typo(self):
        """Tests that it will fail for a typo in the link"""
        with unittest.mock.patch('builtins.input', return_value='https://www.mountainproject.com/arae/105867829/rumney'):
            result = mopro_scraper.verify_link_input()

        self.assertIsNone(result)


class TestVerifyRegex(unittest.TestCase):
    """Tests that verify_regex_input verifies correctly"""
    def test_verify_regex_ow(self):
        """Tests that it will accept ow"""
        with unittest.mock.patch('builtins.input', return_value='ow'):
            result = mopro_scraper.verify_regex_input()

        self.assertEqual(result, 'ow')

    def test_verify_regex_finger(self):
        """Tests that it will accept finger"""
        with unittest.mock.patch('builtins.input', return_value='finger'):
            result = mopro_scraper.verify_regex_input()

        self.assertEqual(result, 'finger')

    def test_verify_fist(self):
        """Tests that it will accept fist"""
        with unittest.mock.patch('builtins.input', return_value='fist'):
            result = mopro_scraper.verify_regex_input()

        self.assertEqual(result, 'fist')

    def test_verify_ignores_case(self):
        """Tests that it ignores case"""
        with unittest.mock.patch('builtins.input', return_value='fISt'):
            result = mopro_scraper.verify_regex_input()

        self.assertEqual(result, 'fist')


if __name__ == '__main__':
    unittest.main()
