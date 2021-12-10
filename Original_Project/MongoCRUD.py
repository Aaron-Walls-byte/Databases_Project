from pymongo import MongoClient
class MongoCRUD(object):

#Initialize contection with the MongoDB
    def __init__(self, username="shipUser", password="password"):
        # Initializing the MongoClient. This helps to
        # access the MongoDB databases and collections.
        if username and password:
            self.client = MongoClient('mongodb://%s:%s@localhost:27017/ms4' % (username, password))
        else:
            self.client = MongoClient('mongodb://localhost:27017')
        self.database = self.client['ms4']


# Complete this create method to implement the C in CRUD.
    def create(self, data):
        if data is not None:
            insert = self.database.shipwrecks.insert(data)  # data should be dictionary
            if insert!=0:
                return True
            else:
                return False
        else:
            raise Exception("Nothing to save, because data parameter is empty")


# Create method to implement the R in CRUD.
    def read(self,criteria=None):

        # will return all rows which matches the criteria
        if criteria:
            data = self.database.shipwrecks.find(criteria,{"_id":False}) #omit id
        else:
            data = self.database.shipwrecks.find( {} , {"_id":False})

        return data


# Update method to implement the U in CRUD
    def update(self, criteria, updateValue):
        self.database.shipwrecks.update_one(criteria, updateValue)


# Delete method to implement the D in Crud
    def delete(self, criteria):
        result = self.database.shipwrecks.delete_one(criteria)
