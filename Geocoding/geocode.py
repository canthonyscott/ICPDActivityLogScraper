from sqlalchemy import Column, Integer, String, Table, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import googlemaps
import os

Base = declarative_base()
BASE_LOC = 'Iowa City, IA'

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
    lat = Column(Float)
    lon = Column(Float)
    geocode_failed = Column(Boolean)

# Get database user and password from environmental variables
username = os.getenv("SCRAPY_DB_USER")
password = os.getenv("SCRAPY_DB_PASS")
api_key = os.getenv("GEOCODE_API_KEY")

db = create_engine('mysql+pymysql://%s:%s@127.0.0.1/ICPDLog?charset=utf8mb4' % (username, password), echo=False)

Base.metadata.create_all(db)
Session = sessionmaker()
Session.configure(bind=db)


def QueryForGeocode():
    # Query items without a lat or lon value
    session = Session()
    # Get Items with no lat or lon that havent been flagged as failed
    items = session.query(LogItem).filter_by(lat=None, geocode_failed=None).all()
    print("{} record(s) found needing geocoding".format(len(items)))

    return items


def UpdateRecordWithGeocode(item, lat: float, lon: float):
    session = Session()
    if lat == None or lon == None:
        item.geocode_failed = True
    else:
        item.lat = lat
        item.lon = lon
    # save the result to the database
    session.merge(item)
    session.commit()

# Takes output of QueryForGeocode()
def GeoCodeItems(items):
    counter = 1
    gmaps = googlemaps.Client(key=api_key)
    for item in items:
        print("Submitting item {}...".format(counter))
        target_address = ", ".join((item.addr, BASE_LOC))
        geocode_result = gmaps.geocode(target_address)
        if geocode_result:
            lat = geocode_result[0]['geometry']['location']['lat']
            lon = geocode_result[0]['geometry']['location']['lng']
        else:
            lat = None
            lon = None
        UpdateRecordWithGeocode(item, lat, lon)
        counter += 1


if __name__ == "__main__":
    items = QueryForGeocode()
    print("Beginning geocode....")
    GeoCodeItems(items)
    print("Complete")
