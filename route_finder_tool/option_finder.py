#! python3
import pprint


# Finds all the areas
def area_options(json_file):
    list_ = []
    for i in json_file:
        list_.append(i[1])

    list_ = list(dict.fromkeys(list_))
    list_.sort()

    return list_


# Finds all the sub areas in the selected area
def sub_area_options(area, json_file):
    list_ = []
    for i in json_file:
        if area in i:
            list_.append(i[2])
    list_ = list(dict.fromkeys(list_))
    list_.sort()

    return list_


# Finds all the grades in an area
def grade_options(area, json_file):
    list_ = []
    for i in json_file:
        if area in i:
            list_.append(i[-1])
    list_ = list(dict.fromkeys(list_))
    list_.sort()

    return list_


# Makes a list of valid choices to eliminate guess work as to whats on the list
def criteria_selector(json_file):
    search_options = area_options(json_file)
    pprint.pprint(search_options)
    area = input('Make a selection from the list:\n')

    grade_or_area = input('Do you want to narrow down to "sub_area" or "grade"?\n')
    if grade_or_area == 'sub_area':
        narrower_search_options = sub_area_options(area, json_file)
        pprint.pprint(narrower_search_options)
        area = input('Make a selection from the list:\n')

    grade_search = grade_options(area, json_file)
    pprint.pprint(grade_search)
    search_criteria = input('Make a selection from the list:\n')

    return search_criteria, area

