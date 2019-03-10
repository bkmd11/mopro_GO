#! python3

""" This program takes my list of climbs and sorts it by area, and
puts everything into a file with hyperlinks to the climbs
"""

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


def navigation_tree(request):
    nav_tree = []
    strainer = SoupStrainer(class_='mb-half small text-warm')
    navigation_tree = BeautifulSoup(request.text, parse_only=strainer, features='lxml')

    for link in navigation_tree.find_all('a'):
        nav_tree.append(link.get('href').rsplit('/',1)[1])
    del nav_tree[0]
    return nav_tree

        
def dict_maker(list_of_climbs):
    dict_of_climbs = {}
    for url in list_of_climbs:
        request = requests.get(url)
        request.raise_for_status()

        nav_tree = navigation_tree(request)
        
        climb_grade = grade_finder(request)
        nav_tree.append(climb_grade)

        dict_of_climbs[url] = nav_tree

        
    return dict_of_climbs

    
with open('off_width.json', 'r') as climbing_list:
    off_width_list = json.load(climbing_list)
    
# Finds the nav_tree for every climb on my list
climb_dict = dict_maker(off_width_list[200:210])

"""
    So I can make my dictionary. I need to figure out how to sort this.
    Dictionaries are not capable of being sorted in that fashion.
    I have found a way to do this in the past, I need to look it up again
"""

pprint.pprint(climb_dict)   # Also for debugging



    

""" I need to make a dict {link:[state,area,sub_area,...]}
    I can then take this and make a list of the values for every key,
    and use that to group climbs in the same areas.

    Then I will need to find the grades for each climb, and sort by that.
    I can probably make that in the same value list
"""
        
