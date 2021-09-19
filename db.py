import pymongo
from bson.json_util import dumps
from flask import json


class MongoDBHandler:
    def __init__(self, database_name: str):
        self.mongo = pymongo.MongoClient('mongodb+srv://admin:KpGbKaygcFlKoDRJ@facerecognition.3mbw1.mongodb.net/DB?retryWrites=true&w=majority',
                                         maxPoolSize=50, connect=False)
        self.db = pymongo.database.Database(self.mongo, database_name)

    def truncate_collection(self, collection):
        self.get_collection(collection).delete_many({})

    def get_collection(self, collection):
        return pymongo.collection.Collection(self.db, collection)

    def insert_one_to_collection(self, collection, data):
        self.get_collection(collection).insert_one(data)

    def scan_collection(self, collection):
        return json.loads(dumps(pymongo.collection.Collection(self.db, collection).find()))

    def count_documents_in_collection(self, collection: str):
        return self.get_collection(collection).count_documents({})
