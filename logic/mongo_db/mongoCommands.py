from pymongo import MongoClient

class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

class dbObj:

    def __init__(self, config):
        url = config['MONGO_DB']['URL']
        port = config['MONGO_DB']['PORT']
        username = config['MONGO_DB']['USERNAME']
        password = config['MONGO_DB']['PASSWORD']
        login_string = f'mongodb://{username}:{password}@{url}:{port}/'
        #Get main client
        self.client = MongoClient(login_string)
        #Now get database and collection
        self.db = self.client[config['MONGO_DB']['DB']]
        self.collection = self.db[config['MONGO_DB']['COL']]

class player:

    def __init__(self, player_name):
        self.player_name = player_name
        