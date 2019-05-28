"""This is a tool to work with the data gathered by my web scraper. It will be able
to search a json file for the climbs that meet a given criteria, whether that is
location or grade, could also go for trad/sport/boulder.


"""
import json
import re

from route_finder import option_finder


"""It works as a CLI taking sys.argv[1] as the regex


IDEA:
Make an area/sub area finder that considers case and extra symbols
Need to make this more user friendly
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
def find_by_criteria(search_criteria, list_of_climbs):
    search_term = regex(search_criteria)

    filtered_list = list(filter(search_term.search, list_of_climbs))

    return filtered_list


def main():
    with open('off_width.json', 'r') as file:
        climbing_list = json.load(file)

    x = list(filter(find_by_criteria, climbing_list))

    for i in x:
        print(i[0])


if __name__ == '__main__':
    main()
