from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from logic.mongo_db.mongoCommands import dbObj
from bson import ObjectId
import os
import sys
import logging
import threading
import time
from flask_socketio import SocketIO, emit

from logic.settup.start_game import (getUserInput, validateInput, startNewGame,
                              checkExistingPlayer, startExistingGame)
from logic import game_logic, player_logic

handler = logging.StreamHandler(sys.stderr)
handler.setLevel(logging.INFO)
logging.getLogger().addHandler(handler)
logging.getLogger().setLevel(logging.INFO)

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SECRET_KEY'] = 'secret'
app.config['APPLICATION_ROOT'] = './'
app.config['PREFERRED_URL_SCHEME'] = 'http'

app.logger.handlers = logging.getLogger().handlers
app.logger.setLevel(logging.INFO)

socketio = SocketIO(app)#, logger=True, engineio_logger=True)

db = dbObj()

@app.get("/")
def home():
    return render_template("home.html", valid='')


def checkVotes(_id, player_name):
    #Give webpage time to load and villagers to vote before starting to count
    time.sleep(3)
    while True:
        game = db.collection.find_one({'_id': _id})

        player, alive_players, alive_villagers, dead_players = player_logic.getPlayersLists(game['players'], player_name)
        voted_alive_players = [p for p in alive_players if p['vote'] != '']

        if game['stage'] == 'day':
            if len(voted_alive_players) > 0:
                for voted_player in voted_alive_players:
                    socketio.emit('update_player_vote', {'voted_player': voted_player['player_name']})
        #Once all players have voted, then ready to move onto next round
        # Wait for all players to vote if playing during day
        # Wait for all wolfs to vote if playing during night
        if game['stage'] == 'day':
            expected_votes = len(alive_players)
        else:
            alive_wolfs = [p for p in alive_players if p['character'] == 'wolf']
            expected_votes = len(alive_wolfs)
        
        if len(voted_alive_players) == expected_votes:
            game = game_logic.endOfPlay(game, db, _id)
            player, alive_players, alive_villagers, dead_players = player_logic.getPlayersLists(game['players'], player_name)
            with app.app_context():
                rendered_template = render_template("village.html", game=game, curr_player=player, alive_players=alive_players, alive_villagers=alive_villagers, dead_players=dead_players)
            socketio.emit('update_village', {'html': rendered_template})
        time.sleep(1)


@socketio.on('castVote')
def castVote(vote_data):
    vote = vote_data['vote']
    game, _id = game_logic.getGameFromSession(session, db)
    players, player_name = player_logic.getPlayersFromSession(session, game)
    voted_player = players[player_name]
    voted_player['vote'] = vote
    result = player_logic.updateMongoPlayer(game, voted_player, db)
    emit('voteResponse', {'success': True, 'voted_player': vote})


@app.get("/firstPlay")
def firstPlay():
    
    game, _id = game_logic.getGameFromSession(session, db)
    players, player_name = player_logic.getPlayersFromSession(session, game)
    players = player_logic.assignCharacters(players)
    game['players'] = players

    player, alive_players, alive_villagers, dead_players = player_logic.getPlayersLists(players, player_name)

    game['status'] = 'In Progress'
    game_logic.replaceGame(game, db, _id)
    thread = threading.Thread(target=checkVotes, args=(_id, player_name))
    thread.start()
    return render_template("village.html", game=game, curr_player=player, alive_players=alive_players, alive_villagers=alive_villagers, dead_players=dead_players)


@app.post("/newGame")
def newGame():
    """This is the landing page for starting a new game"""
    # Get input details from player
    player_name, game_id, new_game = getUserInput()
    # Check to make sure user inputs are all valid, if not alert user
    success, message = validateInput(player_name, game_id, new_game, db)
    if not success:
        return render_template("home.html", valid=message)
    #Made it past all this so initiate player obj
    player = player_logic.initialiseDict(player_name)
    #Start a new game
    if new_game:
        game = startNewGame(player, game_id, db)
        # Save mongo db id and player name to session so we can access later
        session['_id'] = str(game['_id'])
        session['player_name'] = player['player_name']
        return render_template('lobby.html', game=game)
    #Else get current game
    else:
        #Get existing game dict from db
        game = db.collection.find_one({'game_id': game_id})
        #Specified user name might already be taken
        success, message = checkExistingPlayer(player, game)
        if not success:
            return render_template("home.html", valid=message)        
        #Update game db with new user and get updated game obj
        game = startExistingGame(player, game, db)
        # Save mongo db id and player name to session so we can access later
        session['_id'] = str(game['_id'])
        session['player_name'] = player['player_name']
        return render_template('lobby.html', game=game)
    
    # game = db.collection.find_one({'game_id': '123'})
    # session['_id'] = str(game['_id'])
    # session['player_name'] = 'craig'
    # return render_template('lobby.html', game=game)

print('above name = main', flush=True)


if __name__ == '__main__':
    print('in name = main', flush=True)
    if os.getenv('IN_DOCKER') != 'YES':
        logging.info('LOGGING: Running in debug mode')
        print('PRINT: Running in debug mode')
        print('PRINT FLUSH: Running in debug mode', flush=True)
        app.logger.info('APP LOGGER: Running in debug mode')
        socketio.run(app, debug=True)
else:
    logging.info('LOGGING: Running in prod mode')
#     print('PRINT: Running in prod mode')
#     app.logger.info('APP LOGGER: Running in prod mode')
#     print('PRINT FLUSH: Running in prod mode', flush=True)
#     # socketio.run(app, debug=False, host='0.0.0.0', port=5000)
#     gunicorn_app = socketio()