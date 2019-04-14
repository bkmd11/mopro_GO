"""This is a tool to work with the data gathered by my web scraper. It will be able
to search a json file for the climbs that meet a given criteria, whether that is
location or grade, could also go for trad/sport/boulder.


"""
import json
import pprint
import sys
import re


"""It works as a CLI taking sys.argv[1] as the regex


IDEA:
Make an area/sub area finder that considers case and extra symbols
"""


# Makes the user input into a regex to find variations of grade
def regex(search_term):
    search_word = '{}.*'.format(search_term)
    regex = re.compile(search_word)

    return regex


# Adds an escape charecter for the '.' in a grade
def escape_character(climbing_grade):
    list_ = list(climbing_grade)
    add_backslash = [x if x != '.' else '\\.' for x in list_]
    string = ''.join(add_backslash)

    return string
# Takes a list of climbs and searches for a given criteria term
def find_by_criteria(list_of_climbs):
    search_term = regex(sys.argv[1])   # Must add \ for . in grade

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
