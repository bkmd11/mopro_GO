import asyncio
import aiofiles
import aiohttp
import re

from bs4 import BeautifulSoup, SoupStrainer
from aiohttp import ClientSession

regex = re.compile('off-width')


async def page_request(climb_url, session, **kwargs):
    """Gets the url request so the page can be searched"""
    resp = await session.request(method='GET', url=climb_url, **kwargs)
    print(type(resp))
    resp.raise_for_status()

    html = await resp.text()
    return html


async def parse(climb_url, session, **kwargs):
    """Finds the regex in html"""
    found = set()
    html = await page_request(climb_url, session, **kwargs)

    awesome_climb = regex.findall(html)

    if len(awesome_climb) >= 1:
        found.add(climb_url)
    return found


async def display_awesome_climbs(climb_url, **kwargs):
    climbs = await parse(climb_url, **kwargs)
    for climb in climbs:

        print(climb)


async def crawler(climb_url_list, **kwargs):
    """ Starts the crawling portion of this shit show"""
    async with ClientSession() as session:
        tasks = []
        for climb_url in climb_url_list:
            tasks.append(display_awesome_climbs(climb_url, session=session, **kwargs))

        await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(crawler([
        'https://www.mountainproject.com/route/106949198/short-stuff',
        'https://www.mountainproject.com/route/105941458/obscene-phone-call',
        'https://www.mountainproject.com/route/106540643/no-answer'
    ]))
