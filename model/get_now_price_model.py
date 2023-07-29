import datetime

import pandas as pd


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
