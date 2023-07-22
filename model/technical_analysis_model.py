import unittest

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
