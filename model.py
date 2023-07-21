from pymongo import MongoClient
import pandas as pd


class GetStockPrice:
    def __init__(self):
        client = MongoClient('mongodb://localhost:27017/')
        self.mongodb = client['stock']

    def get_stock_data_list_from_mongodb(self, stock_id, column_name):
        collection = self.mongodb[str(stock_id)]
        data_collection = collection.find({}, {column_name: 1, '_id': 0})
        return [open_data[column_name] for open_data in data_collection]

    def get_stock_price_df_from_mongodb(self, stock_id):
        return pd.DataFrame({
            'Date': self.get_stock_data_list_from_mongodb(stock_id, 'Date'),
            'Open': self.get_stock_data_list_from_mongodb(stock_id, 'Open'),
            'Low': self.get_stock_data_list_from_mongodb(stock_id, 'Low'),
            'High': self.get_stock_data_list_from_mongodb(stock_id, 'High'),
            'Close': self.get_stock_data_list_from_mongodb(stock_id, 'Close'),
            'Volume': self.get_stock_data_list_from_mongodb(stock_id, 'Volume'),
        })

    def get_all_stock_df_dict_from_mongodb(self, all_stock_id_np):
        return {stock_id: self.get_stock_price_df_from_mongodb(stock_id) for stock_id in all_stock_id_np}
