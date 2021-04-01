import pymongo as pymongo
from bson import ObjectId


class DatabaseConnection:
    client = pymongo.MongoClient(
        "mongodb+srv://Hacking-Lab:IN4253ET@cluster0.yc2nt.mongodb.net/?retryWrites=true&w=majority")

    def __init__(self, database, collection):
        self.mydb = self.client[database]
        self.mycol = self.mydb[collection]

    def add_entry(self, json):
        object_id = str(ObjectId())
        json["_id"] = object_id
        self.mycol.insert_one(json)
        return object_id

    def delete_entry(self, json):
        self.mycol.delete_one(json)

    def update_entry(self, json, newval):
        self.mycol.update_one(json, newval)

    def find_entries(self, json):
        return self.mycol.find(json)

    def find_entry(self, json):
        """Select a single entry from the MongoDB collection that has the same values as the provided JSON."""
        return self.mycol.find_one(json)

    def find_entry_on_id(self, id):
        """Retrieve entry from the MongoDB collection based on it's unique ID."""
        return self.mycol.find_one(id)

    def get_random_entry(self):
        return self.mycol.aggregate([{"$sample": {"size": 1}}]).next()
