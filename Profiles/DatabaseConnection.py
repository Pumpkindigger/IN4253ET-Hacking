import pymongo as pymongo
from bson import ObjectId


# mydb = client["myFirstDatabase"]
# mycol = mydb["profiles"]


class DatabaseConnection:
    client = pymongo.MongoClient(
        "mongodb+srv://Hacking-Lab:IN4253ET@cluster0.yc2nt.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

    def __init__(self, database, collection):
        self.mydb = self.client[database]
        self.mycol = self.mydb[collection]

    def add_profile(self, json):
        json["_id"] = str(ObjectId())
        self.mycol.insert_one(json)

    def delete_profile(self, json):
        self.mycol.delete_one(json)

    def update_profile(self, json, newval):
        self.mycol.update_one(json, newval)

    def query_profile(self, json):
        return self.mycol.find(json)

    def find_profile(self, json):
        return self.mycol.find_one(json)

    def find_profile_on_id(self, id):
        return self.mycol.find_one(id)

    def find_profiles_on_message(self, device):
        '''
        Given the welcome message, return a list of profiles
        '''
        profiles = []
        for profile in self.mycol.find({"Welcome": device}):
            profiles.append(profile)
        return profiles

    def get_random_profile(self):
        return self.mycol.aggregate([{"$sample": {"size":1}}]).next()