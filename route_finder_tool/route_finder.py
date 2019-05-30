#! python3
"""This is a tool to work with the data gathered by my web scraper_tool. It will be able
to search a json file for the climbs that meet a given criteria, whether that is
location or grade, could also go for trad/sport/boulder.


"""
import json
import re

from route_finder_tool import option_finder


"""It works as a CLI taking sys.argv[1] as the regex
        But I am adding option_finder() to change that


IDEA:
Need to make this more user friendly
I am going to make a GUI for this when my brain is actually working
"""


# Makes the user input into a regex to find variations of grade
def regex(search_term):
    if '.' in search_term:
        search_term = escape_character(search_term)
    search_word = f'{search_term}.*'
    regex = re.compile(search_word, re.I)

    return regex


# Adds an escape character for the '.' in a grade
def escape_character(climbing_grade):
    if '\\' in climbing_grade:

        return climbing_grade
    else:
        list_ = list(climbing_grade)
        add_backslash = [x if x != '.' else '\\.' for x in list_]
        string = ''.join(add_backslash)

        return string


# Takes a list of climbs and searches for a given criteria term
def find_by_criteria(list_of_climbs):
    global criteria
    search_term = regex(criteria)

    filtered_list = list(filter(search_term.search, list_of_climbs))

    return filtered_list


if __name__ == '__main__':
    with open('off_width.json', 'r') as file:
        climbing_list = json.load(file)

    criteria = option_finder.criteria_selector(climbing_list)

    x = list(filter(find_by_criteria, climbing_list))

    for i in x:
        print(i[0])
