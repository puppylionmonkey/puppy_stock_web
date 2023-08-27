from pymongo import MongoClient


class FinancialSystemModel:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["user_db"]
        self.user_balance_collection = self.db["user_balance"]

    def get_balance(self):
        user_balance_dict = self.user_balance_collection.find_one({"username": self.username})
        return user_balance_dict['balance']

    def update_balance(self, username, add_balance):
        balance = self.get_balance()
        new_balance = balance + add_balance
        self.user_balance_collection.update_one(
            {"username": username},
            {"$set": {"balance": new_balance}}
        )

    @staticmethod
    def get_fee(quantity, price):
        return quantity * price * 0.1425 / 100 * 0.28

    @staticmethod
    def get_tax(quantity, price):
        return quantity * price * 0.3 / 100
