import asynctest

from scraper_tool import page_search

with open(r'C:\Users\Brian Kendall\Desktop\off_width_scraper\tests\test_request_text.txt', 'r') as file:
    request_text = file.read()


class TestGetClimbDetails(asynctest.TestCase):
    """Testing all of the features to find climb details"""
    def test_climb_name(self):
        """Testing that climb name is found and returned correctly"""
        result = self.loop.run_until_complete(page_search.climb_name(request_text))

        self.assertEqual('Yellow Zonkers', result)

    def test_grade_finder(self):
        """Testing the the grade gets found and returned correctly"""
        result = self.loop.run_until_complete(page_search.grade_finder(request_text))

        self.assertEqual(r'5.8+', result)

    def test_navigation_tree(self):
        """Testing that the navigation tree for location gets pulled correctly"""
        result = self.loop.run_until_complete(page_search.navigation_tree(request_text))

        self.assertEqual(['pawtuckaway', 'upper-cliff'], result)

    def test_list_maker(self):
        """Integration test for the list maker function"""
        result = self.loop.run_until_complete(page_search.list_maker('https://www.mountainproject.com/route/107235878/yellow-zonkers',
                                                                     request_text,
                                                                           'ow'))

        self.assertEqual(['https://www.mountainproject.com/route/107235878/yellow-zonkers',
                          'Yellow Zonkers',
                          'pawtuckaway',
                          'upper-cliff',
                          r'5.8+',
                          'ow'], result)


if __name__ == '__main__':
    asynctest.main()