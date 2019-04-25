# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, Column, Table, ForeignKey
from sqlalchemy import BigInteger, Integer, SmallInteger, String, Date, DateTime, Float, Boolean, Text, LargeBinary
from sqlalchemy.ext.declarative import declarative_base

from scrapy.utils.project import get_project_settings

Base = declarative_base()

def db_url():
    return get_project_settings().get('CONNECTION_STRING')

def db_connect():
    return create_engine(db_url())

def create_tables(engine):
    Base.metadata.create_all(engine)

def drop_tables(engine):
    Base.metadata.drop_all(engine)

#
# ActiveRecord Models
#

class Rental(Base):
    __tablename__ = 'rentals'

    id = Column(Integer, primary_key=True)
    first_crawl_at = Column(DateTime)
    first_seen_at = Column(DateTime)
    last_seen_at = Column(DateTime)
    off_market_at = Column(DateTime, nullable=True, default=None)

    url = Column(String(1024), index=True, unique=True)
    thumbnail_url = Column(String(1024))
    referrer_url = Column(String(1024))

    neighborhood_id = Column(Integer, index=True)
    neighborhood = Column(String(100), index=True)
    
    address = Column(String(100))
    city = Column(String(50))
    state = Column(String(2))
    zipcode = Column(String(5))
    latitude = Column(Float)
    longitude = Column(Float)

    price = Column(Integer)
    sqft = Column(Integer)
    bedrooms = Column(Integer)
    bathrooms = Column(Integer)

    pet_friendly = Column(Boolean)
    furnished = Column(Boolean)

#
# NEIGHBORHOODS
#

NEIGHBORHOOD_DATA = {
    # Los Angeles
    7205:   'Mid Wilshire',
    7214:   'Mid City',
    139752: 'Mid City West',
    182470: 'Pico-Robertson',
    189056: 'South Carthay',
    194747: 'Crestview',

    # Beverly Hill
    207809: 'North Doheny',
    205780: 'Southwest Doheny',
    208034: 'Southeast Doheny',
    207932: 'La Cienega Park',

    # West Hollywood
    205077: 'West Hollywood West',
}

NEIGHBORHOOD_GROUPS = [
    [0, 'Los Angeles',    [7205, 7214, 139752, 182470, 189056, 194747]],
    [1, 'Beverly Hills',  [207809, 205780, 208034, 207932]],
    [2, 'West Hollywood', [205077]],
]

class Neighborhood(object):
    @classmethod
    def all(cls):
        return [cls(nh_id) for nh_id in NEIGHBORHOOD_DATA.keys()]

    @classmethod
    def by_id(cls, nh_id):
        return cls(nh_id)

    def __init__(self, nh_id):
        name = NEIGHBORHOOD_DATA.get(nh_id)
        self.nh_id = nh_id
        self.name = name if name else '[Unknown]'

class NeighborhoodGroup(object):    
    @classmethod
    def all(cls):
        return [cls(ng[0]) for ng in NEIGHBORHOOD_GROUPS]

    def __init__(self, nhg_id):
        data = NEIGHBORHOOD_GROUPS[nhg_id]
        self.nhg_id = data[0]
        self.name = data[1]
        self.neighborhoods = [Neighborhood(nh_id) for nh_id in data[2]]
