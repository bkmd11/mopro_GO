#! python3

"""This is a tool to work with the data gathered by my web scraper. It will be able
to search a json file for the climbs that meet a given criteria, whether that is
location or grade, could also go for trad/sport/boulder.


"""
import json
import pprint
import sys
import re


"""Trying to make this search for grade variations with a regex
example: V0+, 510d. Also my grade data from mountain_project.py 
has a blank space at the end. Could add a strip to remove the bug
or just deal with it in this regex

It works as a CLI taking sys.argv[1] as the regex


IDEA:
Make a grade finder that adds \ to .
Make an area/sub area finder that considers case and extra symbols
"""


def regex(search_term):
    search_word = '{}.*'.format(search_term)
    regex = re.compile(search_word)

    return regex


# Takes a list of climbs and searches for a given criteria term
#### This function can return things that do not meet the desired regex...
#### . has a special meaning in regex, so searching for grade doesnt work
#### maybe listify the string, find the . index, then insert before that...
#### probably way over complicated...
#### I could just be self aware of the bug and work with it since nobody
#### else will ever use this POS
def find_by_criteria(list_of_climbs):
    search_term = regex(sys.argv[1])

    filtered_list = list(filter(search_term.search, list_of_climbs))

    return filtered_list

"""
# Currently my main body for my shitty testing
with open('off_width.json', 'r') as file:
    climbing_list = json.load(file)


x = list(filter(find_by_criteria, climbing_list))

for i in x:
    pprint.pprint(i)
#pprint.pprint(x)


"""