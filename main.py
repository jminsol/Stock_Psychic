from flask import Flask
from flask_restful import Api
from com_stock_api.ext.db import url, db
from com_stock_api.ext.routes import initialize_routes
from com_stock_api.nasdaq_pred.prediction_api import Prediction, Predictions
from com_stock_api.us_covid.us_covid_api import USCovid, USCovids
from com_stock_api.yhfinance.yhfinance_api import YHFinance, YHFinances
from com_stock_api.yhnews.yhnews_api import YHNews, YHNewses

from com_stock_api.member.member_api import MemberApi, Members
from com_stock_api.board.board_api import BoardApi, Boards
from com_stock_api.comment.comment_api import CommentApi, Comments
from com_stock_api.trading.trading_api import TradingApi, Tradings
from com_stock_api.memberChurn_pred.memberChurn_pred_api import MemberChurnPredApi, MemberChurnPreds
from com_stock_api.recommend_stock.recommend_stock_api import RecommendStockApi, RecommendStocks

from com_stock_api.korea_covid.api import KoreaCovid,KoreaCovids
from com_stock_api.kospi_pred.api import Kospi,Kospis
from com_stock_api.naver_finance.api import Stock,Stocks
from com_stock_api.naver_news.api import News,News_



from flask_cors import CORS
app = Flask(__name__)
CORS(app)
print('========== url ==========')
print(url)
app.config['SQLALCHEMY_DATABASE_URI'] = url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

initialize_routes(api)

with app.app_context():
    db.create_all()

@app.route('/api/test')
def test():
    return {'test':'SUCCESS'}