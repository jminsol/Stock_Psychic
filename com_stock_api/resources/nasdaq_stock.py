from flask_restful import Resource, reqparse
from com_stock_api.ext.db import db, openSession
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
import pandas as pd
import os
import matplotlib.pyplot as plt
from pandas_datareader import data as pdr
import yfinance as yf
yf.pdr_override() 
from datetime import datetime, timedelta



class NasdaqStockDto(db.Model):
    __tablename__ = 'NASDAQ_Stocks'
    __table_args__={'mysql_collate':'utf8_general_ci'}
    id: int = db.Column(db.Integer, primary_key = True, index = True)
    ticker : str = db.Column(db.String(10))
    date : str  = db.Column(db.Date)
    open : float = db.Column(db.Float)
    high : float = db.Column(db.Float)
    low : float = db.Column(db.Float)
    close : float = db.Column(db.Float)
    adjclose : float = db.Column(db.Float)
    volume : int = db.Column(db.Integer)
    #date format : YYYY-MM-DD
    
    def __init__(self, ticker, date, open, high, low, close, adjclose, volume):
        self.ticker = ticker
        self.date = date
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.adjclose = adjclose
        self.volume = volume

    def __repr__(self):
        return f'RecentNews(id=\'{self.id}\', date=\'{self.date}\', time=\'{self.time}\',\
            ticker=\'{self.ticker}\',link=\'{self.link}\', \
                headline=\'{self.headline}\', content=\'{self.content}\')'


    @property
    def json(self):
        return {
            'id' : self.id,
            'ticker' : self.ticker,
            'date' : self.date,
            'open' : self.open,
            'high' : self.high,
            'low' : self.low,
            'close' : self.close,
            'adjclose' : self.adjclose,
            'volume' : self.volume
        }

class NasdaqStockVo:
    id: int = 0
    ticker: str = ''
    date : str = ''
    open: float = 0.0
    high: float = 0.0
    low: float = 0.0
    close: float = 0.0
    adjclose: float = 0.0
    volume: int = 0

class NasdaqStockDao(NasdaqStockDto):

    @classmethod
    def count(cls):
        return cls.query.count()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_date(cls, date):
        return cls.query.filer_by(date == date).all()

    @staticmethod   
    def insert_many():
        service = NasdaqStockPro()
        Session = openSession()
        session = Session()
        dfs = service.hook()
        for i in dfs:
            print(i.head())
            session.bulk_insert_mappings(NasdaqStockDto, i.to_dict(orient="records"))
            session.commit()
        session.close()

    @staticmethod
    def save(news):
        db.session.add(news)
        db.session.commit()

    @staticmethod
    def delete(cls, id):
        data = cls.query.get(id)
        db.session.delete(data)
        db.session.commit()


# =============================================================
# =============================================================
# ======================      SERVICE    ======================
# =============================================================
# =============================================================

class NasdaqStockPro:
    tickers : str = ['AAPL', 'TSLA']
    ticker : str
    START_DATE: str = '2020-07-01'
    END_DATE: str = datetime.now()

    def __init__(self):
        self.ticker = ''
        
    def hook(self):
        histories = []
        for t in self.tickers:
            self.ticker = t
            history = self.saved_to_csv(self.get_history())
            histories.append(self.process_dataframe(history))
        return histories

    def get_history(self):
        data = pdr.get_data_yahoo(self.ticker, start=self.START_DATE, end=self.END_DATE)
        return data

    def get_history_by_date(self, start, end):
        data = pdr.get_data_yahoo(self.ticker, start=start, end=end)
        return data
    
    def get_file_path(self):
        path = os.path.abspath(__file__+"/.."+"/data/")
        file_name = self.ticker + '_now.csv'
        return os.path.join(path,file_name)

    def process_dataframe(self, df):
        # d = {"date":df['Date'], "open": df['Open'], "high": df['High'], "low": df['Low'],"close": df['Close'],"adjclose": df['Adj Close'],"volume": df['Volume']}
        input_file = self.get_file_path()
        print("input file: ", input_file)
        data = pd.read_csv(input_file)
        data.rename(columns = {'Date' : 'date', 'Open':'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Adj Close' :'adjclose', 'Volume':'volume'}, inplace = True)
        data.insert(loc=0, column='ticker', value=self.ticker)
        
        output_file = self.get_file_path()
        data.to_csv(output_file)
        return data

    def saved_to_csv(self, data):
        output_file = self.get_file_path()
        data.to_csv(output_file)

# =============================================================
# =============================================================
# ======================      CONTROLLER    ======================
# =============================================================
# =============================================================
parser = reqparse.RequestParser()
parser.add_argument('id', type=int, required=False, help='This field cannot be left blank')
parser.add_argument('ticker', type=str, required=False, help='This field cannot be left blank')
parser.add_argument('date', type=str, required=False, help='This field cannot be left blank')
parser.add_argument('open', type=float, required=False, help='This field cannot be left blank')
parser.add_argument('high', type=float, required=False, help='This field cannot be left blank')
parser.add_argument('low', type=float, required=False, help='This field cannot be left blank')
parser.add_argument('close', type=float, required=False, help='This field cannot be left blank')
parser.add_argument('adjclose', type=float, required=False, help='This field cannot be left blank')
parser.add_argument('volume', type=int, required=False, help='This field cannot be left blank')

class NasdaqStock(Resource):

    @staticmethod
    def post():
        data = parser.parse_args()
        nasdaq_stock = NasdaqStockDto(data['date'], data['ticker'],data['open'], data['high'], data['low'], data['close'],  data['adjclose'], data['volume'])
        try: 
            nasdaq_stock.save(data)
            return {'code' : 0, 'message' : 'SUCCESS'}, 200

        except:
            return {'message': 'An error occured inserting the current stock'}, 500
        return nasdaq_stock.json(), 201
        
    
    @staticmethod
    def get(self, id):
        nasdaq_stock = NasdaqStockDao.find_by_id(id)
        if nasdaq_stock:
            return nasdaq_stock.json()
        return {'message': 'The current nasdaq stock was not found'}, 404

    @staticmethod
    def put(self, id):
        data = NasdaqStock.parser.parse_args()
        stock = NasdaqStockDao.find_by_id(id)

        stock.date = data['date']
        stock.close = data['close']
        stock.save()
        return stock.json()

class NasdaqStocks(Resource):
    def get(self):
        return {'Current Stock price list': list(map(lambda article: article.json(), NasdaqStockDao.find_all()))}