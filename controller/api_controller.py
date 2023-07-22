from flask import Blueprint

from model import GetStockPrice

bp = Blueprint('controller', __name__)


@bp.route('/get_stock_data_api/<string:stock_id>', methods=['GET'])
def get_stock_data_api(stock_id):
    get_stock_price = GetStockPrice()
    stock_price_df = get_stock_price.get_stock_price_df_from_mongodb(stock_id)
    return stock_price_df.to_json(orient='records')
