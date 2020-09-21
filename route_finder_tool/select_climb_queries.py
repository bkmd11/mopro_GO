import psycopg2
from psycopg2 import OperationalError

import json

# TODO: Need to make query to select style from style_guide table

def create_connection(database, username, pw, host):
    """Creates the connection to database"""
    connection = None
    try:
        connection = psycopg2.connect(
            database=database,
            user=username,
            password=pw,
            host=host
        )
        print('Connected to mopro_climbs')
    except OperationalError as e:
        print(f'Error {e} during connection')

    return connection


def execute_query(connection, query, data=None):
    """Executes the query"""
    results = []
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        if data is None:
            cursor.execute(query)

        else:
            cursor.execute(query, data)

        results = [i for i in cursor]

    except OperationalError as e:
        print(f'Error {e} during query')

    return results


def get_styles_query(connection):
    """Gets the style option available in database"""
    query = 'SELECT climb_style FROM climb_style;'
    result = execute_query(connection, query)

    return result


def get_style_id_query(connection, style):
    """ Gets the id of a given style"""
    query = 'SELECT id FROM climb_style WHERE climb_style = %s'
    result = execute_query(connection, query, style)

    return result


def get_main_areas_query(connection):
    """Gets the main areas from the database"""
    query = 'SELECT area FROM main_area;'
    results = execute_query(connection, query)

    return results


def get_sub_areas_query(connection, main_area):
    """Gets the sub areas from the database"""

    main_id = get_main_area_id_query(connection, main_area)
    query = 'SELECT DISTINCT area FROM sub_area WHERE area_id = %s;'
    result = execute_query(connection, query, (main_id[0],))

    return result


def get_main_area_id_query(connection, main_area):
    """Returns the main area id """
    main_area_id_query = 'SELECT id FROM main_area WHERE area = %s;'
    result = execute_query(connection, main_area_id_query, (main_area,))

    return result


def get_climbs_by_style(connection, sub_area, style_id):
    """ Gets climbs of a certain style"""
    query = 'SELECT climb_name, grade FROM climbs, WHERE sub_area.area = %s and sub_area.climb_id = climbs.id and climbs.style = %s'
    result = execute_query(connection, query, (sub_area, style_id))

    return result


def get_climbs_by_sub_area(connection, sub_area):
    """ gets all climbs from a sub area"""

    query = 'SELECT climb_name, grade FROM climbs, sub_area WHERE sub_area.area = %s and sub_area.climb_id = climbs.id'

    result = execute_query(connection, query, (sub_area,))

    return result


def get_climb_url_query(connection, climb_name):
    """Retrieves the url for a climb"""
    query = 'SELECT url FROM climbs WHERE climb_name = %s'
    result = execute_query(connection, query, (climb_name,))

    return result
