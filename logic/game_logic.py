

def initialiseDict(game_id, player):
    """Will only need to initialise dict like this once, elsewhere
    will get straight from mongodb
    """
    game_dict = {'players': [player],
                 'status': 'initialised',
                 'round': 1,
                 'game_id': game_id}
    return game_dict

