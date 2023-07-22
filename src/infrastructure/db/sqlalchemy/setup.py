from sqlalchemy import Table, MetaData, Column, String, Float, Date, ForeignKey
from sqlalchemy.orm import mapper, relationship

metadata = MetaData()



import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# DB_URL = 'sqlite:///./test.db'
engine = create_engine(config.DB_URL,) #  connect_args = {'check_same_thread' : False} only for sqlite
session = sessionmaker(bind = engine)













