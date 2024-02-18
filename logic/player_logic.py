import random
import math


def initialiseDict(player_name, character=''):
    """Will only need to initialise dict like this once, elsewhere
    will get straight from mongodb
    """
    player_dict = {'player_name': player_name,
                'character': character,
                'vote': '',
                'status': 'alive'}
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

def whoLost(players, stage):
    votes = {p:0 for p in [*players]}
    for player_name, player in players.items():
        if player['character'] == 'wolf':
            votes[player['vote']] += 1
    sorted_dict = dict(sorted(votes.items(), key=lambda item: item[1], reverse=True))
    # Is this random in case of tie draw?
    losing_player = [*sorted_dict][0]
    # losing_player = next(iter(sorted_dict.items()))
    return losing_player

def killPlayer(players, losing_player):
    players[losing_player]['status'] = 'dead'
    return players

def getPlayersFromSession(session, game):
    player_name = session.get('player_name', None)
    players = game['players']
    return players, player_name

def getPlayersLists(players, player_name):
    player = players[player_name]
    other_players = [v for k,v in players.items() if k != player_name]
    alive_players = [p for p in other_players if p['status'] == 'alive']
    alive_villagers = [p for p in alive_players if p['character'] == 'villager']
    dead_players = [p for p in other_players if p['status'] == 'dead']
    return player, alive_players, alive_villagers, dead_players

def resetVotes(players):
    for k in players.keys():
        players[k]['vote'] = ''
    return players