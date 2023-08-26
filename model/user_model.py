from pymongo import MongoClient


class User:
    def __init__(self, username):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["user_db"]
        self.user_balance_collection = self.db["user_balance"]

        self.username = username
        self.initial_balance = self.get_balance()

    def get_balance(self):
        user_balance_dict = self.user_balance_collection.find_one({"username": self.username})
        return user_balance_dict['balance']
