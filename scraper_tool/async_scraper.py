import json
import time
import asyncio

from aiohttp import ClientSession

from scraper_tool import async_web_crawler
from scraper_tool import async_page_search


async def scraper(link, session, **kwargs):
    """Scrapes mountain project links to find all sub areas
    and assert awesomeness of a climb"""
    # Loops through every area and sub area
    climb_links = await async_web_crawler.web_crawler_main(link, session, **kwargs)
    print(len(climb_links))

    # Goes through climb links to search for regex
    off_widths = await async_page_search.page_search_main(climb_links, session, **kwargs)
    print(len(off_widths))
    print('Writing to file')

    with open('rumney.json', 'w') as climb_file:
        json.dump(off_widths, climb_file)


async def main(mountain_project_link):
    """The main function to get called by scraper.py"""
    async with ClientSession() as session:
        tasks = []
        for link in mountain_project_link:
            tasks.append(scraper(link, session))

        await asyncio.gather(*tasks)


if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(main(['https://www.mountainproject.com/area/105867829/rumney']))
    print(f'{time.time() - start_time}')
