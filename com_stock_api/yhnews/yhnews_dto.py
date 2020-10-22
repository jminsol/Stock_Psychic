from com_stock_api.ext.db import db
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from com_stock_api.yhnews.investing_pro import InvestingPro
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

class YHNewsDto(db.Model):
    __tablename__ = 'Yahoo_News'
    __table_args__={'mysql_collate':'utf8_general_ci'}
        # , primary_key = True, index = True

    id: int = db.Column(db.Integer, primary_key = True, index = True)
    date : str = db.Column(db.Date)
    ticker : str = db.Column(db.String(30)) #stock symbol
    link : str = db.Column(db.String(30))
    headline : str = db.Column(db.String(255))
    neg : float = db.Column(db.Float)
    pos : float = db.Column(db.Float)
    neu : float = db.Column(db.Float)
    compound :float  = db.Column(db.Float)



    def __repr__(self):
        return f'User(id=\'{self.id}\', date=\'{self.date}\',ticker=\'{self.ticker}\',\
                link=\'{self.link}\', headline=\'{self.headline}\',neg=\'{self.neg}\', \
                pos=\'{self.pos}\',neu=\'{self.neu}\', compound=\'{self.compound}\',)'


    @property
    def json(self):
        return {
            'id': self.id,
            'date' : self.date,
            'ticker' : self.ticker,
            'link' : self.link,
            'headline' : self.headline,
            'neg' : self.neg,
            'pos' : self.pos,
            'neu' : self.neu,
            'compound' : self.compound
        }


    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

'''
# processing = InverstingPro()
Session = sessionmaker(bind=engine)
s =Session()
# When the files exist...
tickers = ['AAPL', 'TSLA']
for tic in tickers:
    path = os.path.abspath(__file__+"/.."+"/data/")
    file_name = tic + '_sentiment.csv'
    input_file = os.path.join(path,file_name)

    df = pd.read_csv(input_file)
    print(df.head())
    s.bulk_insert_mappings(YHNewsDto, df.to_dict(orient="records"))
    s.commit()
s.close()
'''