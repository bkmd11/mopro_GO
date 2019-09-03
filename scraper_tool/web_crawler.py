#! python3
import requests
import time

from bs4 import BeautifulSoup, SoupStrainer


# Finds links to areas
def area_finder(page_links):
    for link in page_links.find_all('a'):
        area_link = link.get('href')

        yield area_link


# Finds all the climbs on the web page
def climb_finder(page_links):
    for link in page_links.find_all('a'):
        climb_link = link.get('href')
        if 'com/route/' in climb_link:    # Removes extra links that get pulled
            yield climb_link
        else:
            continue


# Determine if link is to a route or a climb
def link_finder(web_address):
    request = requests.get(web_address)
    request.raise_for_status()

    mp_sidebar = SoupStrainer(class_='mp-sidebar')
    page_links = BeautifulSoup(request.text, parse_only=mp_sidebar, features='lxml')

    if 'lef-nav-row' in request.text:
        area_links = area_finder(page_links)
        return 'area', area_links
    else:
        climbing_links = climb_finder(page_links)
        return 'climb', climbing_links


def main_loop(link):
    links_to_climbs = []
    area_links = [link]

    while area_links:
        found_link = area_links.pop(0)
        x, y = link_finder(found_link)
        for link in y:
            if x == 'area':
                area_links.append(link)

            else:
                links_to_climbs.append(link)

    return links_to_climbs


if __name__ == '__main__':
    start_time = time.time()
    spam = main_loop('https://www.mountainproject.com/area/105929413/pawtuckaway')
    print(len(spam))
    print(f'{time.time()-start_time}')
