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
def grade_options(json_file):
    list_ = []
    for i in json_file:
        list_.append(i[-1])
    list_ = list(dict.fromkeys(list_))
    list_.sort()

    return list_
