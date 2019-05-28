#! python3

import requests
import re
import operator

from bs4 import BeautifulSoup, SoupStrainer


# A regex for off-widths
def regex_search(page_text):
    climbing_term = re.compile(r'off width|off-width|chimney| ow | offwidth', re.I)
    awesome_climb = climbing_term.search(str(page_text[0]))

    # If regex is found on page do the thing.
    if awesome_climb is not None:
        return 'send_it'
    else:
        return None


# Finds the grade on the page
def grade_finder(request):
    strainer = SoupStrainer(class_='inline-block mr-2')
    grade = BeautifulSoup(request.text, parse_only=strainer, features='lxml')

    text_for_grade = grade.find_all(text=True)

    return text_for_grade[1]    # The grade will have a space after it


# Finds the area navigation tree on the page
def navigation_tree(request):
    nav_tree = []
    strainer = SoupStrainer(class_='mb-half small text-warm')
    navigation_tree = BeautifulSoup(request.text, parse_only=strainer, features='lxml')

    for link in navigation_tree.find_all('a'):
        nav_tree.append(link.get('href').rsplit('/', 1)[1])

    return nav_tree[2:4]


# Makes a list to add to the big list
def list_maker(climb_link, request):
    list_ = [climb_link]
    nav_tree = navigation_tree(request)
    list_ += nav_tree
    grade = grade_finder(request)
    list_.append(grade)

    return list_


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

        print(f'Searching {climb} for awesomeness')
        awesome_climb = regex_search(description)

        if awesome_climb is not None:
            off_width_links.append(list_maker(climb, res))
            print('Awesomeness asserted!')

        else:
            continue

    off_width_links.sort(key=operator.itemgetter(1, 2, -1))

    return off_width_links

