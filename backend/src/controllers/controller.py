from  src.util.dao import DAO

class Controller:
    def __init__(self, dao: DAO):
        """Instantiate a controller, which acts as a mediator between the data access object and the blueprints.
        The main purpose of a controller is to abstract the data access from the blueprint routes, such that they can be
        executed outside of server operations.

        parameters:
            dao -- data access object, which has to grant access to the specific collection of the database
        """
        self.dao = dao

    def create(self, data: dict):
        """Create a new object in the database and return the newly created object. The database object will contain
        a unique id, which is accessible at ob['_id']['$oid] in the jsonified form.

        parameters:
            data -- a dict containing all relevant fields of data according to the validator

        raises:
            Exception -- in case the database operation fails, raise an exception
        """
        try:
            return self.dao.create(data)
        except Exception as e:
            raise

    # get a user by id
    def get(self, id: str):
        """Search for an object by id and return the associated database object. The database object will contain
        a unique id, which is accessible at ob['_id']['$oid] in the jsonified form.

        parameters:
            id -- the unique identifier of the object

        returns:
            user -- if an object associated to the given id can be found
            None -- if no object associated to the given id can be found

        raises:
            Exception -- in case the database operation fails, raise an exception
        """
        try:
            return self.dao.findOne(id)
        except Exception as e:
            raise

    def get_all(self):
        """Gathers all object in the respective collection of the database. The database object will contain
        a unique id, which is accessible at ob['_id']['$oid] in the jsonified form.
        
        returns:
            users -- array of all objects in the respective collection in the database

        raises:
            Exception -- in case the database operation fails, raise an exception
        """
        try:
            return self.dao.find()
        except Exception as e:
            raise

    def update(self, id: str, data: dict):
        """Locates an object in the respective collection of the database and updates it with the given data 
        values.

        parameters:
            id -- the unique identifier of the object
            data -- a dict where the top level keys are valid MongoDB update operators (e.g., $set, $push), 
                and the values of those keys again dicts where the keys are fieldnames and the values the new values.

        returns: 
            True -- if the update was successful
            False -- if the update failed
            
        raises:
            Exception -- in case the database operation fails, raise an exception
        """
        try:
            update_result = self.dao.update(id=id, update_data=data)
            return update_result
        except Exception as e:
            raise

    def delete(self, id: str):
        """Delete an object from the respective collection of the database

        parameters:
            id -- the unique identifier of the object

        returns: 
            True -- if the delete was successful
            False -- if the delete failed
            
        raises:
            Exception -- in case the database operation fails, raise an exception
        """
        try:
            result = self.dao.delete(id=id)
            return result
        except Exception as e:
            raise