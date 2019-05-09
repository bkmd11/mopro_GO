""" The goal of this project is to find all the off width climbs on mountain
project. It will use requests and BeautifulSoup to gather this info and save
it to a file with links to the climbs page, ordered by grade. 

This will be my masterpiece.

My next step is to make a tool to run on the json file that will pull out what I want
based on either grade or area.

I also want to add asyncio or threading
"""

import json

import web_crawler
import page_search


def main():
    # Loops through every area and sub area
    climb_links = web_crawler.main_loop('https://www.mountainproject.com/area/105946021/blair-woods')
    print('searching for climb awesomeness')
    
    # Goes through climb links to search for regex
    off_widths = page_search.awesome_climb(climb_links)
    print('Writing to file')
    
    with open('test.json', 'w') as climb_file:
        json.dump(off_widths,climb_file)


if __name__ == '__main__':
    main()
