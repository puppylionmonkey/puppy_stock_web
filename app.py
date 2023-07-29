import pandas as pd
from flask import Flask, render_template, jsonify, request
from controller.api_controller import bp as controller_bp
from model.get_now_price_model import GetRealtimeStockPrice
from model.get_price_model import GetStockHistoryPrice
from model.technical_analysis_model import TechnicalAnalysisModel
from path_config import path_database_path
from flask_caching import Cache

app = Flask(__name__)
app.register_blueprint(controller_bp)

cache = Cache(app, config={'CACHE_TYPE': 'simple'})
get_stock_history_price = GetStockHistoryPrice()
stock_id_table_df = pd.read_csv(path_database_path + 'stock_id_table.csv')
all_stock_id_np = stock_id_table_df['stock_id'].to_numpy()
all_stock_df_dict = get_stock_history_price.get_all_stock_df_dict_from_mongodb(all_stock_id_np)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/recommend_stock')
def recommend_stock():
    return render_template('recommend_stock.html')


@app.route('/get_recommend_stock_list', methods=['POST'])
def get_recommend_stock_list():
    selected_conditions = request.get_json()['options']
    print(selected_conditions)
    tech_stock_id_list_list = []
    technical_analysis_model = TechnicalAnalysisModel()
    if 'KD黃金交叉' in selected_conditions:
        print('abc')
        tech_stock_id_list_list.append(technical_analysis_model.get_kd_golden_cross_stock_id_list(all_stock_id_np, all_stock_df_dict))
    if 'RSI小於20' in selected_conditions:
        tech_stock_id_list_list.append(technical_analysis_model.get_rsi_below_20_stock_id(all_stock_id_np, all_stock_df_dict))

    # 做交集
    stock_id_list = set(tech_stock_id_list_list[0])
    for sublist in tech_stock_id_list_list[1:]:
        stock_id_list &= set(sublist)
    stock_id_list = list(stock_id_list)
    print(stock_id_list)
    return jsonify({"stock_id_list": stock_id_list})


if __name__ == '__main__':
    app.run(debug=True)
