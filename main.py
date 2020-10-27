from flask import Flask
from flask_restful import Api
from com_stock_api.ext.db import url, db
from com_stock_api.ext.routes import initialize_routes
from com_stock_api.resources.prediction import PredictionDao
from com_stock_api.resources.uscovid import USCovidDao
from com_stock_api.resources.yhfinance import YHFinanceDao
from com_stock_api.resources.investingnews import InvestingDao

from com_stock_api.resources.member import MemberDao
from com_stock_api.resources.board import BoardDao
from com_stock_api.resources.comment import CommentDao
from com_stock_api.resources.member_churn_pred import MemberChurnPredDao
from com_stock_api.resources.recommend_stock import RecommendStockDao
from com_stock_api.resources.trading import TradingDao

from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r'/api/*': {"origins": "*"}})

# app.register_blueprint(member)
# app.register_blueprint(board)

print('====== url ======')
print(url)

app.config['SQLALCHEMY_DATABASE_URI'] = url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
api = Api(app)

with app.app_context():
    db.create_all()
with app.app_context():
    count1 = USCovidDao.count()
    print(f'US Covid case Total Count is {count1}')
    if count1 == 0:
        USCovidDao.insert_many()
with app.app_context():
    count2 = YHFinanceDao.count()
    print(f'NASDAQ history data Total Count is {count2}')
    if count2 == 0:
        YHFinanceDao.insert_many()
with app.app_context():
    count3 = InvestingDao.count()
    print(f'Stock news Total Count is {count3}')
    if count3 == 0:
        InvestingDao.insert_many()

with app.app_context():
    count = MemberDao.count()
    print(f'Members Total Count is {count}')
    if count == 0:
        MemberDao.insert_many()
with app.app_context():
    count = BoardDao.count()
    print(f'Boards Total Count is {count}')
    if count == 0:
        BoardDao.insert_many()

with app.app_context():
    count = MemberChurnPredDao.count()
    print(f'MemberChurnPredictions Total Count is {count}')
    if count == 0:
        MemberChurnPredDao.insert_many()

initialize_routes(api)

@app.route('/nasdaq/test')
def test():
    return {'test':'SUCCESS'}