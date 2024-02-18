from bson import ObjectId

def initialiseDict(game_id, player):
    """Will only need to initialise dict like this once, elsewhere
    will get straight from mongodb
    """
    # Need some way of indexing players to update from mongodb, so just use name as key
    game_dict = {'players': {player['player_name']: player},
                 'status': 'initialised',
                 'round': 1,
                 'game_id': game_id}
    return game_dict

def getGameFromSession(session, db):
    _id = ObjectId(session.get('_id', None))
    game = db.collection.find_one({'_id': _id})
    return game, _id