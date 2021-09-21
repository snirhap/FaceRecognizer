from pymongo import MongoClient, database, collection
import os

MONGO_CONNECTION_STRING_PARAMETER = 'MONGO_CONNECTION_STRING'


class MongoDBHandler:
    def __init__(self, database_name: str):
        self.mongo = MongoClient(os.getenv(MONGO_CONNECTION_STRING_PARAMETER), maxPoolSize=50)
        self.db = database.Database(self.mongo, database_name)

    def get_collection(self, collection_name: str):
        return collection.Collection(self.db, collection_name)

    def insert_one_to_collection(self, collection_name: str, data: dict):
        self.get_collection(collection_name).insert_one(data)

    def find_in_collection(self, collection_name: str, filter_dict: dict = None):
        if not filter_dict:
            filter_dict = {}
        return self.get_collection(collection_name).find(filter_dict)

    def count_documents_in_collection(self, collection_name: str, filter_dict: dict = None):
        if not filter_dict:
            filter_dict = {}
        return self.get_collection(collection_name).count_documents(filter_dict)

    def truncate_collection(self, collection_name: str):
        self.get_collection(collection_name).delete_many({})
