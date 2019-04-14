#! python3
import requests

from bs4 import BeautifulSoup, SoupStrainer


# Finds links to areas
def area_finder(page_links):
    areas = []
    for link in page_links.find_all('a'):
        areas.append(link.get('href'))
    areas = [link for link in areas if '.com/area/' in link]
    return areas


# Finds all the climbs on the web page
def climb_finder(page_links):
    climbs = []
    for link in page_links.find_all('a'):
        climbs.append(link.get('href'))
    climbs = [link for link in climbs if 'com/route/' in link]  # Takes out extra links that get pulled
    return climbs


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


def main_loop(area_links):
    sub_area_links = []
    links_to_climbs = []

    while True:
        for link in area_links:
            x, y = link_finder(link)
            if x == 'area':
                sub_area_links += y

            else:
                links_to_climbs += y

        area_links = sub_area_links
        if len(area_links) == 0:
            break

        sub_area_links = []
    return links_to_climbs
