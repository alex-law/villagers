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
    shuffled_player_names = [*players]
    random.shuffle(shuffled_player_names)
    #Want roughly 20% of players to be wolfs rounding up
    wolf_count = math.ceil(len(players)*0.2)
    for p in shuffled_player_names[:wolf_count]:
        players[p]['character'] = 'wolf'
    for p in shuffled_player_names[wolf_count:]:
        players[p]['character'] = 'villager'
    return players

def updateMongoPlayer(game, player, db):
    filter = {'_id': game['_id']}
    update_fields = {
            '$set': {
                f'players.{player["player_name"]}': player
                }
        }
    # Update the document
    result = db.collection.update_one(filter, update_fields, upsert=False)
    return result

def getLooser():
    pass

def getPlayersFromSession(session, game):
    player_name = session.get('player_name', None)
    players = game['players']
    return players, player_name