#! python3
"""This is a tool to work with the data gathered by my web scraper_tool. It searches a json file
for criteria such as area, sub area, or grade.

Currently I have it set up somewhat redundantly. The option_finder will narrow down area and grade,
and returns the criteria and a narrower list that gets fed into find_by_criteria.
The regex and escape_character are designed to ignore series of numbers in the http address and for the . in grades.
"""
import json
import re
import pprint

from route_finder_tool import option_finder

# TODO: Make a GUI with sexy click buttons


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
    search_term = regex(criteria)

    filtered_list = [i for i in list_of_climbs if search_term.search(str(i))]

    return filtered_list


# Makes a filtered list of the areas from a given criteria
def area_slimmer_downer(area_option, list_of_climbs):
    list_ = [i for i in list_of_climbs if area_option in i]

    return list_


if __name__ == '__main__':
    with open('rumney.json', 'r') as file:
        climbing_list = json.load(file)

    choice = input('"grade" or "area":\n')

    if choice == 'area':
        narrower_search_options = option_finder.area_options(climbing_list)
        pprint.pprint(narrower_search_options)

        area = input('Make a selection from the list:\n')
        climbing_list = area_slimmer_downer(area, climbing_list)

        choice = input('"sub_area" or "grade":\n')

        if choice == 'sub_area':
            narrower_search_options = option_finder.sub_area_options(climbing_list)
            pprint.pprint(narrower_search_options)
            area = input('Make a selection from the list:\n')

            climbing_list = area_slimmer_downer(area, climbing_list)

    grades = option_finder.grade_options(climbing_list)
    pprint.pprint(grades)

    criteria = input('Make a selection from the list:\n')

    list_filtered_by_criteria = find_by_criteria(climbing_list)

    for climb in list_filtered_by_criteria:
        print(climb[0])

""" I've made this work a bit better. In option finder.py I eliminated a couple things I didnt like.
Error prone still, but I can make it work for me. Might break if I look for more than grade...
"""