from flask import Flask, render_template, jsonify
import requests
from model import GetStockPrice

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


# API 路由
@app.route('/stocks/<string:stock_id>', methods=['GET'])
def get_stock_data(stock_id):
    get_stock_price = GetStockPrice()
    stock_price_df = get_stock_price.get_stock_price_df_from_mongodb(stock_id)
    print(stock_price_df.to_json(orient='records', lines=True))
    return stock_price_df.to_json(orient='records', lines=True)


@app.route('/get_stock_data/<string:stock_id>', methods=['GET'])
def get_stock_data1(stock_id):
    # 將股票 ID 附加到 API URL 中
    api_url = f'http://api.example.com/stocks/{stock_id}'

    try:
        # 發送 GET 請求
        response = requests.get(api_url)

        # 確認回應成功（狀態碼 200）
        if response.status_code == 200:
            # 將 API 回應的 JSON 格式資料轉換成 Python 字典
            stock_data = response.json()

            # 可以在這裡處理資料，例如進行額外的處理或轉換

            # 將處理後的資料以 JSON 格式回傳給前端
            return jsonify(stock_data)

        else:
            return jsonify({"error": "Failed to fetch data"}), 500

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Request Error: {e}"}), 500


if __name__ == '__main__':
    app.run()
