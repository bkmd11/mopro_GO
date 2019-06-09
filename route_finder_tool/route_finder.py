#! python3
"""This is a tool to work with the data gathered by my web scraper_tool. It searches a json file
for criteria such as area, sub area, or grade.

Currently I have it set up somewhat redundantly. The option_finder will narrow down area and grade,
and returns the criteria and a narrower list that gets fed into find_by_criteria.
The regex and escape_character are designed to ignore series of numbers in the http address and for the . in grades.
"""
import json
import re
from route_finder_tool import option_finder


"""
IDEA:
Make option finder work better...
    it needs to give the option for area or grade
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
    list_ = []

    criteria, area = option_finder.criteria_selector(climbing_list)

    for i in climbing_list:
        if area in i:
            list_.append(i)

    x = list(filter(find_by_criteria, list_))

    for i in x:
        print(i[0])
