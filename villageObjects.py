class gameObj:

    def __init__(self, init_game_id='', player=None, game_db=None):
        """If a init_game_id is provided then assume that this is a new game,
        so need a player object and don't use game_db to create object
        Else assume existing game and use game_db to get all game and player info"""
        if game_db is None:
            self.players = [player]
            self.game_state = 'initialised'
            self.game_id = init_game_id
        else:
            self.players = [playerObj(p['player_name'], p['character']) for p in game_db['players']]
            self.game_state = game_db['game_state']
            self.game_id = game_db['game_id']
            self._id = game_db['_id']

    def gameToDict(self):
        """Convert obj to dict for loading to mongo db"""
        db_dict = {'players': self.playersToList(),
                   'game_state': self.game_state,
                   'game_id': self.game_id}
        return db_dict
    
    def playersToList(self):
        """Convert obj to dict for loading to mongo db"""
        players_list = [p.toDict() for p in self.players]
        return players_list
    
    def getPlayers(self):
        pass

    def assignCharacters(self):
        pass
    
class playerObj:

    def __init__(self, player_name, character=''):
        self.player_name = player_name
        self.character = character

    def toDict(self):
        """Convert obj to dict for loading to mongo db"""
        player_dict = {'player_name': self.player_name,
                   'character': self.character}
        return player_dict