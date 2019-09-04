import asyncio
import re
import time

from bs4 import BeautifulSoup, SoupStrainer
from aiohttp import ClientSession

REGEX = re.compile('off-width')   # todo: update this once I am up and running


async def grade_finder(request):
    """Finds the grade on the page"""
    strainer = SoupStrainer(class_='inline-block mr-2')
    grade = BeautifulSoup(request, parse_only=strainer, features='lxml')

    text_for_grade = grade.find_all(text=True)

    return text_for_grade[1]    # The grade will have a space after it


async def navigation_tree(request):
    """Finds the area navigation tree on the page"""
    nav_tree = []
    strainer = SoupStrainer(class_='mb-half small text-warm')
    navigation_tree = BeautifulSoup(request, parse_only=strainer, features='lxml')

    for link in navigation_tree.find_all('a'):
        nav_tree.append(link.get('href').rsplit('/', 1)[1])

    return nav_tree[2:4]


async def list_maker(climb_link, request):
    """Makes a list to add to the big list"""
    list_ = [climb_link]
    nav_tree = await navigation_tree(request)
    list_ += nav_tree
    grade = await grade_finder(request)
    list_.append(grade)

    return list_


async def page_request(climb_url, session, **kwargs):
    """Gets the url request so the page can be searched"""
    resp = await session.request(method='GET', url=climb_url, **kwargs)
    resp.raise_for_status()

    html = await resp.text()

    return html


async def parse(climb_url, session, **kwargs):
    """Finds the regex in html"""
    found = set()
    html = await page_request(climb_url, session, **kwargs)

    awesome_climb = REGEX.findall(html)

    if len(awesome_climb) >= 1:
        found.add(climb_url)

    return found, html


async def write_awesome_climbs(climb_url, **kwargs):
    """Writes the list of climbs to a file for later use"""
    # todo: figure out json with async stuff
    climbs, html = await parse(climb_url, **kwargs)
    for climb in climbs:
        climb_info = await list_maker(climb, html)
        print(climb_info)


async def crawler(climb_url_list, **kwargs):
    """ Starts the crawling portion of this shit show"""
    async with ClientSession() as session:
        tasks = []
        for climb_url in climb_url_list:
            tasks.append(write_awesome_climbs(climb_url, session=session, **kwargs))

        await asyncio.gather(*tasks)


async def main(climb_url_list):
    """The main program to be called by scraper"""
    asyncio.run(crawler(climb_url_list))


if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(crawler([
        'https://www.mountainproject.com/route/106949198/short-stuff',
        'https://www.mountainproject.com/route/105941458/obscene-phone-call',
        'https://www.mountainproject.com/route/106540643/no-answer'
    ]))
    print(f'{time.time()-start_time}')
