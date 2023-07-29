from pymongo import MongoClient
import pandas as pd


class GetStockHistoryPrice:
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


class TestGetStockPrice:
    @classmethod
    def setup_class(cls):
        cls.get_stock_history_price = GetStockHistoryPrice()

    def test_get_stock_data_list_from_mongodb(self):
        stock_date_list = self.get_stock_history_price.get_stock_data_list_from_mongodb('2330', 'Date')
        assert '2000-01-04 00:00:00' == str(stock_date_list[0])
        # todo: 今天日期?

    def test_get_stock_price_df_from_mongodb(self):
        stock_df = self.get_stock_history_price.get_stock_price_df_from_mongodb('2330')
        assert '2000-01-04' in str(stock_df['Date'].to_numpy()[0])

    def test_get_all_stock_df_dict_from_mongodb(self):
        pass
