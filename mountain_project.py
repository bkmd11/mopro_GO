#! python3

""" The goal of this project is to find all the off width climbs on mountain
project. It will use requests and BeautifulSoup to gather this info and save
it to a file with links to the climbs page, ordered by grade. 

This will be my masterpiece.
"""

import requests
import re
from bs4 import BeautifulSoup, SoupStrainer

import sys
import pprint


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
    climbs = [link for link in climbs if 'com/route/' in link]   # Takes out extra links that get pulled
    return climbs


# Determine if link is to a route or a climb
def link_finder(web_address):
    request = requests.get(web_address)
    request.raise_for_status()

    mp_sidebar = SoupStrainer(class_='mp-sidebar')
    page_links = BeautifulSoup(request.text, parse_only=mp_sidebar,features='lxml')
    
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


# sets the initial area
string, area = link_finder('https://www.mountainproject.com/area/105929413/pawtuckaway')

# Loops through every area and sub area
climb_links = main_loop(area)
print(len(climb_links))
sys.exit()
for climb in climb_links:
    url = climb
    res = requests.get(url)
    res.raise_for_status()

    climb_text = BeautifulSoup(res.text, 'html.parser')

    text_to_search = climb_text.select('.fr-view')    # Description, Location, Protection
    ### I need to narrow this down
    ### Something to do with <h2> header...
    
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



""" 
    Current short comings, it searches the entire page for my regex, resulting
    in climbs that are located by a chminey to show up.

    and again, organize by location or grade.
    And market it to make millions
"""
