from flask import Flask, render_template, request, redirect, url_for
from settup import getConfig
from mongoCommands import dbObj
from villageObjects import gameObj, playerObj

app = Flask(__name__)

config = getConfig()
db = dbObj(config)


@app.get("/")
def home():
    return render_template("home.html", valid='')

@app.get("/game")
def game():
    return render_template("game.html")

@app.post("/newGame")
def newGame():
    #If no player name return tell user
    player_name = request.form.get("player_name")
    if len(player_name.strip()) == 0:
        # return redirect(url_for("home"), valid='Please enter a user name')
        return render_template("home.html", valid= 'Please enter a user name')
    #If no game id but new game not tell user
    game_id = request.form.get("game_id")
    new_game = request.form.get("new_game")
    if (len(game_id.strip()) == 0 and new_game is None):
        return render_template("home.html", valid= 'Please select new game or enter a game id')
    #If game id already exists and user is trying to start a new game
    if (db.collection.find_one({'game_id': game_id}) is not None) and (new_game is not None):
        return render_template("home.html", valid='Game id is currently in use, please choose a new id')
    #If game id does not exist and user is trying to join game
    if (db.collection.find_one({'game_id': game_id}) is None) and (new_game is None):
        return render_template("home.html", valid='Game id does not exist, please check your game id or request a new one')
    #Made it past all this so initiate player
    player = playerObj(player_name)
    #Start a new game
    if new_game is not None:
        #Initiate game obj
        game = gameObj(player, init_game_id=game_id)
        #save game to db
        game.mongo_id = db.collection.insert_one(game.gameToDict()).inserted_id
        return render_template('lobby.html', game=game)
    #Otherwise get current game
    if new_game is None:
        #Get existing game
        game_db = db.collection.find_one({'game_id': game_id})
        #Check to make sure that player doesn't already exist
        curr_players = game_db['players']
        if player.player_name in [p['player_name'] for p in curr_players]:
            return render_template("home.html", valid='Player name already taken, please pick a new one')
        #Add new player
        curr_players.append(player.toDict())
        filter = {'_id': game_db['_id']}
        update_fields = {'$set': {'players': curr_players}}
        # Update the document
        result = db.collection.update_one(filter, update_fields, upsert=False)

        #Get game obj
        game = gameObj(player, game_db=game_db)
        #Update game dictionary
        return render_template('lobby.html', game=game)

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
