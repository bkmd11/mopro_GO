#! python3

""" The goal of this project is to find all the off width climbs on mountain
project. It will use requests and BeautifulSoup to gather this info and save
it to a file with links to the climbs page, ordered by grade. 

This will be my masterpiece.
"""

import json
import requests
import re
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


# A regex for off-widths
def regex_search(page_text):
    climbing_term = re.compile(r'off width|off-width|chimney| ow ', re.I)
    awesome_climb = climbing_term.search(str(page_text[0]))

    # If regex is found on page do the thing.
    if awesome_climb is not None:
        return 'send_it'
    else:
        return None


# Parses out the description of a climb 
def awesome_climb(links_to_climbs):
    off_width_links = []
    for climb in links_to_climbs:
        res = requests.get(climb)
        res.raise_for_status()

        # Pulls out just the description
        strainer = SoupStrainer(class_='col-xs-12')
        climb_text = BeautifulSoup(res.text, parse_only=strainer, features='lxml')
        description = climb_text.find_all(class_='fr-view')

        awesome_climb = regex_search(description)
        if awesome_climb is not None:
            off_width_links.append(climb)
        else:
            continue
    return off_width_links


def main():
    # sets the initial area
    string, area = link_finder('https://www.mountainproject.com/area/105929413/pawtuckaway')

    # Loops through every area and sub area
    climb_links = main_loop(area)

    # Goes through climb links to search for regex
    off_widths = awesome_climb(climb_links)

    with open('off_width.json', 'w') as climb_file:
        json.dump(off_widths,climb_file)


if __name__ == '__main__':
    main()