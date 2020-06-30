import PySimpleGUI as psg
import webbrowser
import json

from route_finder_tool import select_climb_queries as scq


def title_bar(text):
    """Title bar for the various dropdown menus"""

    return psg.Text(text, font=(None, 20), text_color='black', )


def main_area_menu(connection, **kwargs):
    """ A drop down menu that shows all of the main areas"""
    options = scq.get_main_areas_query(connection)

    return psg.Combo([i for i in options], key='AREA', font=(None, 20), size=(30, 1), enable_events=True, **kwargs)


def sub_area_menu(connection, main_area_input, **kwargs):
    """A drop down menu that shows all sub areas"""
    area = []
    if main_area_input:
        area = scq.get_sub_areas_query(connection, main_area_input)

    return psg.Combo([i for i in area], key='SUB_AREA', font=(None, 20), enable_events=True, size=(30, 1),  **kwargs)


def climb_menu(connection, sub_area_input):
    """A list box of all climbs in a sub area"""
    climbs = []
    if sub_area_input:
        climbs = scq.get_climbs_by_sub_area(connection, sub_area_input)

    list_of_climbs = [f'{i[0]} -> {i[1]}' for i in climbs]

    return psg.Listbox(list_of_climbs, key='CLIMB', no_scrollbar=True, enable_events=True, font=(None, 15), size=(42, len(list_of_climbs),))


def load_climb(connection, climb_name):
    """Loads the climb url into webbrowser"""
    climb_url = scq.get_climb_url_query(connection, climb_name)

    webbrowser.open(climb_url[0][0])


def search_button():
    """The magic button"""
    return psg.Button('Search', font=20)


def launch_button():
    """launches webbrowser"""
    return psg.Button('Launch Site!', font=20)


def window_layout(connection, main_area, sub_area):
    """ The window layout"""
    layout = [[title_bar('Main Area')],
              [main_area_menu(connection, default_value=main_area)],
              [title_bar('Sub Area')],
              [sub_area_menu(connection, main_area, default_value=sub_area[0])],
              [title_bar('Climbs')],
              [climb_menu(connection, sub_area[0])]
              ]

    return psg.Window('Awesome Climb Finder', layout, element_justification='center')


def help_window(text):
    """A somewhat useful help window"""
    layout = [[psg.Text(text, font=(None, 30), text_color='black', background_color='red')],
              [psg.Ok(font=(None, 30), button_color=('red', 'dark red'))]
             ]

    return psg.Window('Oops', layout, element_justification='center', background_color='red')


def main_window(database, username, password, host):
    reset_search = {'AREA': ''}    # this value makes it so if main area gets changed everything can reset
    connection = scq.create_connection(database, username, password, host)

    window = window_layout(connection, '', ('',))

    while True:
        event, value = window.read()
        # print(event)
        if event in (None, 'Escape:27'):
            break
        elif event in ('AREA', 'SUB_AREA'):
            # print(value)
            if value['AREA'] == reset_search['AREA']:
                window.close()
                window = window_layout(connection, value['AREA'], (value['SUB_AREA'],))
                reset_search = value

            else:
                window.close()
                window = window_layout(connection, value['AREA'], ('',))
                reset_search = value
        elif event == 'CLIMB':
            try:
                climb_info = value['CLIMB'][0].split('->')
                climb_name = climb_info[0].strip()
                load_climb(connection, climb_name)
            except IndexError as e:
                help_me = help_window('Try selecting the climb before launching')
                # print(e)
                event, value = help_me.read()
                while True:
                    if event in (None, 'Ok'):
                        help_me.close()
                        break


if __name__ == '__main__':
    with open(r'/db_credentials.json', 'r') as file:
        credentials = json.load(file)
    main_window(credentials['database'], credentials['username'], credentials['password'], credentials['host'])
