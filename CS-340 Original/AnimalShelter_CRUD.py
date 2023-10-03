from pymongo import MongoClient
from bson.objectid import ObjectId


class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self, aacuser, admin):
        # Initializing the MongoClient. This helps to 
        # access the MongoDB databases and collections. 
        self.client = MongoClient('mongodb://%s:%s@localhost:46703/AAC' % (aacuser, admin))
        self.database = self.client['AAC']

    # Complete this create method to implement the C in CRUD.
    def create(self, data):
        if data is not None:
            insert = self.database.animals.insert(data)  # data should be dictionary
            if insert != 0:
                return True
            else:
                return False
        else:
            raise Exception("Nothing to save, data parameter is empty")

    # Create method to implement the R in CRUD.
    def read(self, criteria=None):

        # If criteria is not None then this find will return all rows which matches the criteria
        if criteria:
            # {'_id':False} just omits the unique ID of each row        

            data = self.database.animals.find(criteria, {"_id": False})
        else:
            # If there is no search criteria then all the rows will be return
            data = self.database.animals.find({}, {"_id": False})

        assert isinstance(data, object)
        return data

    # Create method to implement the U in CRUD
    def update(self, data, newvals): 
        if data is not None:
            return self.database.animals.update(data, newvals)
        else:
            print('Update unsuccessful.')
            return False


    # Create method to implement the D in CRUD
    def delete(self, data):
        if data is not None:
            self.database.animals.remove(data)
            return True
        else:
            return False
        