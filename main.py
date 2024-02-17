from flask import Flask, render_template, request, redirect, url_for, session
from mongoCommands import dbObj
from bson import ObjectId
from villageObjects import gameObj, playerObj

from settup import getConfig
from logic.start_game import (getUserInput, validateInput, startNewGame,
                              checkExistingPlayer, startExistingGame)

app = Flask(__name__)
app.secret_key = 'your_secret_key'

config = getConfig()
db = dbObj(config)


@app.get("/")
def home():
    return render_template("home.html", valid='')

@app.get("/game")
def game():
    return render_template("game.html")

@app.get("/play")
def play():
    _id = ObjectId(session.get('_id', None))
    player_name = session.get('player_name', None)
    game_db = db.collection.find_one({'_id': _id})
    game = gameObj(game_db=game_db)
    player = [p for p in game.players if p.player_name == player_name]
    
    print('hold')

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
    player = playerObj(player_name)
    #Start a new game
    if new_game:
        game = startNewGame(player, game_id, db)
        # Save mongo db id and player name to session so we can access later
        session['_id'] = str(game._id)
        session['player_name'] = player.player_name
        return render_template('lobby.html', game=game_db)
    #Else get current game
    else:
        #Get existing game dict from db
        game_db = db.collection.find_one({'game_id': game_id})
        #Specified user name might already be taken
        success, message = checkExistingPlayer(player, game_db)
        if not success:
            return render_template("home.html", valid=message)        
        #Update game db with new user and get updated game obj
        game = startExistingGame(player, game_db, db)
        # Save mongo db id and player name to session so we can access later
        session['_id'] = str(game._id)
        session['player_name'] = player.player_name
        return render_template('lobby.html', game=game_db)

@app.get("/update/<int:todo_id>")
def update(todo_id):
    todo = db.collection.find_one({'id': str(todo_id)})
    todo['complete'] = not todo['complete']
    db.collection.update_one({'id':str(todo_id)}, {"$set": todo}, upsert=False)
    return redirect(url_for("home"))


@app.get("/delete/<int:todo_id>")
def delete(todo_id):
    db.collection.delete_one({'id': str(todo_id)})
    return redirect(url_for("home"))
