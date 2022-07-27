import PySimpleGUI as sg
from file_manip import settings_retriever


def create_win(games: dict)->None:
    # creating the buttons for the games
    column = [
        [sg.Button(f'{nom}={games[nom]}')] for nom in games
    ]
    # setting the desired layout
    layout = [
        [sg.Column(column, scrollable=True, vertical_scroll_only=True)]
    ]
    # creating the actual window
    window = sg.Window('Spotify Background Adjust', layout, margins=(400, 200))

    while True:
        event, values = window.read()
        print(event)
        event_process = ''
        if type(event) == str:
            if '=' in event:
                event_process = event.split('=')[0]


        # End program if user closes window or presses the OK button
        if event == sg.WIN_CLOSED:
            break
        elif event_process in games:
            window.close()
            column.pop(0)
            window = sg.Window('Spotty_backy', layout, margins=(400, 200))

    window.close()

if __name__ == '__main__':
    gamesy ={}
    autos ={}
    vols ={}

    settings_retriever(vols, autos, gamesy)
    create_win(gamesy)
