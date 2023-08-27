# 在名為order_model.py的文件中

from pymongo import MongoClient
from model.get_now_price_model import GetRealtimeStockPrice


class OrderModel:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["user_db"]
        self.orders_collection = self.db["stock_inventory"]
        self.get_realtime_stock_price = GetRealtimeStockPrice()

    def get_user_inventory(self, username):
        return list(self.orders_collection.find({"username": username}))


