from pymongo import MongoClient

def connect_mongodb():
    client = MongoClient("mongodb://localhost:27017/")
    mydb = client["user"]
    return mydb