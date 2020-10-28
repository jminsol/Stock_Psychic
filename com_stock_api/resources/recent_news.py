from flask_restful import Resource, reqparse
from com_stock_api.ext.db import db, openSession
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
import pandas as pd
import os
import re
from bs4 import BeautifulSoup as bs
import matplotlib.pyplot as plt
import urllib
from urllib.request import Request, urlopen
import requests
from datetime import datetime, timedelta
from http.client import IncompleteRead
from unicodedata import normalize
from newspaper import Article



class RecentNewsDto(db.Model):
    __tablename__ = 'Recent_News'
    __table_args__={'mysql_collate':'utf8_general_ci'}
    id: int = db.Column(db.Integer, primary_key = True, index = True)
    date: str = db.Column(db.Date)
    time: str = db.Column(db.Time())
    ticker: str = db.Column(db.String(30))
    link: str = db.Column(db.String(30))
    headline: str = db.Column(db.String(225))
    content : str = db.Column(db.Text)
    #date format : YYYY-MM-DD
    
    def __init__(self, date, time, ticker, link, headline, content):
        self.date = date
        self.time = time
        self.ticker = ticker
        self.link = link
        self.headline = headline
        self.content = content

    def __repr__(self):
        return f'RecentNews(id=\'{self.id}\', date=\'{self.date}\', time=\'{self.time}\',\
            ticker=\'{self.ticker}\',link=\'{self.link}\', \
                headline=\'{self.headline}\', content=\'{self.content}\')'


    @property
    def json(self):
        return {
            'id' : self.id,
            'date' : self.date,
            'time' : self.time,
            'ticker' : self.ticker,
            'link' : self.link,
            'headline' : self.headline,
            'content' : self.content
        }

class RecentNewsVo:
    id: int = 0
    date: str = ''
    time : str = ''
    ticker: str = ''
    link: str = ''
    headline: str = ''
    content: str = ''

class RecentNewsDao(RecentNewsDto):

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
        service = RecentNewsPro()
        Session = openSession()
        session = Session()
        dfs = service.hook()
        for i in dfs:
            print(i.head())
            session.bulk_insert_mappings(RecentNewsDto, i.to_dict(orient="records"))
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

