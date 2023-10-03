from pymongo import MongoClient
from bson.objectid import ObjectId
import logging

###########################
#Configuring Logging Feature
###########################

logging.basicConfig(
    filename='AnimalShelter_CRUD.log',  # Specify the log file name
    level=logging.INFO,  # Set the logging level to INFO (you can change it)
    format='%(asctime)s - %(levelname)s - %(message)s'  # Define log message format
)


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
            try:
                insert = self.database.animals.insert(data)  # data should be dictionary
                if insert != 0:
                    logging.info("Record created successfully")
                    return True
                else:
                    logging.error("Failed to create record")
                    return False
            except Exception as e:
                logging.error(f"Error while creating record: {str(e)}")
                return False
        else:
            logging.error("Nothing to save, data parameter is empty")
            raise Exception("Nothing to save, data parameter is empty")

    # Create method to implement the R in CRUD.
    def read(self, criteria=None):

        try:
            # If criteria is not None then this find will return all rows which match the criteria
            if criteria:
                # {'_id': False} omits the unique ID of each row
                data = self.database.animals.find(criteria, {"_id": False})
            else:
                # If there is no search criteria then all the rows will be returned
                data = self.database.animals.find({}, {"_id": False})
            assert isinstance(data, object)
            logging.info("Records read successfully")
            return data
        except Exception as e:
            logging.error(f"Error while reading records: {str(e)}")
            return None

    # Create method to implement the U in CRUD
    def update(self, data, newvals):
        try:
            if data is not None:
                update_result = self.database.animals.update(data, newvals)
                if update_result.get("updatedExisting", False):
                    logging.info("Record updated successfully")
                    return True
                else:
                    logging.error("Failed to update record")
                    return False
            else:
                logging.error("Update unsuccessful. Data parameter is empty.")
                return False
        except Exception as e:
            logging.error(f"Error while updating record: {str(e)}")
            return False

    # Create method to implement the D in CRUD
    def delete(self, data):
        try:
            if data is not None:
                self.database.animals.remove(data)
                logging.info("Record deleted successfully")
                return True
            else:
                logging.error("Delete unsuccessful. Data parameter is empty.")
                return False
        except Exception as e:
            logging.error(f"Error while deleting record: {str(e)}")
            return False
        