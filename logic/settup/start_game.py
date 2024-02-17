from flask import request
from logic import game_logic

def getUserInput():
    player_name = request.form.get("player_name")
    game_id = request.form.get("game_id")
    new_game = request.form.get("new_game")
    # Convert to bool for clarity
    new_game = True if new_game else False
    return player_name, game_id, new_game

def validateInput(player_name, game_id, new_game, db):
    #If no player name return tell user
    if len(player_name.strip()) == 0:
        return False, 'Please enter a user name'
    if (len(game_id.strip()) == 0 and not new_game):
        return False, 'Please select new game or enter a game id'
    #If game id already exists and user is trying to start a new game
    if (db.collection.find_one({'game_id': game_id}) is not None) and new_game:
        return False, 'Game id is currently in use, please choose a new id'
    #If game id does not exist and user is trying to join game
    if (db.collection.find_one({'game_id': game_id}) is None) and not new_game:
        return False, 'Game id does not exist, please check your game id or request a new one'
    #If passed all these now return true and no failure message
    return True, ''
    
def startNewGame(player, game_id, db):
    #Initiate game obj
    game = game_logic.initialiseDict(game_id, player)
    #save game to db
    game['_id'] = db.collection.insert_one(game).inserted_id
    return game

def checkExistingPlayer(player, game):
    #Check to make sure that player doesn't already exist
    curr_players = game['players']
    if player['player_name'] in [p['player_name'] for p in curr_players]:
        return False, 'Player name already taken, please pick a new one'
    else:
        return True, ''

def startExistingGame(player, game, db):
    #Add new player
    game['players'].append(player)
    filter = {'_id': game['_id']}
    update_fields = {'$set': {'players': game['players']}}
    # Update the document
    result = db.collection.update_one(filter, update_fields, upsert=False)
    # Check if the update was successful
    if result.matched_count > 0:
        print(f"Successfully updated document with _id {game['_id']}")
    else:
        print(f"No document found with _id {game['_id']}")
    return game