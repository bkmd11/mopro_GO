import unittest
import unittest.mock

from scraper_tool import async_scraper


class TestVerifyLink(unittest.TestCase):
    """Tests verify_link_input function"""
    def test_verify_link_accepts_area(self):
        """Tests that an actual link will pass"""
        with unittest.mock.patch('builtins.input', return_value='https://www.mountainproject.com/area/105867829/rumney'):
            result = async_scraper.verify_link_input()

        self.assertEqual(result, 'https://www.mountainproject.com/area/105867829/rumney')

    def test_verify_link_refuses_route(self):
        """Tests that it will refuse a mountain project route link"""
        with unittest.mock.patch('builtins.input', return_value='https://www.mountainproject.com/route/106137609/cream'):
            result = async_scraper.verify_link_input()

        self.assertIsNone(result)

    def test_verify_link_refuses_non_mountain_project_links(self):
        """Tests that a non mountain project link fails"""
        with unittest.mock.patch('builtins.input', return_value='https://www.backcountry.com/'):
            result = async_scraper.verify_link_input()

        self.assertIsNone(result)

    def test_verify_link_fails_for_typo(self):
        """Tests that it will fail for a typo in the link"""
        with unittest.mock.patch('builtins.input', return_value='https://www.mountainproject.com/arae/105867829/rumney'):
            result = async_scraper.verify_link_input()

        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
