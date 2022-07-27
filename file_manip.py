def settings_retriever(vol: dict, auto_pause: dict, games: dict) -> None:
    """
    Reads a file storing the data for volume adjustment and another file storing
    data to autopause spotify on certain sites.
    """
    with open("vol.txt", 'r') as volly:
        volly.readline()
        volly.readline()
        x = volly.readlines()
        non_games = []
        game = []

        # Sifting through the data file
        gam = True
        for line in x:
            if "NOT GAMES" in line:
                gam = False
            elif line == '\n':
                pass
            elif gam:
                y = line.strip()
                game.extend(y.split('='))
            else:
                y = line.strip()
                non_games.extend(y.split('='))

        num = False
        prev = None
        # Storing the non_games into a list, they don't need volume
        # adjustment
        for stuff in non_games:
            if num:
                vol[prev] = float(stuff)
                num = False
            else:
                vol[stuff] = None
                prev = stuff
                num = True

        num = False
        prev = None
        # Storing the games into a list
        for stuff in game:
            if num:
                vol[prev] = float(stuff)
                games[prev] = float(stuff)
                num = False
            else:
                vol[stuff] = None
                games[stuff] = None
                prev = stuff
                num = True

    # setting up auto pause configurations
    with open('auto.txt', 'r') as auto:
        auto.readline()
        x = auto.readlines()
        w = []

        for line in x:
            y = line.strip()
            w.extend(y.split('='))

        skip = False
        prev = None

        for stuff in w:
            if skip:
                # '1' means auto pause on, '0' means autopause off
                if stuff == '1':
                    auto_pause[prev] = True
                    skip = False
                else:
                    auto_pause[prev] = False
                    skip = False
            else:
                auto_pause[stuff] = False
                prev = stuff
                skip = True


def vol_app_adder(name: str, level=1.0) -> None:
    """
    adds new app to vol.txt if not already in the file.

    Note: currently not going to support adding volume level, will just set it
          to 1.
    """
    with open('vol.txt', 'a') as volly:
        volly.write(name + '=' + str(level) + '\n')
