from com_stock_api.ext.db import db
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
import pandas as pd
import os


config = {
    'user' : 'root',
    'password' : 'root',
    'host': '127.0.0.1',
    'port' : '3306',
    'database' : 'stockdb'
}

charset = {'utf8':'utf8'}
url = f"mysql+mysqlconnector://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}?charset=utf8"
engine = create_engine(url)


class YHFinanceDto(db.Model):
    __tablename__ = 'Yahoo_Finance'
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
    # amount : unit = million 
    
    # Date,Open,High,Low,Close,Adj Close,Volume
    def __repr__(self):
        return f'YHFinance(id=\'{self.id}\',ticker=\'{self.ticker}\', date=\'{self.date}\',open=\'{self.open}\', \
            high=\'{self.high}\',low=\'{self.low}\', close=\'{self.close}\',\
                adjclose=\'{self.adjclose}\',volume=\'{self.volume}\',)'


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

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

'''
Session = sessionmaker(bind=engine)
s =Session()
# When the files exist...
tickers = ['AAPL', 'TSLA']
for tic in tickers:
    path = os.path.abspath(__file__+"/.."+"/data/")
    file_name = tic + '.csv'
    input_file = os.path.join(path,file_name)

    df = pd.read_csv(input_file)
    print(df.head())
    s.bulk_insert_mappings(YHFinanceDto, df.to_dict(orient="records"))
    s.commit()
s.close()
'''