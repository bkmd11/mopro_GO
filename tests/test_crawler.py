import unittest
import asynctest

from aiohttp import ClientSession
import requests
from bs4 import BeautifulSoup, SoupStrainer

from scraper_tool import crawler


class TestAreaFinder(asynctest.TestCase):
    def setUp(self):
        self.html = requests.get('https://www.mountainproject.com/area/105929413/pawtuckaway')
        self.html_text = self.html.text
        self.mp_sidebar = SoupStrainer(class_='mp-sidebar')
        self.bs4_parsed_area = BeautifulSoup(self.html_text, parse_only=self.mp_sidebar, features='lxml')

    def test_area_finder_ignores_route(self):
        result = self.loop.run_until_complete(crawler.area_finder(self.bs4_parsed_area))

        for i in result:
            self.assertNotIn('com/route', i)

    def test_area_finder_ignores_map(self):
        result = self.loop.run_until_complete(crawler.area_finder(self.bs4_parsed_area))

        for i in result:
            self.assertNotIn('com/map', i)

    def test_area_finder_finds_area(self):
        result = self.loop.run_until_complete(crawler.area_finder(self.bs4_parsed_area))

        for i in result:
            self.assertIn('com/area', i)


class TestClimbFinder(asynctest.TestCase):
    def setUp(self):
        self.html = requests.get('https://www.mountainproject.com/area/106523382/the-split-boulder')
        self.html_text = self.html.text
        self.mp_sidebar = SoupStrainer(class_='mp-sidebar')
        self.bs4_parsed_route = BeautifulSoup(self.html_text, parse_only=self.mp_sidebar, features='lxml')

    def test_climb_finder_ignores_map(self):
        result = self.loop.run_until_complete(crawler.climb_finder(self.bs4_parsed_route))

        for i in result:
            self.assertNotIn('com/map', i)

    def test_climb_finder_finds_climb(self):
        result = self.loop.run_until_complete(crawler.climb_finder(self.bs4_parsed_route))

        for i in result:
            self.assertIn('com/route', i)


class TestGetRequest(asynctest.TestCase):
    async def setUp(self):
        self.session = ClientSession()

    async def test_get_request_returns_string(self):
        result = await crawler.get_request('https://www.mountainproject.com/area/106688566/area-51', self.session)

        self.assertIsInstance(result, str)

    async def tearDown(self):
        await self.session.close()


class TestParseClimbOrArea(asynctest.TestCase):
    async def setUp(self):
        self.session = ClientSession()

    async def test_parse_returns_area(self):
        result = await crawler.parse_climb_or_area('https://www.mountainproject.com/area/106688566/area-51',
                                                   self.session)

        self.assertIn('area', result)

    async def test_parse_does_not_return_area(self):
        result = await crawler.parse_climb_or_area('https://www.mountainproject.com/route/106306113/fritzs-demise',
                                                   self.session)

        self.assertNotIn('area', result)

    async def test_parse_returns_climb(self):
        result = await crawler.parse_climb_or_area('https://www.mountainproject.com/route/106306113/fritzs-demise',
                                                   self.session)

        self.assertIn('climb', result)
        self.assertTrue(len(result[1]) > 0)

    async def test_parse_ignores_map_link(self):
        result = await crawler.parse_climb_or_area('https://www.mountainproject.com/map/106523382/the-split-boulder',
                                                   self.session)

        self.assertIn('climb', result)
        self.assertTrue(len(result[1]) == 0)

    async def tearDown(self):
        await self.session.close()


