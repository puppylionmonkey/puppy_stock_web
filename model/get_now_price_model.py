import requests


class GetRealtimeStockPrice:
    @staticmethod
    def get_realtime_strock_price_df():
        pass
        # while True:
        #     try:
        #         now_df = pd.read_html('https://histock.tw/stock/rank.aspx?p=all')[0]
        #         realtime_strock_price_df = pd.DataFrame()
        #         realtime_strock_price_df['stock_id'] = now_df['代號▼']
        #         realtime_strock_price_df['Open'] = now_df['昨收▼']
        #         realtime_strock_price_df['High'] = now_df['最高▼']
        #         realtime_strock_price_df['Low'] = now_df['最低▼']
        #         realtime_strock_price_df['Close'] = now_df['價格▼']
        #         realtime_strock_price_df['Volume'] = now_df['成交量▼']
        #         realtime_strock_price_df['stock_name'] = now_df['名稱▼']
        #         realtime_strock_price_df['Date'] = [str(datetime.datetime.today().date()) for _ in range(len(realtime_strock_price_df))]
        #         return realtime_strock_price_df
        #     except:
        #         continue

    def get_best_five_quotes(self, stock_code):
        api_url = f"https://mis.twse.com.tw/stock/api/getStockInfo.jsp"
        params = {
            "ex_ch": f"tse_{stock_code}.tw",  # 股票代碼格式
            "json": "1",
        }
        response = requests.get(api_url, params=params)
        if response.status_code == 200:
            data = response.json()
            if "msgArray" in data:
                print(data)
                best_sell_data = float(data["msgArray"][0]["a"].split('_')[0])
                best_buy_data = float(data["msgArray"][0]["b"].split('_')[0])
                return best_sell_data, best_buy_data
            else:
                print("Error: No data found")
                return None
        else:
            print("Error fetching data:", response.status_code)
            return None
