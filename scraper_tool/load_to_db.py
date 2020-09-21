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
    query_id = None
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query, data)
        query_id = cursor.fetchone()[0]

    except OperationalError as e:
        print(f'Error {e} during query')

    return query_id


def insert_climb(climb_data, connection):
    """The query to load into climb table
        CLIMB_DATA MUST BE TUPLE"""
    climb_id = None
    try:
        insert_climb_query = 'INSERT INTO climbs (climb_name, url, grade) VALUES (%s, %s, %s) RETURNING id;'
        climb_id = execute_query(connection, insert_climb_query, climb_data)
    except psycopg2.Error as e:
        if e.pgcode == '23505':
            climb_id_query = 'SELECT id FROM climbs WHERE url = %s;'
            climb_id = execute_query(connection, climb_id_query, (climb_data[1],))

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


def sub_area_query(sub_area_data, connection):
    """ The query to insert into sub_area table
    SUB_AREA_DATA MUST BE TUPLE"""

    insert_sub_area = 'INSERT INTO sub_area (area, climb_id, area_id) VALUES (%s, %s, %s) RETURNING id;'
    sub_area_id = execute_query(connection, insert_sub_area, sub_area_data)

    return sub_area_id


def style_query(style_data, connection):
    """The query to insert into climb_style table
    STYLE DATA MUST BE TUPLE"""
    style_id = None
    try:
        insert_style = 'INSERT INTO climb_style (climb_style) VALUES (%s) RETURNING id;'
        style_id = execute_query(connection, insert_style, style_data)
    except psycopg2.Error as e:
        if e.pgcode == '23505':
            style_id_query = 'SELECT id FROM climb_style WHERE climb_style = %s'
            style_id = execute_query(connection, style_id_query, style_data)

    return style_id


def insert_style_guide_query(climb_data, connection):
    """Inserts a climb and it's style into the style_guide table
    CLIMB_DATA MUST BE TUPLE"""
    id_key = None
    try:
        insert_query = 'INSERT INTO style_guide (climb_name, style) VALUES (%s, %s) RETURNING 1;'
        id_key = execute_query(connection, insert_query, climb_data)
    except psycopg2.Error as e:
        if e.pgcode == '23505':
            insert_query = 'SELECT (climb_name, style) FROM style_guide WHERE climb_name = %s AND style = %s'
            id_key = execute_query(connection, insert_query, climb_data)
    return id_key


def main_query(connection, scrapped_data):
    """Runs all the queries to populate tables. If the url is already in climbs table, it bypasses to reduce
        redundancies and just fills in the climb_style information"""
    style_id = style_query((scrapped_data[-1],), connection)
    climb_id = insert_climb((scrapped_data[1], scrapped_data[0], scrapped_data[4]), connection)
    main_area_id = insert_main_area((scrapped_data[2],), connection)

    sub_area_id = sub_area_query((scrapped_data[3], climb_id, main_area_id), connection)

    print(f'{Fore.BLUE}"{scrapped_data[1]}" loaded into database')


