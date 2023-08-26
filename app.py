import pandas as pd
from controller.api_controller import bp as controller_bp
from model.get_now_price_model import GetRealtimeStockPrice
from model.get_price_model import GetStockHistoryPrice
from model.order_model import OrderModel
from model.technical_analysis_model import TechnicalAnalysisModel
from path_config import path_database_path
from flask_caching import Cache
from flask import Flask, jsonify, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
app.register_blueprint(controller_bp)

cache = Cache(app, config={'CACHE_TYPE': 'simple'})
get_stock_history_price = GetStockHistoryPrice()
stock_id_table_df = pd.read_csv(path_database_path + 'stock_id_table.csv')
all_stock_id_np = stock_id_table_df['stock_id'].to_numpy()
all_stock_id_np = ['1101']
all_stock_df_dict = get_stock_history_price.get_all_stock_df_dict_from_mongodb(all_stock_id_np)

client = MongoClient("mongodb://localhost:27017/")
db = client["user_db"]
users = db["users"]
orders_collection = db["stock_inventory"]
app.secret_key = "bfe53d416ad39325e33062c5d7c629d962919a6edb88b0b7d4ba636b7ab23743"


@app.route("/", methods=["GET", "POST"])
def login():
    if "username" in session:
        return redirect(url_for("welcome"))
    if request.method == "POST":
        login_user = users.find_one({"username": request.form["username"]})
        if login_user:
            if bcrypt.checkpw(request.form["password"].encode("utf-8"), login_user["password"]):
                session["username"] = request.form["username"]
                return redirect(url_for("welcome"))
        return "無效的用戶名或密碼！"
    return render_template("login.html")


@app.route("/welcome")
def welcome():
    if "username" in session:
        return render_template("welcome.html")
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        existing_user = users.find_one({"username": request.form["username"]})
        if existing_user is None:
            hashed_password = bcrypt.hashpw(request.form["password"].encode("utf-8"), bcrypt.gensalt())
            users.insert_one({
                "username": request.form["username"],
                "password": hashed_password
            })
            return redirect(url_for("login"))
        return "該用戶名已存在！"
    return render_template("register.html")


# 登入後
@app.route("/dashboard")
def dashboard():
    if "username" in session:
        return f"歡迎，{session['username']}！這是你的儀表板。"
    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


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
        tech_stock_id_list_list.append(technical_analysis_model.get_rsi_below_20_stock_id_list(all_stock_id_np, all_stock_df_dict))
    if '漲5%以上' in selected_conditions:
        tech_stock_id_list_list.append(technical_analysis_model.above_percent_increase_stock_id_list(all_stock_id_np, all_stock_df_dict, 0.05))
    # 做交集
    stock_id_list = set(tech_stock_id_list_list[0])
    for sublist in tech_stock_id_list_list[1:]:
        stock_id_list &= set(sublist)
    stock_id_list = list(stock_id_list)
    print(stock_id_list)
    return jsonify({"stock_id_list": stock_id_list})


@app.route("/stock_order", methods=["GET", "POST"])
def stock_order():
    get_realtime_stock_price = GetRealtimeStockPrice()
    order_model = OrderModel()
    if "username" not in session:
        return redirect(url_for("login"))
    # 檢索該使用者的庫存股票
    inventory = order_model.get_user_inventory(session["username"])
    if request.method == "POST":
        print(request.form)
        stock_symbol = request.form["stock_symbol"]
        quantity = int(request.form["quantity"])
        best_sell_data, best_buy_data = get_realtime_stock_price.get_best_five_quotes(stock_symbol)
        if 'buy' in request.form:
            action = 'buy'
        else:
            action = 'sell'
        if action == 'buy':
            price = best_sell_data
        else:
            price = best_buy_data
        if action == "buy":
            order_model.buy_stock(session["username"], stock_symbol, quantity, price)
        elif action == "sell":
            order_model.sell_stock(session["username"], stock_symbol, quantity, price)

    return render_template("stock_order.html", inventory=inventory)  # 顯示下單表單和庫存股票


@app.route("/get_inventory")
def get_inventory():
    # 檢索該使用者的庫存股票
    inventory = list(orders_collection.find({"username": session["username"]}))
    inventory_data = [{"stock_symbol": item["stock_symbol"], "quantity": item["quantity"]} for item in inventory]
    return jsonify(inventory_data)  # 返回 JSON 格式的庫存數據


if __name__ == '__main__':
    app.run(debug=True)
