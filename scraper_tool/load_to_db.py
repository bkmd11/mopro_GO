import psycopg2
from psycopg2 import OperationalError

from colorama import Fore

import json


def create_connection(username, pw):
    """Creates the connection to database"""
    connection = None
    try:
        connection = psycopg2.connect(
            database='mopro_climbs',
            user=username,
            password=pw,
            host='localhost'
        )
        print('Connected to mopro_climbs')
    except OperationalError as e:
        print(f'Error {e} during connection')

    return connection


def execute_query(connection, query, data):
    """Executes the query"""
    id = None
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query, data)
        id = cursor.fetchone()[0]

    except OperationalError as e:
        print(f'Error {e} during query')

    return id


def insert_climb(climb_data, connection):
    """The query to load into climb table
        CLIMB_DATA MUST BE TUPLE"""
    climb_id = None
    try:
        insert_climb_query = 'INSERT INTO climbs (climb_name, url, grade) VALUES (%s, %s, %s) RETURNING id;'
        climb_id = execute_query(connection, insert_climb_query, climb_data)
    except psycopg2.Error as e:
        if e.pgcode == '23505':
            climb_id_query = 'SELECT id FROM climbs WHERE url = %s'
            climb_id = execute_query(connection, climb_id_query, (climb_data[0],))

    return climb_id


def insert_main_area(area_data, connection):
    """ The query to load into main_area table
        AREA_DATA MUST BE TUPLE"""
    main_area_id = None
    try:
        insert_main_area = 'INSERT INTO main_area (area) VALUES (%s) RETURNING id;'
        main_area_id = execute_query(connection, insert_main_area, area_data)
    except psycopg2.Error as e:
        if e.pgcode == '23505':
            main_area_id_query = 'SELECT id FROM main_area WHERE area = %s;'
            main_area_id = execute_query(connection, main_area_id_query, area_data)

    return main_area_id


def sub_area_query(sub_area_data, climb_id, main_area_id, connection):
    """ The query to insert into sub_area table
    SUB_AREA_DATA MUST BE TUPLE"""

    sub_area = (sub_area_data, climb_id, main_area_id)
    insert_sub_area = 'INSERT INTO sub_area (area, climb_id, area_id) VALUES (%s, %s, %s) RETURNING id;'
    sub_area_id = execute_query(connection, insert_sub_area, sub_area)

    return sub_area_id


def style_query(style_data, connection):
    """The query to insert into climb_style table
    STYLE DATA MUST BE TUPLE"""

    insert_style = 'INSERT INTO climb_style (climb_style, climb_id) VALUES (%s, %s) RETURNING id;'
    style_id = execute_query(connection, insert_style, style_data)

    return style_id


def main_query(connection, scrapped_data):
    """Runs all the queries to populate tables. If the url is already in climbs table, it bypasses to reduce
        redundancies and just fills in the climb_style information"""
    climb_id = insert_climb((scrapped_data[1], scrapped_data[0], scrapped_data[4]), connection)
    main_area_id = insert_main_area((scrapped_data[2],), connection)

    sub_area_id = sub_area_query((scrapped_data[3], climb_id, main_area_id), climb_id, main_area_id, connection)
    style = style_query((scrapped_data[-1], climb_id), connection)

    print(f'{Fore.BLUE}"{scrapped_data[1]}" loaded into database')


if __name__ == '__main__':
    """ Testing purposes"""
    with open('test.json', 'r') as file:
        data = json.load(file)

    with open(r'C:\Users\Brian Kendall\Desktop\off_width_scraper\db_credentials.json', 'r') as file:
        credentials = json.load(file)

    connection = create_connection(credentials['username'], credentials['password'])
    for i in data:
        main_query(connection, i)
