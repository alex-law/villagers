import yaml
from pymongo import MongoClient
import urllib.parse

def getConfig():
    with open("config.yml", "r") as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return config

def pyMongoConnect(config):
    url = config['MONGO_DB']['URL']
    port = config['MONGO_DB']['PORT']
    username = config['MONGO_DB']['USERNAME']
    password = config['MONGO_DB']['PASSWORD']
    login_string = f'mongodb://{username}:{password}@{url}:{port}/'
    # db_client = MongoClient('localhost', 27017)
    db_client = MongoClient(login_string)
    return db_client

    db_client = MongoClient(f'mongodb://{username}:{password}@{url}' % (username, password), port = int(port))
    return db_client
