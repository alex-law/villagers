class gameObj:

    def __init__(self, player, init_game_id='', game_db=None):
        if game_db is None:
            self.players = [player]
            self.game_state = 'initialised'
            self.game_id = init_game_id
        else:
            self.players = game_db['players']
            self.game_state = game_db['game_state']
            self.game_id = game_db['game_id']

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

    def __init__(self, player_name):
        self.player_name = player_name
        self.character = ''

    def toDict(self):
        """Convert obj to dict for loading to mongo db"""
        player_dict = {'player_name': self.player_name,
                   'character': self.character}
        return player_dict