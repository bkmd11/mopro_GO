#! python3

""" This program takes my list of climbs and sorts it by area, and
puts everything into a file with hyperlinks to the climbs
"""

import operator
import json
import requests
from bs4 import BeautifulSoup, SoupStrainer

import pprint


# Looks at the grade of each climb
def grade_finder(request):
    strainer = SoupStrainer(class_='inline-block mr-2')
    grade = BeautifulSoup(request.text, parse_only=strainer, features='lxml')

    text_for_grade = grade.find_all(text=True)
    return text_for_grade[1]


# Pulls the nav tree off Mountain Project
def navigation_tree(request):
    nav_tree = []
    strainer = SoupStrainer(class_='mb-half small text-warm')
    navigation_tree = BeautifulSoup(request.text, parse_only=strainer, features='lxml')

    for link in navigation_tree.find_all('a'):
        nav_tree.append(link.get('href').rsplit('/', 1)[1])
    del nav_tree[0]
    return nav_tree


# Makes a list of the url, areas, and grade, returns a tuple       
def list_maker(list_of_climbs):
    master_list = []
    for url in list_of_climbs:
        list_ = []
        request = requests.get(url)
        request.raise_for_status()

        nav_tree = navigation_tree(request)
        
        climb_grade = grade_finder(request)
        nav_tree.append(climb_grade)
        list_.append(url)
        list_ += nav_tree

        master_list.append(tuple(list_))

    return master_list

    
with open('off_width.json', 'r') as climbing_list:
    off_width_list = json.load(climbing_list)
    
# Finds the nav_tree for every climb on my list
climb_list = list_maker(off_width_list[190:210])
climb_list.sort(key = operator.itemgetter(2,-1)) # Organizes by area, then grade

link_list = [x[0] for x in climb_list]    # This takes my sorted urls
pprint.pprint(climb_list)   # Also for debugging


"""
    New idea a list of tuples [(url,area,sub area, sub sub area...,grade)]
    I can save this as a master file thats organized by grades if I want to make
    a tick list of progression, But I will also be able to make a search tool
    that can look up an area im going to to see if anything on the list is there
    and give me its approxamate location. I like this idea best.

    I have my list of tuples sorted. I just need to figure out how I want to
    display this information... Just saving it and pulling info by an area
    would probably be simplest.
"""
