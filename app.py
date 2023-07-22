import json

import pandas as pd
from flask import Flask, render_template, jsonify
import requests
from controller.api_controller import bp as controller_bp
from model.get_price_model import GetStockPrice
from model.technical_analysis_model import TechnicalAnalysisModel
from path_config import path_database_path

app = Flask(__name__)
app.register_blueprint(controller_bp)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/recommend_stock')
def recommend_stock():
    return render_template('recommend_stock.html')


@app.route('/get_rsi_small_than_20_stock_id', methods=['GET'])
def get_rsi_small_than_20_stock_id():
    stock_id_table_df = pd.read_csv(path_database_path + 'stock_id_table.csv')
    all_stock_id_np = stock_id_table_df['stock_id'].to_numpy()
    get_stock_price = GetStockPrice()
    all_stock_df_dict = get_stock_price.get_all_stock_df_dict_from_mongodb(all_stock_id_np)
    rsi_small_than_20_stock_id_list = list()
    for stock_id in all_stock_id_np:
        # 將股票 ID 附加到 API URL 中
        stock_df = all_stock_df_dict[stock_id]
        close_price_list = stock_df['Close'].to_list()
        technical_analysis_model = TechnicalAnalysisModel()
        rsi_days = 6
        today_rsi = technical_analysis_model.get_rsi(close_price_list[-rsi_days:])
        if today_rsi < 20:
            rsi_small_than_20_stock_id_list.append(stock_id)
    print(rsi_small_than_20_stock_id_list)
    return render_template('recommend_stock.html', stock_id_list=rsi_small_than_20_stock_id_list)


if __name__ == '__main__':
    app.run(debug=True)
