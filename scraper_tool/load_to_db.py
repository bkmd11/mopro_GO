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


def main_query(connection, scrapped_data):
    """Runs all the queries to populate tables. If the url is already in climbs table, it bypasses to reduce
        redundancies and just fills in the climb_style information"""
    climb_id = None
    main_area_id = None

    try:
        climbs = (scrapped_data[1], scrapped_data[0], scrapped_data[4])
        insert_climb_query = 'INSERT INTO climbs (climb_name, url, grade) VALUES (%s, %s, %s) RETURNING id;'
        climb_id = execute_query(connection, insert_climb_query, climbs)
    except psycopg2.Error as e:
        if e.pgcode == '23505':
            climb_id_query = 'SELECT id FROM climbs WHERE url = %s'
            climb_id = execute_query(connection, climb_id_query, (scrapped_data[0],))
    try:
        main_area = (scrapped_data[2],)
        insert_main_area = 'INSERT INTO main_area (area) VALUES (%s) RETURNING id;'
        main_area_id = execute_query(connection, insert_main_area, main_area)
    except psycopg2.Error as e:
        if e.pgcode == '23505':
            main_area_id_query = 'SELECT id FROM main_area WHERE area = %s;'
            main_area_id = execute_query(connection, main_area_id_query, (scrapped_data[2], ))

    sub_area = (scrapped_data[3], climb_id, main_area_id)
    insert_sub_area = 'INSERT INTO sub_area (area, climb_id, area_id) VALUES (%s, %s, %s) RETURNING id;'
    sub_area_id = execute_query(connection, insert_sub_area, sub_area)

    style = (scrapped_data[-1], climb_id)
    insert_style = 'INSERT INTO climb_style (climb_style, climb_id) VALUES (%s, %s) RETURNING id;'
    style_id = execute_query(connection, insert_style, style)

    print(f'{Fore.BLUE}"{scrapped_data[1]}" loaded into database')


if __name__ == '__main__':
    """ Testing purposes"""
    with open('test.json', 'r') as file:
        data = json.load(file)

    with open('db_credentials.json', 'r') as file:
        credentials = json.load(file)

    connection = create_connection(credentials['username'], credentials['password'])
    for i in data:
        main_query(connection, i)
