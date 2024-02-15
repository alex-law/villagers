from flask import request

def getUserInput():
    player_name = request.form.get("player_name")
    game_id = request.form.get("game_id")
    new_game = request.form.get("new_game")
    return player_name, game_id, new_game

def validateInput(player_name, game_id, new_game, db):
    #If no player name return tell user
    if len(player_name.strip()) == 0:
        return False, 'Please enter a user name'
    if (len(game_id.strip()) == 0 and new_game is None):
        return False, 'Please select new game or enter a game id'
    #If game id already exists and user is trying to start a new game
    if (db.collection.find_one({'game_id': game_id}) is not None) and (new_game is not None):
        return False, 'Game id is currently in use, please choose a new id'
    #If game id does not exist and user is trying to join game
    if (db.collection.find_one({'game_id': game_id}) is None) and (new_game is None):
        return False, 'Game id does not exist, please check your game id or request a new one'
    #If passed all these now return true and no failure message
    return True, ''
    