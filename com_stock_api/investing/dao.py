from com_stock_api.ext.db import db, openSession
from com_stock_api.investing.dto import InvestingDto
import os
import pandas as pd


class InvestingDao():

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_date(cls, date):
        return cls.query.filer_by(date == date).all()

    @staticmethod   
    def insert_many():
        Session = openSession()
        session = Session()
        tickers = ['AAPL', 'TSLA']
        for tic in tickers:
            path = os.path.abspath(__file__+"/.."+"/data/")
            file_name = tic + '_sentiment.csv'
            input_file = os.path.join(path,file_name)

            df = pd.read_csv(input_file)
            print(df.head())
            session.bulk_insert_mappings(InvestingDto, df.to_dict(orient="records"))
            session.commit()
        session.close()


# news = InvestingDao()
# news.insert_many()
