import pymongo as pymongo

client = pymongo.MongoClient(
    "mongodb+srv://Hacking-Lab:IN4253ET@cluster0.yc2nt.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
mydb = client["myFirstDatabase"]
mycol = mydb["profiles"]


def add_profile(json):
    mycol.insert_one(json)


def delete_profile(json):
    mycol.delete_one(json)


def update_profile(json, newval):
    mycol.update_one(json, newval)


def query_profile(json):
    return mycol.find(json)


def find_profile(json):
    return mycol.find_one(json)
