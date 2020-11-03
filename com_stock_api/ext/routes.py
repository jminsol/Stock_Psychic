from com_stock_api.resources.nasdaq_prediction import NasdaqPrediction, NasdaqPredictions, TeslaPredGraph, ApplePredGraph
from com_stock_api.resources.home import Home
from com_stock_api.resources.yhfinance import YHFinance, YHFinances, TeslaGraph, AppleGraph
from com_stock_api.resources.recent_news import RecentNews, AppleNews, TeslaNews
from com_stock_api.resources.investingnews import Investing, AppleSentiment, TeslaSentiment
from com_stock_api.resources.nasdaq_prediction import NasdaqPrediction, NasdaqPredictions, ApplePredGraph, TeslaPredGraph
from com_stock_api.resources.uscovid import USCovid, USCovids
from com_stock_api.resources.member import Member, Members, Auth, Access
from com_stock_api.resources.board import Board, Boards
from com_stock_api.resources.comment import Comment, Comments
# from com_stock_api.resources.trading import Trading, Tradings

def initialize_routes(api):
    print("====2====")
    api.add_resource(Home, '/nasdaq')
    api.add_resource(NasdaqPredictions, '/nasdaq/predictions')
    api.add_resource(ApplePredGraph, '/nasdaq/apple_pred')
    api.add_resource(TeslaPredGraph, '/nasdaq/tesla_pred')
    api.add_resource(AppleGraph, '/nasdaq/apple')
    api.add_resource(TeslaGraph, '/nasdaq/tesla')
    api.add_resource(AppleNews, '/nasdaq/apple_news')
    api.add_resource(TeslaNews, '/nasdaq/tesla_news')
    api.add_resource(AppleSentiment, '/nasdaq/apple_sentiment')
    api.add_resource(TeslaSentiment, '/nasdaq/tesla_sentiment')
    api.add_resource(USCovid, '/nasdaq/uscovid')

    api.add_resource(Members, '/api/members')
    api.add_resource(Member, '/api/member/<string:email>')
    api.add_resource(Auth, '/api/auth')
    print('=============== route.py')
    api.add_resource(Access, '/api/access')
    api.add_resource(Boards, '/api/boards')
    api.add_resource(Board, '/api/board')
    api.add_resource(Comments, '/api/comments')
    api.add_resource(Comment, '/api/comment/<string:id>')
    # api.add_resource(Tradings, '/api/tradings')
    # api.add_resource(Trading, '/api/trading/<string:id>')
    # api.add_resource(MemberChurnPreds, '/api/member-churn-preds')
    # api.add_resource(MemberChurnPred, '/api/member-churn-preds')
    # api.add_resource(RecommendStocks, '/api/recommend-stocks')
    # api.add_resource(RecommendStock, '/api/recommend-stocks')



