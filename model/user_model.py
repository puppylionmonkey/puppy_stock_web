from pymongo import MongoClient

from model.financial_system_model import FinancialSystemModel


class User:
    def __init__(self, username):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["user_db"]
        self.user_balance_collection = self.db["user_balance"]

        self.username = username
        financial_systemModel = FinancialSystemModel()
        self.balance = financial_systemModel.get_balance(username)

    def buy_stock(self, orders_collection, username, stock_symbol, quantity, price):
        existing_order = orders_collection.find_one({"stock_symbol": stock_symbol, "username": username})
        if existing_order:  # 有庫存
            new_quantity = existing_order["quantity"] + quantity
            if new_quantity == 0:
                orders_collection.delete_one({"stock_symbol": stock_symbol, "username": username})
            else:
                new_total_price = existing_order["total_price"] + price * quantity
                orders_collection.update_one(
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
            orders_collection.insert_one(order)

    def sell_stock(self, orders_collection, username, stock_symbol, quantity, price):
        existing_order = orders_collection.find_one({"stock_symbol": stock_symbol, "username": username})
        if existing_order:  # 有庫存
            new_quantity = existing_order["quantity"] - quantity
            if new_quantity == 0:
                orders_collection.delete_one({"stock_symbol": stock_symbol, "username": username})
            else:
                new_total_price = existing_order["total_price"] - price * quantity
                orders_collection.update_one(
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
            orders_collection.insert_one(order)
