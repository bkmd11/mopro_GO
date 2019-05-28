#! python3

import json
import sys
import pprint


# Finds all the areas
def options(list_index, json_file):
    list_ = []
    for i in json_file:
        list_.append(i[list_index])

    list_ = list(dict.fromkeys(list_))
    list_.sort()

    return list_


# Makes a list of valid choices to eliminate guess work as to whats on the list
def criteria_selector(json_file):
    criteria = input('area, sub_area, or grade?\n')
    if criteria == 'area':
        search_options = options(1, json_file)

    elif criteria == 'sub_area':
        search_options = options(2, json_file)

    elif criteria == 'grade':
        search_options = options(-1, json_file)

    else:
        print('invalid option')
        sys.exit()

    pprint.pprint(search_options)

    search_by_criteria = input('Make a selection from the list:\n')

    return search_by_criteria






