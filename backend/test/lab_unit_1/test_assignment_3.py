# import unittest
# from unittest import TestCase, mock
# from unittest.mock import patch
# from src.util.dao import DAO

# class TestDAO(unittest.TestCase):

#     def setUp(self):
#         self.mock_client = mock.MagicMock()
#         self.mock_database = mock.MagicMock()
#         self.mock_collection = mock.MagicMock()
#         self.mock_client.__getitem__.return_value = self.mock_database
#         self.mock_database.__getitem__.return_value = self.mock_collection

#         self.patcher = mock.patch('pymongo.MongoClient', return_value=self.mock_client)
#         self.patcher.start()

#         # mock the open function to return a JSON object
#         self.mock_open = mock.mock_open(read_data='{"name": {"$type": "string"}}')
#         self.patcher_open = mock.patch('builtins.open', self.mock_open)
#         self.patcher_open.start()

#         self.dao = DAO('test_collection')

#     def tearDown(self):
#         self.patcher.stop()
#         self.patcher_open.stop()

#     def test_create(self):
#         # mock the insert_one method of the collection to return a test value
#         self.mock_collection.insert_one.return_value.inserted_id = 'test_id'

#         # create a test data dictionary
#         test_data = {
#             'name': 'Test task',
#             'completed': False
#         }

#         # call the create method of the DAO
#         result = self.dao.create(test_data)

#         # check that the result is as expected
#         self.assertEqual(result, {
#             '_id': 'test_id',
#             'name': 'Test task',
#             'completed': False
#         })
