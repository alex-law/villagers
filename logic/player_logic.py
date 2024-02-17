def initialiseDict(player_name, character=''):
    """Will only need to initialise dict like this once, elsewhere
    will get straight from mongodb
    """
    player_dict = {'player_name': player_name,
                'character': character}
    return player_dict