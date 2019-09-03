import asyncio
import re

from scraper_tool import page_search
from aiohttp import ClientSession

REGEX = re.compile('off-width')   # todo: update this once I am up and running


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
        climb_info = page_search.list_maker(climb, html)    # todo: passing html text into beautiful soup worked
                                                            #   look into doing that for the web_crawler
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
    asyncio.run(crawler([
        'https://www.mountainproject.com/route/106949198/short-stuff',
        'https://www.mountainproject.com/route/105941458/obscene-phone-call',
        'https://www.mountainproject.com/route/106540643/no-answer'
    ]))
