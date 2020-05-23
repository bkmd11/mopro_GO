import asyncio
import re
import time

from bs4 import BeautifulSoup, SoupStrainer
from aiohttp import ClientSession

from colorama import Fore
OFFWIDTH_REGEX = re.compile(r'off width|off-width|chimney| ow | offwidth', re.I)
FINGER_REGEX = re.compile(r'finger|finger-crack|finger crack', re.I)
FIST_REGEX = re.compile(r'fist', re.I)
# TODO: make scrapper look for all these types and save them to my database


async def climb_name(html_text):
    """Finds the name of the climb"""
    strainer = SoupStrainer('h1')
    name = BeautifulSoup(html_text, parse_only=strainer, features='lxml')

    route_name = name.find_all(text=True)
    cleaned_route_name = route_name[1].strip()

    return cleaned_route_name


async def grade_finder(html_text):
    """Finds the grade on the page"""
    strainer = SoupStrainer(class_='inline-block mr-2')
    grade = BeautifulSoup(html_text, parse_only=strainer, features='lxml')

    text_for_grade = grade.find_all(text=True)

    return text_for_grade[1].strip()    # The grade will have a space after it


async def navigation_tree(html_text):
    """Finds the area navigation tree on the page"""
    nav_tree = []
    strainer = SoupStrainer(class_='mb-half small text-warm')
    navigation_tree = BeautifulSoup(html_text, parse_only=strainer, features='lxml')

    for link in navigation_tree.find_all('a'):
        nav_tree.append(link.get('href').rsplit('/', 1)[1])

    return nav_tree[2:4]


async def list_maker(climb_link, html_text, style_regex):
    """Makes a list to add to the big list"""
    list_ = [climb_link]
    route_name = await climb_name(html_text)
    list_.append(route_name)
    nav_tree = await navigation_tree(html_text)
    list_ += nav_tree
    grade = await grade_finder(html_text)
    list_.append(grade)
    list_.append(style_regex)

    return list_


async def page_request(climb_url, session, **kwargs):
    """Gets the url request so the page can be searched"""
    resp = await session.request(method='GET', url=climb_url, **kwargs)
    resp.raise_for_status()

    html = await resp.text()

    return html


async def parse(climb_url, session, style_regex, **kwargs):
    """Finds the regex in the description from the html"""
    found = set()
    print(f'{Fore.CYAN}searching {climb_url}')
    html = await page_request(climb_url, session, **kwargs)

    # Pulls out just the description
    strainer = SoupStrainer(class_='col-xs-12')
    climb_text = BeautifulSoup(html, parse_only=strainer, features='lxml')
    description = climb_text.find(class_='fr-view')

    if style_regex == 'ow':
        awesome_climb = OFFWIDTH_REGEX.findall(str(description))
    elif style_regex == 'finger':
        awesome_climb = FINGER_REGEX.findall(str(description))
    elif style_regex == 'fist':
        awesome_climb = FIST_REGEX.findall(str(description))

    if len(awesome_climb) >= 1:
        found.add(climb_url)
        print('awesomeness found!')
    return found, html


async def page_search_main(climb_url_list, session, style_regex, **kwargs):
    """This is the main function to be run with async_scraper"""
    awesome_climb_list = []
    for climb in climb_url_list:
        climb_links, html = await parse(climb, session, style_regex)
        for link in climb_links:
            awesome_climb_list.append(await list_maker(link, html, style_regex))

    return awesome_climb_list


async def main(climb_url_list, **kwargs):
    """ Starts the crawling portion of this shit show"""
    #style_regex = input('Enter choice "ow" or "finger" or "fist": ')
    async with ClientSession() as session:
        tasks = [page_search_main(climb_url_list, session=session, style_regex='ow', **kwargs)]

        await asyncio.gather(*tasks)


if __name__ == '__main__':
    """To be run for testing purposes"""
    start_time = time.time()
    asyncio.run(main([
        'https://www.mountainproject.com/route/106949198/short-stuff',
        'https://www.mountainproject.com/route/105941458/obscene-phone-call',
        'https://www.mountainproject.com/route/106540643/no-answer',
        'https://www.mountainproject.com/route/105929544/the-horn'
    ]))
    print(f'{time.time()-start_time}')
