#! python3

""" The goal of this project is to find all the off width climbs on mountain
project. It will use requests and BeautifulSoup to gather this info and save
it to a file with links to the climbs page, ordered by grade. 

This will be my masterpiece.
"""

import requests
import re
from bs4 import BeautifulSoup, SoupStrainer

import pprint

# Setting global variables
sub_area_links = []
climb_links = []

# Makes a requests obj and parses to BS
# Needs to change url for every possible location and all areas and all climbs
url = 'https://www.mountainproject.com/area/105929413/pawtuckaway'
res = requests.get(url)
res.raise_for_status()

# This could become a function as it will be repeated
# Gets me a list of sub areas
left_nav_row = SoupStrainer(class_='lef-nav-row')
climbing_areas = BeautifulSoup(res.text, parse_only=left_nav_row,features='lxml')
for link in climbing_areas.find_all('a'):
    sub_area_links.append(link.get('href'))

       
for link in sub_area_links:
    url = link
    res = requests.get(url)
    res.raise_for_status()

    mp_sidebar = SoupStrainer(class_='mp-sidebar')
    sub_climbing_areas = BeautifulSoup(res.text, parse_only=mp_sidebar, features='lxml')

    for link in sub_climbing_areas.find_all('a'):
        climb_links.append(link.get('href'))

#pprint.pprint(climb_links)


for climb in climb_links:
    try:
        url = climb
        res = requests.get(url)
        res.raise_for_status()

        climb_text = BeautifulSoup(res.text, 'html.parser')

        # This searches for climbs in each area
        text_to_search = climb_text.select('.fr-view')    # Description

        # Makes a regex to find
        # Needs to search for more variations
        climbing_term = re.compile(r'off width|off-width|chimney', re.I) 
        awesome_climb = climbing_term.search(str(text_to_search))

        # If regex is found on page do the thing.
        # Will be changed to make a link in a file
        if awesome_climb is not None:
            print(climb)
        else:
            continue
    except:
        continue


""" 
    Current short comings, it searches the entire page for my regex, resulting
    in climbs that are located by a chminey to show up. Also climbing areas
    show up in my list if they are described with one of my regex. I only want
    routes to show up.

    Other than that it looks good. Moving forward I want to try expanding to
    go through the larger areas or the entire state.

    and again, organize by location or grade.
    And market it to make millions

    It doesnt go all the way to the end of the areas to get to climbs if there
    are more than two steps.
"""
