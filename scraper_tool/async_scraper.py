import json
import time
import asyncio

from scraper_tool import async_web_crawler
from scraper_tool import async_page_search


async def main():
    # Loops through every area and sub area
    climb_links = await async_web_crawler.main(['https://www.mountainproject.com/area/105946021/blair-woods'])

    # Goes through climb links to search for regex
    off_widths = async_page_search.crawler(climb_links)
    print('Writing to file')

    with open('test.json', 'w') as climb_file:
        json.dump(str(off_widths), climb_file)


if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(main())
    print(f'{time.time() - start_time}')
