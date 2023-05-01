# coding=utf-8
import os

import pymongo
from dotenv import dotenv_values

# create a data access object
from src.util.validators import getValidator

import json
from bson import json_util
from bson.objectid import ObjectId


class DAO:

    def __init__(self, collection_name: str):
        """Establish a data access object to a collection of the given name in the MongoDB database as specified in the environment variables. When the collection is first creted, it will be associated to a validator (see https://www.mongodb.com/docs/manual/core/schema-validation/) to ensure some basic data compliance.

        parameters:
            collection_name -- the name of the collection (a collection validator of the same name must be available)
        """

        # load the local mongo URL (something like mongodb://localhost:27017)
        LOCAL_MONGO_URL = dotenv_values('.env').get('MONGO_URL')
        # check out of the environment (which can be overridden by the docker-compose file) also specifies an URL, and use that instead if it exists
        MONGO_URL = os.environ.get('MONGO_URL', LOCAL_MONGO_URL)

        # connect to the MongoDB and select the appropriate database
        print(
            f'Connecting to collection {collection_name} on MongoDB at url {MONGO_URL}')
        client = pymongo.MongoClient(MONGO_URL)
        database = client.edutask

        # create the collection if it does not yet exist
        if collection_name not in database.list_collection_names():
            validator = getValidator(collection_name)
            database.create_collection(collection_name, validator=validator)

        self.collection = database[collection_name]

    def create(self, data: dict):
        """Creates a new document in the collection associated to this data access object. The creation of a new document must comply to the corresponding validator, which defines the data structure of the collection. In particular, the validator has to make sure that: (1) the data for the new object contains all required properties, (2) every property complies to the bson data type constraint (see https://www.mongodb.com/docs/manual/reference/bson-types/, though we currently only consider Strings and Booleans), (3) and the values of a property flagged with 'uniqueItems' are unique among all documents of the collection.

        parameters:
            data -- a dict containing key-value pairs compliant to the validator

        returns:
            object -- the newly created MongoDB document (parsed to a JSON object) containing the input data and an _id attribute

        raises:
            WriteError - in case at least one of the validator criteria is violated
        """
        localdata = dict(data)

        try:
            # insert the object into the database
            inserted_id = self.collection.insert_one(localdata).inserted_id

            # fetch and return the created object
            obj = self.collection.find_one({'_id': inserted_id})
            return self.to_json(obj)
        except Exception as e:
            raise

    def findOne(self, id: str):
        """Find one specific object in the collection with the _id property equal to the given id.

        parameters: 
            id -- id value of the requested object

        returns:
            object -- MongoDB document (parsed to json object)

        raises:
            Exception -- in case any database operation fails
        """
        try:
            obj = self.collection.find_one({'_id': ObjectId(id)})
            return self.to_json(obj)
        except Exception as e:
            raise

    # find all objects that comply to the optional filter
    def find(self, filter=None, toid: list = None):
        """Find all objects contained in the collection which comply to the given filter. 

        parameters: 
            filter -- dict containing key value pairs of properties and applicable filters
            toid -- list of properties (contained in the filter) which are MongoDB ObjectIDs and hence need to be converted

        returns:
            [object] -- list of objects compliant to the given filter

        raises:
            Exception -- in case any database operation fails
        """

        # if the filter contains attributes that are IDs, then they need to be converted
        if toid and len(toid) > 0:
            for i in toid:
                converted = []
                for element in filter[i]:
                    conv = ObjectId(element['$oid'])
                    converted.append(conv)
                filter[i] = {'$in': converted}

        objs = []
        try:
            dbobjs = self.collection.find(filter)

            for obj in dbobjs:
                objs.append(self.to_json(obj))

            return objs
        except Exception as e:
            raise

    def update(self, id: str, update_data: dict):
        """Find one specific object in the collection with the _id property equal to the given id and update its data according to the update_data.

        parameters: 
            id -- id value of the requested object
            update_data -- dict containing the update operation (top-level key values must be valid MongoDB update operators, see https://www.mongodb.com/docs/manual/reference/operator/update/#std-label-update-operators)

        returns:
            True -- if the update was successful
            False -- otherwise

        raises:
            Exception -- in case any database operation fails
        """
        try:
            update_result = self.collection.update_one(
                {'_id': ObjectId(id)},
                update_data
            )
            return update_result.acknowledged
        except Exception as e:
            raise

    def delete(self, id: str):
        """Find one specific object in the collection with the _id property equal to the given id and remove it from the collection

        parameters: 
            id -- id value of the requested object

        returns:
            True -- if the deletion was successful
            False -- otherwise

        raises:
            Exception -- in case any database operation fails
        """
        try:
            result = self.collection.delete_one(
                {'_id': ObjectId(id)}
            )
            return result.acknowledged
        except Exception as e:
            raise

    def drop(self):
        """Remove the entire collection

        raises:
            Exception -- in case any database operation fails
        """
        try:
            self.collection.drop()
        except Exception as e:
            raise

    def to_json(self, data):
        """Transform a MongoDB document into a json object.

        paramenters: 
            data -- the MongoDB document

        returns:
            dict -- the document converted to JSON
        """
        return json.loads(json_util.dumps(data))
