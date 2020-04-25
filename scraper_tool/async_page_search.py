import asyncio
import re
import time

from bs4 import BeautifulSoup, SoupStrainer
from aiohttp import ClientSession

REGEX = re.compile(r'off width|off-width|chimney| ow | offwidth', re.I)


async def climb_name(request):
    """Finds the name of the climb"""
    strainer = SoupStrainer('h1')
    name = BeautifulSoup(request, parse_only=strainer, features='lxml')

    route_name = name.find_all(text=True)
    cleaned_route_name = route_name[1].strip()

    return cleaned_route_name


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
    route_name = await climb_name(request)
    list_.append(route_name)
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
    """Finds the regex in the description from the html"""
    found = set()
    print(f'searching {climb_url}')
    html = await page_request(climb_url, session, **kwargs)

    # Pulls out just the description
    strainer = SoupStrainer(class_='col-xs-12')
    climb_text = BeautifulSoup(html, parse_only=strainer, features='lxml')
    description = climb_text.find(class_='fr-view')

    awesome_climb = REGEX.findall(str(description))

    if len(awesome_climb) >= 1:
        found.add(climb_url)
        print('awesomeness found!')
    return found, html


async def page_search_main(climb_url_list, session, **kwargs):
    """This is the main function to be run with async_scraper"""
    awesome_climb_list = []
    for climb in climb_url_list:
        climb_links, html = await parse(climb, session, **kwargs)
        for link in climb_links:
            awesome_climb_list.append(await list_maker(link, html))

    return awesome_climb_list


async def main(climb_url_list, **kwargs):
    """ Starts the crawling portion of this shit show"""
    async with ClientSession() as session:
        tasks = [page_search_main(climb_url_list, session=session, **kwargs)]

        await asyncio.gather(*tasks)


if __name__ == '__main__':
    """To be run for testing purposes"""
    start_time = time.time()
    asyncio.run(main([
        'https://www.mountainproject.com/route/106949198/short-stuff',
        'https://www.mountainproject.com/route/105941458/obscene-phone-call',
        'https://www.mountainproject.com/route/106540643/no-answer'
    ]))
    print(f'{time.time()-start_time}')
