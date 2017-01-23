from sqlalchemy import Column, Integer, String, Table, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

# Get database user and password from environmental variables
username = os.getenv("SCRAPY_DB_USER")
password = os.getenv("SCRAPY_DB_PASS")

class LogItem(Base):
    __tablename__ = 'ICPDLog'
    dispatch = Column(Integer, primary_key=True)
    inc = Column(String(1000))
    activity = Column(String(1000))
    disposition = Column(String(1000))
    addr = Column(String(1000))
    apt = Column(String(1000))
    time = Column(String(1000))
    date = Column(String(1000))

db = create_engine('mysql+pymysql://%s:%s@127.0.0.1/ICPDLog?charset=utf8mb4' % (username, password), echo=False)

Base.metadata.create_all(db)
Session = sessionmaker()
Session.configure(bind=db)
session = Session()

def AddToDb(scrapy_item):
    item = LogItem()
    item.dispatch = scrapy_item['dispatch']
    item.inc = str(scrapy_item['inc'])
    item.activity = scrapy_item['activity']
    item.disposition = scrapy_item['disposition']
    item.addr = scrapy_item['addr']
    item.apt = scrapy_item['apt']
    item.time = scrapy_item['time']
    item.date = scrapy_item['date']

    session = Session()
    session.merge(item)
    session.commit()


