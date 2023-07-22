from flask import Flask, render_template, jsonify
import requests
from controller.api_controller import bp as controller_bp

app = Flask(__name__)
app.register_blueprint(controller_bp)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_stock_data/<string:stock_id>', methods=['GET'])
def get_stock_data(stock_id):
    # 將股票 ID 附加到 API URL 中
    api_url = f'http://127.0.0.1:5000/get_stock_data_api/{stock_id}'
    print(api_url)
    try:
        # 發送 GET 請求
        response = requests.get(api_url)
        # print(response)
        # print(response.json())
        # api_text = response1.text
        # 確認回應成功（狀態碼 200）
        if response.status_code == 200:
            # 將 API 回應的 JSON 格式資料轉換成 Python 字典
            stock_price_list = response.json()
            print(stock_price_list)
            print(type(stock_price_list))
            # data_dict = dict(api_text)
            # print(data_dict)
            return jsonify(stock_price_list)
        else:
            return jsonify({"error": "Failed to fetch data"}), 500

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Request Error: {e}"}), 500


if __name__ == '__main__':
    app.run(debug=True)
