import json
import time
import asyncio
import re

from aiohttp import ClientSession

from scraper_tool import crawler
from scraper_tool import page_search
from scraper_tool import load_to_db


async def scraper(link, style_regex, session, **kwargs):
    """Scrapes mountain project links to find all sub areas
    and assert awesomeness of a climb"""
    # Loops through every area and sub area
    climb_links = await crawler.web_crawler_main(link, session, **kwargs)

    # Goes through climb links to search for regex
    off_widths = await page_search.page_search_main(climb_links, session, style_regex, **kwargs)

    with open(r'db_credentials.json', 'r') as file:
        credentials = json.load(file)

    connection = load_to_db.create_connection(credentials['username'], credentials['password'])
    for climb_info in off_widths:
        load_to_db.main_query(connection, climb_info)


async def main(mountain_project_link, style_regex):
    """The main function to get called by scraper.py"""
    async with ClientSession() as session:
        tasks = []
        for link in mountain_project_link:
            tasks.append(scraper(link, style_regex, session))

        await asyncio.gather(*tasks)


def verify_link_input():
    """Checks to make sure the link is a valid mountain project link"""
    link = input('Copy and paste the full mountain project link:\n')
    regex = re.compile('https://www.mountainproject.com/area/.*')
    try:
        verified_link = regex.search(link)
        verified_link.group()
        return link

    except AttributeError:
        return None


def verify_regex_input():
    """Checks to verify regex choice"""
    style_regex = input('Enter your style regex "ow", "finger", "fist"')

    if style_regex.lower() in ('ow', 'finger', 'fist'):
        return style_regex.lower()
    else:
        return None


if __name__ == '__main__':
    start_time = time.time()
    while True:
        mo_pro_link = verify_link_input()
        if mo_pro_link is not None:
            break
        else:
            print('Invalid area, please enter a valid area link.\n')

    while True:
        style = verify_regex_input()
        if style:
            break
        else:
            print('Invalid style, please enter a valid choice')

    asyncio.run(main([mo_pro_link], style))
    print(f'{time.time() - start_time}')
