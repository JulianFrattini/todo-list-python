import unittest
from src.util.dao import DAO
from src.util.validators import getValidator
import os
from pymongo import MongoClient
from pymongo.errors import OperationFailure
from bson import ObjectId
import json

class TestCreateMethod(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        mongo_url = os.getenv('MONGO_URL', 'mongodb://root:root@localhost:27017')
        try:
            cls.client = MongoClient(mongo_url)
            cls.db = cls.client['edutask']
            cls.dao = DAO(collection_name="video")
            cls.dao.collection = cls.db['video']
        except OperationFailure as e:
            print(f"Authentication failed: {e}")
            raise e

    @classmethod
    def tearDownClass(cls):
        cls.client.drop_database(cls.db.name)
        cls.client.close()

    def setUp(self):
        self.dao.collection.delete_many({})

    def test_create_compliant_data_insertion(self):
        compliant_data = {
            "url": "https://www.youtube.com/watch?v=1"
        }
        result = self.dao.create(compliant_data)
        self.assertIsNotNone(result)
        self.assertIn('_id', result)

        inserted_id = result['_id']
        if isinstance(inserted_id, dict) and '$oid' in inserted_id:
            inserted_id = ObjectId(inserted_id['$oid'])

        created_obj = self.dao.collection.find_one({'_id': inserted_id})
        self.assertEqual(created_obj['url'], compliant_data['url'])

    def test_create_compliant_data_find_one_call(self):
        compliant_data = {
            "url": "https://www.youtube.com/watch?v=1"
        }
        result = self.dao.create(compliant_data)

        inserted_id = result['_id']

        if isinstance(inserted_id, dict) and '$oid' in inserted_id:
            inserted_id = ObjectId(inserted_id['$oid'])

        created_obj = self.dao.collection.find_one({'_id': inserted_id})
        self.assertIsNotNone(created_obj)
        self.assertEqual(created_obj['url'], compliant_data['url'])

    def test_create_non_compliant_data(self):
        non_compliant_data = {
            "email": "test@gmail.com"
        }
        with self.assertRaises(Exception):
            self.dao.create(non_compliant_data)


    def test_getValidator_loads_validator_from_json(self):
        collection_name = "video"
        expected_file_path = f'./src/static/validators/{collection_name}.json'

        expected_validator = {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["url"],
                "properties": {
                    "url": {
                        "bsonType": "string",
                        "description": "the url of a YouTube video must be determined"
                    }
                }
            }
        }

        validator = getValidator(collection_name)

        self.assertEqual(validator, expected_validator)

        with open(expected_file_path, 'r') as f:
            file_contents = json.load(f)
        self.assertEqual(validator, file_contents)


if __name__ == '__main__':
    unittest.main()
