class gameObj:

    def __init__(self, player, game_db=None):
        if game_db is None:
            self.players = [player]
            self.game_state = 'initialised'
        else:
            self.players = game_db['players']
            self.game_state = game_db['game_state']
            self.game_id = game_db['_id']

    def toDict(self):
        """Convert obj to dict for loading to mongo db"""
        db_dict = {'players': self.players,
                   'game_state': self.game_state}
        return db_dict
    
    def getPlayers(self)
        pass

    def assignCharacters(self):
        pass
    
class playerObj:

    def __init__(self, player_name):
        self.player_name = player_name
        self.character = ''