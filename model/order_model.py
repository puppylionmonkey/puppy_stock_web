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

    def buy_stock(self, username, stock_symbol, quantity, price):
        existing_order = self.orders_collection.find_one({"stock_symbol": stock_symbol, "username": username})
        if existing_order:  # 有庫存
            new_quantity = existing_order["quantity"] + quantity
            if new_quantity == 0:
                self.orders_collection.delete_one({"stock_symbol": stock_symbol, "username": username})
            else:
                new_total_price = existing_order["total_price"] + price * quantity
                self.orders_collection.update_one(
                    {"stock_symbol": stock_symbol, "username": username},
                    {"$set": {"quantity": new_quantity, "total_price": new_total_price}}
                )
        else:  # 沒庫存
            order = {
                "username": username,
                "stock_symbol": stock_symbol,
                "quantity": quantity,
                "total_price": price * quantity
            }
            self.orders_collection.insert_one(order)

    def sell_stock(self, username, stock_symbol, quantity, price):
        existing_order = self.orders_collection.find_one({"stock_symbol": stock_symbol, "username": username})
        if existing_order:  # 有庫存
            new_quantity = existing_order["quantity"] - quantity
            if new_quantity == 0:
                self.orders_collection.delete_one({"stock_symbol": stock_symbol, "username": username})
            else:
                new_total_price = existing_order["total_price"] - price * quantity
                self.orders_collection.update_one(
                    {"stock_symbol": stock_symbol, "username": username},
                    {"$set": {"quantity": new_quantity, "total_price": new_total_price}}
                )
        else:  # 沒庫存
            order = {
                "username": username,
                "stock_symbol": stock_symbol,
                "quantity": -quantity,
                "total_price": price * -quantity
            }
            self.orders_collection.insert_one(order)

    def get_fee(self, quantity, price):
        return quantity * price * 0.1425 / 100 * 0.28
