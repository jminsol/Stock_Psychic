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

class USCovidDto(db.Model):
    __tablename__ = 'US_Covid_cases'
    __table_args__={'mysql_collate':'utf8_general_ci'}
    id: int = db.Column(db.Integer, primary_key = True, index = True)
    date: str = db.Column(db.Date)
    total_cases: int = db.Column(db.Integer)
    total_deaths: int = db.Column(db.Integer)
    ca_cases : int = db.Column(db.Integer)
    ca_deaths: int = db.Column(db.Integer)
    #date format : YYYY-MM-DD
    
    def __repr__(self):
        return f'USCovid(id=\'{self.id}\', date=\'{self.date}\', total_cases=\'{self.total_cases}\',\
            total_deaths=\'{self.total_deaths}\',ca_cases=\'{self.ca_cases}\', \
                ca_deaths=\'{self.ca_deaths}\')'


    @property
    def json(self):
        return {
            'id' : self.id,
            'date' : self.date,
            'total_cases' : self.total_cases,
            'total_deaths' : self.total_death,
            'ca_cases' : self.ca_cases,
            'ca_deaths' : self.ca_death,
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

path = os.path.abspath(__file__+"/.."+"/data/")
file_name = 'covid.csv'
input_file = os.path.join(path,file_name)
df = pd.read_csv(input_file)
print(df.head())
s.bulk_insert_mappings(USCovidDto, df.to_dict(orient="records"))
s.commit()
s.close()
'''