import asyncio
import re

from bs4 import BeautifulSoup, SoupStrainer

from colorama import init, Fore

URL_TAG = re.compile(r'href="(.*?)"')


async def area_finder(bs4_parsed_links_for_areas):
    """If a link is an area, this pulls all of the sub-areas from it"""
    areas = []
    for link in URL_TAG.findall(str(bs4_parsed_links_for_areas)):
        areas.append(link)
    areas = [link for link in areas if 'com/area/' in link]

    return areas


async def climb_finder(bs4_parsed_links_for_climbs):
    """If a link is a climb, this pulls all of the other climbs from it"""
    climbs = []
    for link in URL_TAG.findall(str(bs4_parsed_links_for_climbs)):
        climbs.append(link)
    climbs = [link for link in climbs if 'com/route/' in link]

    return climbs


async def get_request(mountain_project_url, session, **kwargs):
    """This gets the request for the mountain_project_url"""
    resp = await session.request(method='GET', url=mountain_project_url, **kwargs)
    resp.raise_for_status()

    html_text = await resp.text()

    return html_text


async def parse_climb_or_area(url, session, **kwargs):
    """Determines if a link is to a climb or an area"""

    print(f'{Fore.GREEN}parsing {url}')
    html_text = await get_request(url, session, **kwargs)

    mp_sidebar = SoupStrainer(class_='mp-sidebar')
    page_links = BeautifulSoup(html_text, parse_only=mp_sidebar, features='lxml')

    if 'lef-nav-row' in html_text:
        area_links = await area_finder(page_links)

        return 'area', area_links

    else:
        climb_links = await climb_finder(page_links)

        return 'climb', climb_links


async def web_crawler_main(mountain_project_url, session, **kwargs):
    climb_links = []
    area_links = [mountain_project_url]
    while area_links:
        found_link = area_links.pop(0)
        x, y = await parse_climb_or_area(found_link, session, **kwargs)
        for link in y:
            if x == 'area':
                area_links.append(link)

            else:
                climb_links.append(link)

    return climb_links
