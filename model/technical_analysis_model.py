import unittest

import numpy as np
import pandas as pd

from model.get_now_price_model import GetRealtimeStockPrice


class TechnicalAnalysisModel:
    @staticmethod
    def get_up_down_list(close_price_list):
        return [0] + [close_price_list[i] - close_price_list[i - 1] for i in range(1, len(close_price_list))]

    def get_rsi(self, close_price_list):
        days_up_down_list = self.get_up_down_list(close_price_list)
        up_mean = np.sum([up_down for up_down in days_up_down_list if up_down > 0])
        down_mean = -np.sum([up_down for up_down in days_up_down_list if up_down < 0])
        return round(up_mean / (up_mean + down_mean) * 100, 2)

    def get_rsi_list(self, close_price_list, days):
        rsi_list = [0 for _ in range(days - 1)]
        for i in range(len(close_price_list) - (days - 1)):
            days_close_price_list = close_price_list[i:(i + days)]
            rsi = self.get_rsi(days_close_price_list)
            rsi_list.append(rsi)
        return rsi_list

    def get_kd_list(self, low_price_list, high_price_list, close_price_list):
        # 計算RSVt
        df1 = pd.DataFrame({
            'Close': close_price_list,
            'Low': low_price_list,
            'High': high_price_list,
        })
        n = 9
        df1['lowest'] = df1['Low'].rolling(n).min()
        df1['highest'] = df1['High'].rolling(n).max()
        df1['rsvt'] = (df1['Close'] - df1['lowest']) / (df1['highest'] - df1['lowest']) * 100

        # 計算Kt和Dt
        k_weight = 3
        d_weight = 3
        df1['kt'] = df1['rsvt'].ewm(alpha=1 / k_weight, adjust=False).mean()
        df1['dt'] = df1['kt'].ewm(alpha=1 / d_weight, adjust=False).mean()
        k_list = df1['kt'].to_list()
        d_list = df1['dt'].to_list()
        return k_list, d_list

    def get_kd_golden_cross_stock_id_list(self, all_stock_id_np, all_stock_df_dict):
        get_realtime_stock_price = GetRealtimeStockPrice()
        now_stock_df = get_realtime_stock_price.get_realtime_strock_price_df()
        kd_golden_cross_list = list()
        for stock_id in all_stock_id_np:
            stock_df = all_stock_df_dict[stock_id]
            # stock_df = pd.concat([stock_df, now_stock_df[now_stock_df['stock_id'] == str(stock_id)]])
            stock_df = stock_df.reset_index()
            high_price_list = stock_df['High'].to_list()
            low_price_list = stock_df['Low'].to_list()
            close_price_list = stock_df['Close'].to_list()
            k_list, d_list = self.get_kd_list(low_price_list, high_price_list, close_price_list)
            if len(k_list) == 0 or len(d_list) == 0:
                continue
            if d_list[-1] < k_list[-1] and k_list[-2] < d_list[-2] and d_list[-1] < 35 and k_list[-1] < 35:  # 增加低檔黃金交叉
                kd_golden_cross_list.append(stock_id)
        return kd_golden_cross_list

    def get_rsi_below_20_stock_id_list(self, all_stock_id_np, all_stock_df_dict):
        technical_analysis_model = TechnicalAnalysisModel()
        get_realtime_stock_price = GetRealtimeStockPrice()
        now_stock_df = get_realtime_stock_price.get_realtime_strock_price_df()
        rsi_small_than_20_stock_id_list = list()
        for stock_id in all_stock_id_np:
            stock_df = all_stock_df_dict[stock_id]
            # stock_df = pd.concat([stock_df, now_stock_df[now_stock_df['stock_id'] == str(stock_id)]])
            stock_df = stock_df.reset_index()
            close_price_list = stock_df['Close'].to_list()
            rsi_days = 6
            today_rsi = technical_analysis_model.get_rsi(close_price_list[-rsi_days:])
            if today_rsi < 20:
                rsi_small_than_20_stock_id_list.append(stock_id)
        return rsi_small_than_20_stock_id_list

    def above_percent_increase_stock_id_list(self, all_stock_id_np, all_stock_df_dict, percent):
        get_realtime_stock_price = GetRealtimeStockPrice()
        now_stock_df = get_realtime_stock_price.get_realtime_strock_price_df()
        stock_id_list = list()
        for stock_id in all_stock_id_np:
            stock_df = all_stock_df_dict[stock_id]
            # stock_df = pd.concat([stock_df, now_stock_df[now_stock_df['stock_id'] == str(stock_id)]])
            close_price_list = stock_df['Close'].to_list()
            today_price = close_price_list[-1]
            yesterday_price = close_price_list[-2]
            if (today_price - yesterday_price) / yesterday_price > percent:
                stock_id_list.append(stock_id)
        return stock_id_list


class TestFeatureFunction(unittest.TestCase):
    @classmethod
    def setup_class(cls):
        cls.technical_analysis_model = TechnicalAnalysisModel()

    def test_get_up_down_list(self):
        self.assertEqual(self.technical_analysis_model.get_up_down_list([10, 5, 15, 20]), [0, -5, 10, 5])

    def test_get_rsi(self):
        self.assertEqual(self.technical_analysis_model.get_rsi([23.7, 27.9, 26.5, 29.6, 31.1, 29.4]), 73.95)

    def test_get_rsi_list(self):
        self.assertEqual(self.technical_analysis_model.get_rsi_list([23.7, 27.9, 26.5, 29.6, 31.1, 29.4, 25.5, 28.9, 20.5, 23.3], 6),
                         [0, 0, 0, 0, 0, 73.95, 39.66, 58.82, 25.93, 30.69])
