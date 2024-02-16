from flask import request
from villageObjects import gameObj, playerObj

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
    
def startNewGame(player, game_id, db):
    #Initiate game obj
    game = gameObj(player, init_game_id=game_id)
    #save game to db
    game.mongo_id = db.collection.insert_one(game.gameToDict()).inserted_id
    return game

def checkExistingPlayer(player, game_db):
    #Check to make sure that player doesn't already exist
    curr_players = game_db['players']
    if player.player_name in [p['player_name'] for p in curr_players]:
        return False, 'Player name already taken, please pick a new one'
    else:
        return True, ''

def startExistingGame(player, game_db, db):
    #Add new player
    game_db['players'].append(player.toDict())
    filter = {'_id': game_db['_id']}
    update_fields = {'$set': {'players': game_db['players']}}
    # Update the document
    result = db.collection.update_one(filter, update_fields, upsert=False)
    # Check if the update was successful
    if result.matched_count > 0:
        print(f"Successfully updated document with mongo_id {game_db['_id']}")
    else:
        print(f"No document found with mongo_id {game_db['_id']}")
    #Get game obj
    game = gameObj(player, game_db=game_db)
    return game