import asyncio
import re
import time

from bs4 import BeautifulSoup, SoupStrainer
from aiohttp import ClientSession

# Todo: docstrings for each function and clean up variable names for clarity

HREF_RE = re.compile(r'href="(.*?)"')


async def area_finder(page_links):
    areas = []
    for link in HREF_RE.findall(str(page_links)):
        areas.append(link)
    areas = [link for link in areas if 'com/area/' in link]

    return areas


async def climb_finder(page_links):
    climbs = []
    for link in HREF_RE.findall(str(page_links)):
        climbs.append(link)
    climbs = [link for link in climbs if 'com/route/' in link]

    return climbs


async def get_request(url, session, **kwargs):
    resp = await session.request(method='GET', url=url, **kwargs)
    resp.raise_for_status()

    html = await resp.text()

    return html


async def parse_climb_or_area(url, session, **kwargs):
    html = await get_request(url, session)

    mp_sidebar = SoupStrainer(class_='mp-sidebar')
    page_links = BeautifulSoup(html, parse_only=mp_sidebar, features='lxml')

    if 'lef-nav-row' in html:
        area_links = await area_finder(page_links)

        return 'area', area_links

    else:
        climb_links = await climb_finder(page_links)

        return 'climb', climb_links


async def main_loop(url, session, **kwargs):
    climb_links = []
    area_links = [url]
    while area_links:
        found_link = area_links.pop(0)
        x, y = await parse_climb_or_area(found_link, session, **kwargs)
        for link in y:
            if x == 'area':
                area_links.append(link)

            else:
                climb_links.append(link)
    print(len(climb_links))
    return climb_links


async def main(url_list):
    async with ClientSession() as session:
        tasks = []
        for link in url_list:
            tasks.append(main_loop(link, session))

        await asyncio.gather(*tasks)

if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(main(['https://www.mountainproject.com/area/105929413/pawtuckaway']))
    print(f'{time.time()-start_time}')
