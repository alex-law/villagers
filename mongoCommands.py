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
        #Get max todo num
        try:
            self.max_todo = self.collection.find_one(sort=[("id", -1)])['id']
        except TypeError:
            self.max_todo = '1'


    def getToDo(self):
        """Get current list of todos"""
        cursor = self.collection.find({})
        todo_list = []
        for document in cursor:
            document['complete'] = bool(int(document['complete']))
            todo_list.append(dotdict(document))
        return todo_list
    
    def addToDo(self, new_todo_dict):
        """Add a new to do item to mongodb"""
        new_todo_dict['id'] = self.max_todo
        self.max_todo = str(int(self.max_todo) + 1)
        self.collection.insert_one(new_todo_dict)