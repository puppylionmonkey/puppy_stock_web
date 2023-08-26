import datetime

import pandas as pd
import requests


class GetRealtimeStockPrice:
    def get_realtime_open_low_high_close_price(self, stock_symbol):
        api_url = f"https://mis.twse.com.tw/stock/api/getStockInfo.jsp"
        params = {
            "ex_ch": f"tse_{stock_symbol}.tw",  # 股票代碼格式
            "json": "1",
        }
        response = requests.get(api_url, params=params)
        if response.status_code == 200:
            data = response.json()
            if "msgArray" in data:
                return float(data["msgArray"][0]["z"])  # close price

    def get_best_five_quotes(self, stock_symbol):
        api_url = f"https://mis.twse.com.tw/stock/api/getStockInfo.jsp"
        params = {
            "ex_ch": f"tse_{stock_symbol}.tw",  # 股票代碼格式
            "json": "1",
        }
        response = requests.get(api_url, params=params)
        if response.status_code == 200:
            data = response.json()
            if "msgArray" in data:
                best_sell_data = float(data["msgArray"][0]["a"].split('_')[0])
                best_buy_data = float(data["msgArray"][0]["b"].split('_')[0])
                return best_sell_data, best_buy_data
            else:
                print("Error: No data found")
                return None
        else:
            print("Error fetching data:", response.status_code)
            return None
