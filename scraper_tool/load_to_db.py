import psycopg2
from psycopg2 import OperationalError


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
        print('Query complete')
        id = cursor.fetchone()[0]
    except OperationalError as e:
        print(f'Error {e} during query')

    return id


def main_query(username, password, scrapped_data):
    try:
        connection = create_connection(username, password)

        climbs = (scrapped_data[1], scrapped_data[0], scrapped_data[4])
        insert_climb_query = 'INSERT INTO climbs (climb_name, url, grade) VALUES (%s, %s, %s) RETURNING id;'
        climb_id = execute_query(connection, insert_climb_query, climbs)

        main_area = (scrapped_data[2],)
        insert_main_area = 'INSERT INTO main_area (area) VALUES (%s) RETURNING id;'
        main_area_id = execute_query(connection, insert_main_area, main_area)

        sub_area = (scrapped_data[3], climb_id, main_area_id)
        insert_sub_area = 'INSERT INTO sub_area (area, climb_id, area_id) VALUES (%s, %s, %s) RETURNING id;'
        sub_area_id = execute_query(connection, insert_sub_area, sub_area)

        style = (scrapped_data[-1], climb_id)
        insert_style = 'INSERT INTO climb_style (climb_style, climb_id) VALUES (%s, %s) RETURNING id;'
        style_id = execute_query(connection, insert_style, style)
    except psycopg2.Error as e:
        print(e)


SCRAPPED_DATA = [
    'https://www.mountainproject.com/route/106540643/no-answer',
    'No Answer',
    'pawtuckaway',
    'upper-cliff',
    '5.8 ',
    'ow']

main_query(SCRAPPED_DATA)
