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
        left_nav_row = SoupStrainer(class_='lef-nav-row')
        areaLinks = BeautifulSoup(request.text,parse_only=left_nav_row,features='lxml')
        area_links = area_finder(areaLinks)
        return 'area', area_links
    else:
        max_height = SoupStrainer({'id':'lef-nav-route-table'})
        route_links = BeautifulSoup(request.text,parse_only=max_height,features='lxml')
        climbing_links = climb_finder(page_links)
        return 'climb', climbing_links


# Checks for error in link placemant and corrects it
def list_swap(climbing_list, area_list):
    for link in climbing_list:
        if '/area/' in link:
            area_list.append(link)   
            climbing_list.remove(link)
    return climbing_list, area_list

            
# Setting global variables
sub_area_links = []
sub_sub_area_links = []
climb_links = []

# Makes a requests obj and parses to BS
string, areas = link_finder('https://www.mountainproject.com/area/105929413/pawtuckaway')

### I need to make a while loop to go through a whole state

# Gets me a list of sub areas
for link in areas:
    x,y = link_finder(link)
    if x == 'area':
        sub_area_links += y
    else:
        climb_links += y

### I need to actually analyze what this does
climb_links, sub_area_links = list_swap(climb_links, sub_area_links)

for link in sub_area_links: 
    x,y = link_finder(link)
    if x == 'area':
        sub_sub_area_links += y
    elif x == 'climb':
        climb_links += y

climb_links, sub_sub_area_links = list_swap(climb_links, sub_sub_area_links)

sys.exit()  # I have this here because idk how to debug this correctly
        
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
