from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects import registry
import mysql.connector
import sqlalchemy.dialects.sqlite
import pymysql

db = SQLAlchemy()

# Local DB
config = {
    'user' : 'root',
    'password' : 'root',
    'host': '127.0.0.1',
    'port' : '3306',
    'database' : 'stockdb'
}

# AWS DB

'''
config = {
    'user' : 'stockpsychic',
    'password' : 'stockpsychic',
    'host': 'stockpsychic.c4fat9wcknyn.ap-northeast-2.rds.amazonaws.com',
    'port' : '3306',
    'database' : 'stockpsychic'
}
'''
# registry.register('mysql.mysqlconnector', 'mysqlconnector', 'dialect')
charset = {'utf8':'utf8'}
Base = declarative_base()
url = f"mysql+pymysql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}?charset=utf8"
engine = create_engine(url)

def openSession():
    return sessionmaker(bind=engine)