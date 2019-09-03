""" The goal of this project is to find all the off width climbs on mountain
project. It will use requests and BeautifulSoup to gather this info and save
it to a file with links to the climbs page, ordered by grade. 

This will be my masterpiece.
"""

import json

from scraper_tool import web_crawler
from scraper_tool import async_page_search

# Todo: make this run with asyncio too


def main():
    # Loops through every area and sub area
    climb_links = web_crawler.main_loop('https://www.mountainproject.com/area/105946021/blair-woods')
    
    # Goes through climb links to search for regex
    off_widths = async_page_search.main(climb_links)
    print('Writing to file')
    
    with open('test.json', 'w') as climb_file:
        json.dump(off_widths,climb_file)


if __name__ == '__main__':
    main()
