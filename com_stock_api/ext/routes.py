from com_stock_api.nasdaq_pred.prediction_api import Prediction, Predictions
# from com_stock_api.us_covid.us_covid_api import USCovid, USCovids
# from com_stock_api.yhfinance.yhfinance_api import YHFinance, YHFinances
# from com_stock_api.investing.api import Investing, Investings
from com_stock_api.home.api import Home

def initialize_routes(api):
    print("====2====")
    api.add_resource(Home, '/nasdaq')
    api.add_resource(Prediction, '/nasdaq/prediction')
    api.add_resource(Predictions, '/nasdaq/predictions')



