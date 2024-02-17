import random
import math


def initialiseDict(player_name, character=''):
    """Will only need to initialise dict like this once, elsewhere
    will get straight from mongodb
    """
    player_dict = {'player_name': player_name,
                'character': character,
                'vote': ''}
    return player_dict

def assignCharacters(players):
    # Shuffle to randomly assign characters
    random.shuffle(players)
    #Want roughly 20% of players to be wolfs rounding up
    wolf_count = math.ceil(len(players)*0.2)
    for c in range(0, wolf_count):
        players[c]['character'] = 'wolf'
    for c in range(wolf_count, len(players)):
        players[c]['character'] = 'villager'
    return players