class TestWebCrawlerMain(asynctest.TestCase):
    async def setUp(self):
        self.session = ClientSession()

    async def test_main(self):
        result = await crawler.web_crawler_main('https://www.mountainproject.com/area/106523382/the-split-boulder',
                                                self.session)

        self.assertEqual(result, ['https://www.mountainproject.com/route/106104812/anorexorcist',
                                  'https://www.mountainproject.com/route/106041614/bones-to-bits',
                                  'https://www.mountainproject.com/route/112138886/bulemia',
                                  'https://www.mountainproject.com/route/106118276/confident-man',
                                  'https://www.mountainproject.com/route/112272699/flakes-of-life',
                                  'https://www.mountainproject.com/route/106118269/halcyon',
                                  'https://www.mountainproject.com/route/109648266/jaded',
                                  'https://www.mountainproject.com/route/106632408/the-morgue',
                                  'https://www.mountainproject.com/route/106104859/my-little-pony',
                                  'https://www.mountainproject.com/route/112036656/outback',
                                  'https://www.mountainproject.com/route/106632399/rios-problem',
                                  'https://www.mountainproject.com/route/106104828/stegasaurus'])

    async def test_main_fully_works(self):
        result = await crawler.web_crawler_main('https://www.mountainproject.com/area/106523360/boulder-natural',
                                                self.session)

        self.assertEqual(result, ['https://www.mountainproject.com/route/106296132/barnyard-crack',
                                  'https://www.mountainproject.com/route/106528351/bought-the-farm',
                                  'https://www.mountainproject.com/route/106285021/classic-crack',
                                  'https://www.mountainproject.com/route/106528439/the-cooper-problem',
                                  'https://www.mountainproject.com/route/106528409/hay-fever',
                                  'https://www.mountainproject.com/route/106528378/plowed',
                                  'https://www.mountainproject.com/route/106528475/unnamed-2',
                                  'https://www.mountainproject.com/route/106528458/unnamed-aka-jeds-arete',
                                  'https://www.mountainproject.com/route/106528402/whitewash',
                                  'https://www.mountainproject.com/route/106250020/aroma-therapy',
                                  'https://www.mountainproject.com/route/105960793/bolt-on-top',
                                  'https://www.mountainproject.com/route/111938173/conceptual-therapy',
                                  'https://www.mountainproject.com/route/108415531/dilemma-tree',
                                  'https://www.mountainproject.com/route/105960798/gene-therapy',
                                  'https://www.mountainproject.com/route/111029537/grab-the-junk',
                                  'https://www.mountainproject.com/route/106206889/realms-regions-and-concepts',
                                  'https://www.mountainproject.com/route/106279158/runaway',
                                  'https://www.mountainproject.com/route/105960789/sandy-landing',
                                  'https://www.mountainproject.com/route/106621187/splendid',
                                  'https://www.mountainproject.com/route/111088314/crank',
                                  'https://www.mountainproject.com/route/106144306/hitman',
                                  'https://www.mountainproject.com/route/106128129/illmob',
                                  'https://www.mountainproject.com/route/106128147/mob-boss',
                                  'https://www.mountainproject.com/route/111033744/mob-corner',
                                  'https://www.mountainproject.com/route/111088288/reward',
                                  'https://www.mountainproject.com/route/106528577/the-ripper',
                                  'https://www.mountainproject.com/route/111033752/rising-tide',
                                  'https://www.mountainproject.com/route/106279439/scarface',
                                  'https://www.mountainproject.com/route/106252277/tragedy-of-dusk',
                                  'https://www.mountainproject.com/route/107892295/trigger-happy',
                                  'https://www.mountainproject.com/route/108261653/a-bear-and-a-bug',
                                  'https://www.mountainproject.com/route/107589129/ankle-biter',
                                  'https://www.mountainproject.com/route/111985821/bench-warmers',
                                  'https://www.mountainproject.com/route/106104874/bodacious',
                                  'https://www.mountainproject.com/route/105954120/boulder-x',
                                  'https://www.mountainproject.com/route/106597513/boulder-x-slab',
                                  'https://www.mountainproject.com/route/108623471/diamond-in-the-rough',
                                  'https://www.mountainproject.com/route/105960810/essentials',
                                  'https://www.mountainproject.com/route/106621025/groovey',
                                  'https://www.mountainproject.com/route/106040314/headz-aint-ready',
                                  'https://www.mountainproject.com/route/111033777/the-impaler',
                                  'https://www.mountainproject.com/route/106529411/know-hands',
                                  'https://www.mountainproject.com/route/106621033/piece-o-cake',
                                  'https://www.mountainproject.com/route/105960804/poppers',
                                  'https://www.mountainproject.com/route/112111166/slot-machine',
                                  'https://www.mountainproject.com/route/109589079/super-smash-brothers',
                                  'https://www.mountainproject.com/route/108261779/swamp-butt',
                                  'https://www.mountainproject.com/route/111029548/tonys-problem',
                                  'https://www.mountainproject.com/route/107892305/touchdown-giants',
                                  'https://www.mountainproject.com/route/108261758/unknown-slab-left',
                                  'https://www.mountainproject.com/route/108261690/unknown-slab-right',
                                  'https://www.mountainproject.com/route/106104812/anorexorcist',
                                  'https://www.mountainproject.com/route/106041614/bones-to-bits',
                                  'https://www.mountainproject.com/route/112138886/bulemia',
                                  'https://www.mountainproject.com/route/106118276/confident-man',
                                  'https://www.mountainproject.com/route/112272699/flakes-of-life',
                                  'https://www.mountainproject.com/route/106118269/halcyon',
                                  'https://www.mountainproject.com/route/109648266/jaded',
                                  'https://www.mountainproject.com/route/106632408/the-morgue',
                                  'https://www.mountainproject.com/route/106104859/my-little-pony',
                                  'https://www.mountainproject.com/route/112036656/outback',
                                  'https://www.mountainproject.com/route/106632399/rios-problem',
                                  'https://www.mountainproject.com/route/106104828/stegasaurus',
                                  'https://www.mountainproject.com/route/105954114/blaow',
                                  'https://www.mountainproject.com/route/111786306/blaows-cousin',
                                  'https://www.mountainproject.com/route/106187758/bretts-mom',
                                  'https://www.mountainproject.com/route/106104984/downward-spiral',
                                  'https://www.mountainproject.com/route/106036837/evolution',
                                  'https://www.mountainproject.com/route/117029137/flying-v',
                                  'https://www.mountainproject.com/route/112022611/four-eyed-blues',
                                  'https://www.mountainproject.com/route/106945335/further-down-the-spiral',
                                  'https://www.mountainproject.com/route/106104848/glass-blower-aka-pygmies-cornrolls',
                                  'https://www.mountainproject.com/route/113491812/indiana-jones',
                                  'https://www.mountainproject.com/route/106121538/innovator',
                                  'https://www.mountainproject.com/route/107719571/monkey-crotch',
                                  'https://www.mountainproject.com/route/106118078/monkey-press',
                                  'https://www.mountainproject.com/route/106282503/mothra-stewart',
                                  'https://www.mountainproject.com/route/112387920/mothra-stewart-left',
                                  'https://www.mountainproject.com/route/113899750/mothra-stewart-variation',
                                  'https://www.mountainproject.com/route/107336748/mr-natural',
                                  'https://www.mountainproject.com/route/111806947/pikachu',
                                  'https://www.mountainproject.com/route/105948129/polish-terrorist',
                                  'https://www.mountainproject.com/route/106121528/revolution',
                                  'https://www.mountainproject.com/route/105945043/ride-the-lightning',
                                  'https://www.mountainproject.com/route/106597836/squeeze-play',
                                  'https://www.mountainproject.com/route/105948029/storm-pockets',
                                  'https://www.mountainproject.com/route/111996244/storm-traverse',
                                  'https://www.mountainproject.com/route/105948124/terrorist',
                                  'https://www.mountainproject.com/route/111890508/terrorist-left',
                                  'https://www.mountainproject.com/route/118791914/tessa',
                                  'https://www.mountainproject.com/route/106945302/the-three-graces',
                                  'https://www.mountainproject.com/route/118789721/the-unknown-v10',
                                  'https://www.mountainproject.com/route/106597854/up',
                                  'https://www.mountainproject.com/route/106208786/vintage',
                                  'https://www.mountainproject.com/route/106197476/warrior',
                                  'https://www.mountainproject.com/route/112009611/the-wizard',
                                  'https://www.mountainproject.com/route/111033801/woodfords-reserve',
                                  'https://www.mountainproject.com/route/105948043/zap',
                                  'https://www.mountainproject.com/route/118815050/zap-left',
                                  'https://www.mountainproject.com/route/112201242/cup-of-tea',
                                  'https://www.mountainproject.com/route/111033724/down-in-it',
                                  'https://www.mountainproject.com/route/111996264/downward-dog',
                                  'https://www.mountainproject.com/route/109340303/due-north',
                                  'https://www.mountainproject.com/route/105960764/e-z-cheese',
                                  'https://www.mountainproject.com/route/106945118/feel-the-pull',
                                  'https://www.mountainproject.com/route/106306113/fritzs-demise',
                                  'https://www.mountainproject.com/route/106945110/king-arthur',
                                  'https://www.mountainproject.com/route/106945105/kissing-cousins',
                                  'https://www.mountainproject.com/route/106864465/north-slab',
                                  'https://www.mountainproject.com/route/106104839/provia',
                                  'https://www.mountainproject.com/route/106528535/the-riverbed',
                                  'https://www.mountainproject.com/route/106945094/seinfeld',
                                  'https://www.mountainproject.com/route/116539769/steezy-cheese',
                                  'https://www.mountainproject.com/route/108366698/swiss-cheese',
                                  'https://www.mountainproject.com/route/109331194/battle-of-the-bulge',
                                  'https://www.mountainproject.com/route/113278093/bog-of-eternal-stench',
                                  'https://www.mountainproject.com/route/108386961/chasm-crack',
                                  'https://www.mountainproject.com/route/111874069/the-chasm',
                                  'https://www.mountainproject.com/route/114364543/dauber',
                                  'https://www.mountainproject.com/route/111890587/dookie-dyno',
                                  'https://www.mountainproject.com/route/115374854/enthusiasm',
                                  'https://www.mountainproject.com/route/112367815/eternal-love',
                                  'https://www.mountainproject.com/route/117996540/fact-and-fancy',
                                  'https://www.mountainproject.com/route/112984508/the-gloryhole',
                                  'https://www.mountainproject.com/route/116069557/golden-hind',
                                  'https://www.mountainproject.com/route/111336658/jungle-fever',
                                  'https://www.mountainproject.com/route/112868054/kindly-kiting',
                                  'https://www.mountainproject.com/route/112369721/lapras',
                                  'https://www.mountainproject.com/route/108421259/lost-at-sea',
                                  'https://www.mountainproject.com/route/111955276/mart-fart',
                                  'https://www.mountainproject.com/route/113173886/mccabers-direct',
                                  'https://www.mountainproject.com/route/109638740/methods-of-escape',
                                  'https://www.mountainproject.com/route/112367798/mist-of-paradise',
                                  'https://www.mountainproject.com/route/118118274/most-mystic-moods',
                                  'https://www.mountainproject.com/route/108145761/mouthful-of-chalk',
                                  'https://www.mountainproject.com/route/108445099/mudblood',
                                  'https://www.mountainproject.com/route/118118303/mystic-moods',
                                  'https://www.mountainproject.com/route/112369795/the-nile',
                                  'https://www.mountainproject.com/route/112367785/the-number',
                                  'https://www.mountainproject.com/route/112272458/point-of-no-return',
                                  'https://www.mountainproject.com/route/109346318/poseidon',
                                  'https://www.mountainproject.com/route/113278239/puddle-jumper',
                                  'https://www.mountainproject.com/route/112369839/pyramid-crack',
                                  'https://www.mountainproject.com/route/112369758/pyramid-poison',
                                  'https://www.mountainproject.com/route/112369740/rolling-under',
                                  'https://www.mountainproject.com/route/108445108/sar-chasm',
                                  'https://www.mountainproject.com/route/111277251/shadow-of-the-colossus',
                                  'https://www.mountainproject.com/route/108433842/slow-vibration',
                                  'https://www.mountainproject.com/route/112369700/stemmed-possibilities',
                                  'https://www.mountainproject.com/route/113167339/the-swamp-crack-direct',
                                  'https://www.mountainproject.com/route/113167245/the-swamp-crack',
                                  'https://www.mountainproject.com/route/113474635/swamp-descent',
                                  'https://www.mountainproject.com/route/113474558/swamp-is-on',
                                  'https://www.mountainproject.com/route/113294705/swampedelic-pop',
                                  'https://www.mountainproject.com/route/112369656/train-wreck',
                                  'https://www.mountainproject.com/route/111273715/ammunition',
                                  'https://www.mountainproject.com/route/106305754/bloody-knuckles',
                                  'https://www.mountainproject.com/route/106831886/brett-does-lawn-jobs-aka-keep-it-subtle',
                                  'https://www.mountainproject.com/route/106104975/bulletproof',
                                  'https://www.mountainproject.com/route/106528559/ceadas',
                                  'https://www.mountainproject.com/route/107884630/death-of-the-blues',
                                  'https://www.mountainproject.com/route/111959758/the-dream-of-life',
                                  'https://www.mountainproject.com/route/106187751/gun-show',
                                  'https://www.mountainproject.com/route/106305776/hemlock-gate',
                                  'https://www.mountainproject.com/route/106041591/kalbro',
                                  'https://www.mountainproject.com/route/107553699/kids-with-guns',
                                  'https://www.mountainproject.com/route/106529203/knuckle-dragger',
                                  'https://www.mountainproject.com/route/112170933/missile-command',
                                  'https://www.mountainproject.com/route/106305767/my-girlfriend',
                                  'https://www.mountainproject.com/route/106277637/nra',
                                  'https://www.mountainproject.com/route/114382550/one-in-the-chamber',
                                  'https://www.mountainproject.com/route/112194373/out-of-ammo',
                                  'https://www.mountainproject.com/route/106144294/power-technique',
                                  'https://www.mountainproject.com/route/107553690/slab-dercling',
                                  'https://www.mountainproject.com/route/106144284/standard-direct',
                                  'https://www.mountainproject.com/route/106144279/standard-route',
                                  'https://www.mountainproject.com/route/107833342/still-remains',
                                  'https://www.mountainproject.com/route/106529195/the-very-bad-idea',
                                  'https://www.mountainproject.com/route/106041602/yosemite-arete',
                                  'https://www.mountainproject.com/route/111308073/an-unexpected-journey',
                                  'https://www.mountainproject.com/route/105960774/another-world',
                                  'https://www.mountainproject.com/route/106553877/barnacle-bill',
                                  'https://www.mountainproject.com/route/107659455/bilbos-revenge',
                                  'https://www.mountainproject.com/route/108428326/boredum',
                                  'https://www.mountainproject.com/route/112027659/charlie-horse',
                                  'https://www.mountainproject.com/route/107393928/circumspect-ceiling',
                                  'https://www.mountainproject.com/route/106528490/crystal-method',
                                  'https://www.mountainproject.com/route/105960778/edges',
                                  'https://www.mountainproject.com/route/106250047/four-hole',
                                  'https://www.mountainproject.com/route/112016142/gandalf',
                                  'https://www.mountainproject.com/route/106104969/gone-in-60-seconds',
                                  'https://www.mountainproject.com/route/105960783/good-rips',
                                  'https://www.mountainproject.com/route/111996201/grilled-cheese',
                                  'https://www.mountainproject.com/route/105945808/hobbit-direct',
                                  'https://www.mountainproject.com/route/105945048/hobbit-hole',
                                  'https://www.mountainproject.com/route/105948017/jaws-texas-chainsaw-massacre',
                                  'https://www.mountainproject.com/route/105948021/johns-stand-up',
                                  'https://www.mountainproject.com/route/109009807/lets-call-it-levitation',
                                  'https://www.mountainproject.com/route/106774962/the-lobster-pot',
                                  'https://www.mountainproject.com/route/105948025/the-lobster-tail',
                                  'https://www.mountainproject.com/route/107941108/manhole',
                                  'https://www.mountainproject.com/route/105948111/the-marathon',
                                  'https://www.mountainproject.com/route/107296135/mistaken-identity',
                                  'https://www.mountainproject.com/route/105945380/power-and-grace',
                                  'https://www.mountainproject.com/route/105948118/the-professor',
                                  'https://www.mountainproject.com/route/112776360/ricochet',
                                  'https://www.mountainproject.com/route/110507213/rios-smaug-face-problem',
                                  'https://www.mountainproject.com/route/106555507/shillings',
                                  'https://www.mountainproject.com/route/107941091/the-shire',
                                  'https://www.mountainproject.com/route/106118067/sidewinder',
                                  'https://www.mountainproject.com/route/114318932/sisyphus',
                                  'https://www.mountainproject.com/route/119062779/smaugs-face',
                                  'https://www.mountainproject.com/route/106285891/two-bits',
                                  'https://www.mountainproject.com/route/106211401/the-wanderer',
                                  'https://www.mountainproject.com/route/105960769/when-im-on-my-own',
                                  'https://www.mountainproject.com/route/106103762/zoo-traverse'])

    async def tearDown(self):
        await self.session.close()


if __name__ == '__main__':
    unittest.main(buffer=False)
