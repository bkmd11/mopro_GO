import PySimpleGUI as psg
import webbrowser

from route_finder_tool import select_climb_queries as scq


def main_area_menu(connection, **kwargs):
    """ A drop down menu that shows all of the main areas"""
    options = scq.get_main_areas_query(connection)

    return psg.InputCombo([i for i in options], key='AREA', size=(30, 1), **kwargs)


def sub_area_menu(connection, main_area_input, **kwargs):
    """A drop down menu that shows all sub areas"""
    area = []
    if main_area_input:
        area = scq.get_sub_areas_query(connection, main_area_input)

    return psg.InputCombo([i for i in area], key='SUB_AREA', size=(30, 1), **kwargs)


def climb_menu(connection, sub_area_input):
    """A list box of all climbs in a sub area"""
    climbs = []
    if sub_area_input:
        climbs = scq.get_climbs_by_sub_area(connection, sub_area_input)

    list_of_climbs = [f'{i[0]} - {i[1]}' for i in climbs]

    return psg.Listbox(list_of_climbs, key='CLIMB', size=(30, len(list_of_climbs)))


def load_climb(connection, climb_name):
    """Loads the climb url into webbrowser"""
    climb_url = scq.get_climb_url_query(connection, climb_name)

    webbrowser.open(climb_url[0][0])


def search_button():
    """The magic button"""
    return psg.Button('Search')


def launch_button():
    """launches webbrowser"""
    return psg.Button('Launch Site!')


def window_layout(connection, main_area, sub_area):
    """ The window layout"""
    layout = [[main_area_menu(connection, default_value=main_area)],
              [sub_area_menu(connection, main_area, default_value=sub_area[0])],
              [climb_menu(connection, sub_area[0])],
              [search_button(), launch_button()]
              ]

    return psg.Window('Awesome Climb Finder', layout)


def help_window(text):
    """A somewhat useful help window"""
    layout = [[psg.Text(text)],
              [psg.Ok()]
             ]

    return psg.Window('Oops', layout)


def main_window():
    reset_search = {'AREA': ''}    # this value makes it so if main area gets changed everything can reset
    connection = scq.create_connection('Brian Kendall', 'spam')

    window = window_layout(connection, '', ('',))

    while True:
        event, value = window.read()
        if event in (None, 'Escape:27'):
            break
        elif event == 'Search':
            print(value)
            if value['AREA'] == reset_search['AREA']:
                window.close()
                window = window_layout(connection, value['AREA'], (value['SUB_AREA'],))
                reset_search = value

            else:
                window.close()
                window = window_layout(connection, value['AREA'], ('',))
                reset_search = value
        elif event == 'Launch Site!':
            try:
                climb_info = value['CLIMB'][0].split('-')
                climb_name = climb_info[0].strip()
                load_climb(connection, climb_name)
            except IndexError as e:
                help_me = help_window('Try selecting the climb before launching')
                event, value = help_me.read()
                while True:
                    if event in (None, 'Ok'):
                        help_me.close()
                        break


if __name__ == '__main__':
    main_window()
