from pymongo import database, MongoClient, collection
from bson.json_util import dumps
from flask import json


class MongoDBHandler:
    def __init__(self, database_name: str):
        self.mongo = MongoClient('mongodb+srv://admin:KpGbKaygcFlKoDRJ@facerecognition.3mbw1.mongodb.net/DB?retryWrites=true&w=majority',
                                 maxPoolSize=50, connect=False)
        self.db = database.Database(self.mongo, database_name)

    def truncate_collection(self, collection_name: str):
        self.get_collection(collection_name).delete_many({})

    def get_collection(self, collection_name: str):
        return collection.Collection(self.db, collection_name)

    def insert_one_to_collection(self, collection_name: str, data):
        self.get_collection(collection_name).insert_one(data)

    def scan_collection(self, collection_name: str):
        return json.loads(dumps(collection.Collection(self.db, collection_name).find()))

    def count_documents_in_collection(self, collection_name: str):
        return self.get_collection(collection_name).count_documents({})
