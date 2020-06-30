# mountain_project
A web scraper to find particular climbs on mountain project

First set up a postgreSQL database with build_query.sql.
Credentials should be saved to a json file formatted as:
{
  "database": "database_name",
  "username": "user_name",
  "password": "pass_word",
  "host": "host_address"
}
The path for your json file will need to be updated in both route_finder.py and mopro_scraper.py

Run mopro_scrapper.py and enter a mountain project link for an area. The program will run to find climbs that are off-widths and then save it to a database.

To access the database, run route_finder.py and use the drop down menus to filter out climbs in specified areas.
