from pymongo import MongoClient


class StockSystemModel:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["user_db"]
        self.orders_collection = self.db["stock_inventory"]

    def create_stock(self, username, stock_symbol, quantity, total_price):
        order = {
            "username": username,
            "stock_symbol": stock_symbol,
            "quantity": quantity,
            "total_price": total_price
        }
        self.orders_collection.insert_one(order)

    def update_stock(self, username, stock_symbol, quantity, new_total_price):
        existing_order = self.orders_collection.find_one({"stock_symbol": stock_symbol, "username": username})
        new_quantity = existing_order["quantity"] + quantity
        self.orders_collection.update_one(
            {"stock_symbol": stock_symbol, "username": username},
            {"$set": {"quantity": new_quantity, "total_price": new_total_price}}
        )

    def delete_stock(self, username, stock_symbol):
        self.orders_collection.delete_one({"stock_symbol": stock_symbol, "username": username})
