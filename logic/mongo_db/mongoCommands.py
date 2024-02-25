from pymongo import MongoClient
import yaml
import os

class dbObj:

    def __init__(self):
        config = self.getConfig()
        if os.getenv('IN_DOCKER') != 'YES':
            url = config['MONGO_DB']['URL']
            port = config['MONGO_DB']['PORT']
            username = config['MONGO_DB']['USERNAME']
            password = config['MONGO_DB']['PASSWORD']
            login_string = f'mongodb://{username}:{password}@{url}:{port}/'
        else:
            login_string = os.environ.get('MONGO_URI')
        #Get main client
        self.client = MongoClient(login_string)
        #Now get database and collection
        self.db = self.client[config['MONGO_DB']['DB']]
        self.collection = self.db[config['MONGO_DB']['COL']]

    def getConfig(self):
        with open("logic/mongo_db/mongo_config.yml", "r") as stream:
            try:
                config = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        return config
