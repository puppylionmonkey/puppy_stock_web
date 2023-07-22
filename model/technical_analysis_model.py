import numpy as np


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
