from sqlalchemy import Table, MetaData, Column, String, Float, Date, ForeignKey
from sqlalchemy.orm import mapper, relationship

metadata = MetaData()







from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DB_URL = 'sqlite:///./test.db'
engine = create_engine(DB_URL, connect_args = {'check_same_thread' : False})
session = sessionmaker(bind = engine)













