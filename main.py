from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from logic.mongo_db.mongoCommands import dbObj
from bson import ObjectId
import threading
import time
from flask_socketio import SocketIO

from logic.settup.initialise import getConfig
from logic.settup.start_game import (getUserInput, validateInput, startNewGame,
                              checkExistingPlayer, startExistingGame)
from logic import game_logic, player_logic

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)

config = getConfig()
db = dbObj(config)


@app.get("/")
def home():
    return render_template("home.html", valid='')

def checkVotes(_id, player_name):
    while True:
        game = db.collection.find_one({'_id': _id})
        other_players = [p for p in game['players'] if p['player_name'] != player_name]
        voted_players = [p for p in other_players if p['vote'] != '']
        if len(voted_players) > 0:
            socketio.emit('update_ui', {'borderColor': 'red'})
            return
        time.sleep(2)
        


@app.route('/update_game', methods=['POST'])
def update_game():
    if request.is_json:
        data = request.get_json()
        vote = data.get('vote')
        # Process the game_id as needed...
        return jsonify({"success": True, "message": "Game info updated with vote: " + vote})
    else:
        return jsonify({"success": False, "message": "Request body must be JSON."}), 400

@app.get("/play")
def play():
    _id = ObjectId(session.get('_id', None))
    player_name = session.get('player_name', None)
    game = db.collection.find_one({'_id': _id})
    game['players'] = player_logic.assignCharacters(game['players'])
    players = game['players']
    player = [p for p in players if p['player_name'] == player_name]
    if len(player) > 1:
        raise Exception('Multiple players in game with same name')
    player = player[0]
    game['status'] = 'In Progress'
    db.collection.replace_one({'_id': _id}, game)

    thread = threading.Thread(target=checkVotes, args=(_id, player_name))
    thread.start()

    return render_template("village.html", game=game, player=player, players=players)

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

if __name__ == '__main__':
    socketio.run(app, debug=True)