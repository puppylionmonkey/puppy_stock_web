from pymongo import MongoClient

from model.financial_system_model import FinancialSystemModel
from model.stock_system_model import StockSystemModel


class User:
    def __init__(self, username):
        self.financial_system = FinancialSystemModel()
        self.stock_system = StockSystemModel()

        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["user_db"]
        self.user_balance_collection = self.db["user_balance"]

        self.username = username
        self.balance = self.financial_system.get_balance(username)

    def buy_stock(self, orders_collection, username, stock_symbol, quantity, price):
        # 錢
        total_price = quantity * price
        buy_fee = self.financial_system.get_fee(quantity, price)
        self.financial_system.update_balance(self.username, -total_price - buy_fee)
        # 股票
        existing_order = orders_collection.find_one({"stock_symbol": stock_symbol, "username": username})
        if existing_order:  # 有庫存
            new_quantity = existing_order["quantity"] + quantity
            if new_quantity == 0:
                self.stock_system.delete_stock(username, stock_symbol)
            else:
                new_total_price = existing_order["total_price"] + price * quantity
                self.stock_system.update_stock(username, stock_symbol, quantity, new_total_price)
        else:  # 沒庫存
            total_price = quantity * price
            self.stock_system.create_stock(username, stock_symbol, quantity, total_price)

    def sell_stock(self, orders_collection, username, stock_symbol, quantity, price):
        # 錢
        total_price = quantity * price
        buy_fee = self.financial_system.get_fee(quantity, price)
        tax = self.financial_system.get_tax(quantity, price)
        self.financial_system.update_balance(self.username, +total_price - buy_fee - tax)
        # 股票
        existing_order = orders_collection.find_one({"stock_symbol": stock_symbol, "username": username})
        if existing_order:  # 有庫存
            new_quantity = existing_order["quantity"] - quantity
            if new_quantity == 0:
                self.stock_system.delete_stock(username, stock_symbol)
            else:
                new_total_price = existing_order["total_price"] - price * quantity
                self.stock_system.update_stock(username, stock_symbol, -quantity, new_total_price)
        else:  # 沒庫存
            total_price = -quantity * price
            self.stock_system.create_stock(username, stock_symbol, -quantity, total_price)
