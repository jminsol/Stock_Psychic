from com_stock_api.nasdaq_pred.prediction_api import Prediction, Predictions

def initialize_routes(api):
    api.add_resource(Prediction, '/api/prediction')



