import asynctest

import sys
from io import StringIO
from aiohttp import ClientSession
from colorama import Fore

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
        result = self.loop.run_until_complete(
            page_search.list_maker('https://www.mountainproject.com/route/107235878/yellow-zonkers',
                                   request_text,
                                   'ow'))

        self.assertEqual(['https://www.mountainproject.com/route/107235878/yellow-zonkers',
                          'Yellow Zonkers',
                          'pawtuckaway',
                          'upper-cliff',
                          r'5.8+',
                          'ow'], result)


class TestGetRequest(asynctest.TestCase):
    """Testing get request works"""

    async def setUp(self):
        self.session = ClientSession()

    async def test_get_request(self):
        result = await page_search.page_request('https://www.mountainproject.com/route/107235878/yellow-zonkers',
                                                self.session)

        self.assertIsInstance(result, str)

    async def tearDown(self):
        await self.session.close()


class TestParse(asynctest.TestCase):
    """Testing parse finds off widths and adds to the list"""

    async def setUp(self):
        self.session = ClientSession()

    async def test_parse_prints_awesomeness_correctly_ow(self):
        output = StringIO()
        sys.stdout = output
        result = await page_search.parse('https://www.mountainproject.com/route/107235878/yellow-zonkers', self.session,
                                         'ow')

        self.assertEqual(output.getvalue(),
                         f'{Fore.CYAN}searching https://www.mountainproject.com/route/107235878/yellow-zonkers'
                         f'\nawesomeness found!\n')
        self.assertEqual(len(result[0]), 1)

    async def test_parse_ignores_lame_climbs_ow(self):
        output = StringIO()
        sys.stdout = output
        result = await page_search.parse('https://www.mountainproject.com/route/117989364/beanstalk',
                                         self.session, 'ow')

        self.assertEqual(len(result[0]), 0)

    async def test_parse_prints_awesomeness_correctly_fist(self):
        output = StringIO()
        sys.stdout = output
        result = await page_search.parse('https://www.mountainproject.com/route/107607462/the-raptor-roofs', self.session,
                                         'fist')

        self.assertEqual(output.getvalue(),
                         f'{Fore.CYAN}searching https://www.mountainproject.com/route/107607462/the-raptor-roofs'
                         f'\nawesomeness found!\n')
        self.assertEqual(len(result[0]), 1)

    async def test_parse_ignores_lame_climbs_fist(self):
        output = StringIO()
        sys.stdout = output
        result = await page_search.parse('https://www.mountainproject.com/route/117989364/beanstalk',
                                         self.session, 'fist')

        self.assertEqual(len(result[0]), 0)

    async def tearDown(self):
        await self.session.close()


class TestMain(asynctest.TestCase):
    """Testing the main function"""

    async def setUp(self):
        self.session = ClientSession()

    async def test_main(self):
        result = await page_search.page_search_main(['https://www.mountainproject.com/route/117989364/beanstalk',
                                                     'https://www.mountainproject.com/route/106207758/far-out-jam',
                                                     'https://www.mountainproject.com/route/105995594/bean-pole',
                                                     'https://www.mountainproject.com/route/107235878/yellow-zonkers'],
                                                    self.session, 'ow')

        self.assertEqual(result, [['https://www.mountainproject.com/route/106207758/far-out-jam',
                                   'Far Out Jam',
                                   'pawtuckaway',
                                   'upper-cliff',
                                   '5.9',
                                   'ow'],
                                  ['https://www.mountainproject.com/route/107235878/yellow-zonkers',
                                   'Yellow Zonkers',
                                   'pawtuckaway',
                                   'upper-cliff',
                                   '5.8+',
                                   'ow']])

    async def tearDown(self):
        await self.session.close()


if __name__ == '__main__':
    asynctest.main()
