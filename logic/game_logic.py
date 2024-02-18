from bson import ObjectId
from logic import player_logic

def initialiseDict(game_id, player):
    """Will only need to initialise dict like this once, elsewhere
    will get straight from mongodb
    """
    # Need some way of indexing players to update from mongodb, so just use name as key
    game_dict = {'players': {player['player_name']: player},
                 'status': 'initialised',
                 'round': 1,
                 'stage': 'night',
                 'game_id': game_id}
    return game_dict

def getGameFromSession(session, db):
    _id = ObjectId(session.get('_id', None))
    game = db.collection.find_one({'_id': _id})
    return game, _id

def replaceGame(game, db, _id):
    db.collection.replace_one({'_id': _id}, game)

def endOfPlay(game, db, _id):
    players = game['players']
    losing_player = player_logic.whoLost(players, game['stage'])
    players = player_logic.killPlayer(players, losing_player)
    players = player_logic.resetVotes(players)
    game['players'] = players
    #Update stage and round depending on current stage and round
    if game['stage'] == 'night':
        game['round'] += 1
        game['stage'] = 'day'
    else:
        game['stage'] = 'night'
    replaceGame(game, db, _id)
    return game