class RecentNewsPro:
    tickers: str = ['AAPL', 'TSLA']
    ticker : str
    finviz_url = 'https://finviz.com/quote.ashx?t='

    def __init__(self):
        ...
    
    def hook(self):
        dfs=[]
        for t in self.tickers:
            self.ticker = t
            lst = self.get_latest_news()
            self.save_news(lst)
            df= self.df_processing(lst)
            dfs.append(df)
        return dfs
        print( " ++ DONE ++ ")

    def get_latest_news(self):
        ticker = self.ticker
        url = self.finviz_url

    # Open url
        url +=ticker
        req = Request(url=url, headers={'user-agent': 'my-app/0.0.1'})
        resp = urlopen(req)
        html = bs(resp, features="lxml")
        news_table = html.find(id='news-table')

    # Extract news data only

        df = news_table.findAll('tr')
        today = datetime.now()
        recent = today - timedelta(days = 3)
        processed_data = []
        
        for i, row in enumerate(df):
            headline = row.a.text
            time = row.td.text
            time = time.strip()
            link = row.find("a").get("href")
            
            # Get published date and time
            date_time = self.get_published_datetime(time)
            published_date = date_time[0] if (date_time[0]!=0) else (processed_data[-1][0])
            published_time = date_time[1]
            
            #Get news content
            if "https://finance.yahoo.com/news" in link:
                content=self.get_yahoo_news(link)
            else:
                article = Article(link)
                article.download()
                article.parse()
                content = self.clean_paragraph(article.text)
                content = "".join(content)
          
            #Scrap news data 
            processed_data.append([published_date, published_time, self.ticker, link, headline, content])
            
            if (datetime.strptime(published_date, '%Y-%m-%d') < recent):
                processed_data.pop()
                break
        return processed_data

    def get_published_datetime(self, time):
        
        try:
            publish_date = str(datetime.strptime(time, '%b-%d-%y %I:%M%p'))
            publish_date = "".join(publish_date)
            pub_time = publish_date[11:]
            publish_date = publish_date[:10]

        except ValueError:
            publish_date = 0
            pub_time = str(datetime.strptime(time, '%I:%M%p'))
            pub_time = "".join(pub_time)[11:]

        return publish_date, pub_time

    def get_yahoo_news(self, link):
        request = Request(link, headers={"User-Agent": "Mozilla/5.0"})
        content = urlopen(request).read()
        page= bs(content, 'lxml')

        text_tag = page.find('div', attrs={'class': 'caas-body'})
        paragraphs = text_tag.find_all('p')
        text = '\n'.join([self.clean_paragraph(p.get_text()) for p in paragraphs[:-1]])
        text = "".join(text)
        return text

    def clean_paragraph(self, paragraph):
        paragraph = re.sub(r'\(http\S+', '', paragraph)
        paragraph = re.sub(r'\([A-Z]+:[A-Z]+\)', '', paragraph)
        paragraph = re.sub(r'[\n\t\s\']', ' ', paragraph)
        return normalize('NFKD', paragraph)    

    def save_news(self, data):
        col = ['date', 'time', 'ticker', 'link', 'headline', 'content']
        df = pd.DataFrame(data, columns=col)
        path = os.path.abspath(__file__+"/.."+"/saved_data/")
        file_name = self.ticker + '_recent_news.csv'
        output_file = os.path.join(path,file_name)
        df.to_csv(output_file)
        print("Completed saving ", file_name)
    
    def df_processing(self, data):
        col = ['date', 'time', 'ticker', 'link', 'headline', 'content']
        df = pd.DataFrame(data, columns=col)
        return df
'''
if __name__=='__main__':
    news_pro = RecentNewsPro('TSLA')
    news_pro2 = RecentNewsPro('AAPL')

    news_pro.hook()
    news_pro2.hook()

'''
# 'date', 'time', 'ticker', 'link', 'headline', 'content'
# =============================================================
# =============================================================
# ======================      CONTROLLER    ======================
# =============================================================
# =============================================================
parser = reqparse.RequestParser()
parser.add_argument('id', type=int, required=False, help='This field cannot be left blank')
parser.add_argument('date', type=str, required=False, help='This field cannot be left blank')
parser.add_argument('time', type=str, required=False, help='This field cannot be left blank')
parser.add_argument('ticker', type=str, required=False, help='This field cannot be left blank')
parser.add_argument('link', type=str, required=False, help='This field cannot be left blank')
parser.add_argument('headline', type=str, required=False, help='This field cannot be left blank')
parser.add_argument('content', type=str, required=False, help='This field cannot be left blank')

class RecentNews(Resource):

    @staticmethod
    def post():
        data = parser.parse_args()
        recent_news = RecentNewsDto(data['date'], data['time'] ,data['ticker'], data['link'],data['headline'], data['content'])
        try: 
            recent_news.save(data)
            return {'code' : 0, 'message' : 'SUCCESS'}, 200

        except:
            return {'message': 'An error occured inserting recent news'}, 500
        return recent_news.json(), 201
        
    
    @staticmethod
    def get(self, id):
        recent_news = RecentNewsDao.find_by_id(id)
        if recent_news:
            return recent_news.json()
        return {'message': 'the news not found'}, 404

    @staticmethod
    def put(self, id):
        data = RecentNews.parser.parse_args()
        stock = RecentNewsDao.find_by_id(id)

        stock.headline = data['headline']
        stock.content = data['content']
        stock.save()
        return stock.json()

class RecentNews_(Resource):
    def get(self):
        return {'Recent News list': list(map(lambda article: article.json(), RecentNewsDao.find_all()))}