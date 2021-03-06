from pymongo import MongoClient

client = MongoClient(host=['co_repo:27017'], username="root", password="root123")

db = client.co_db