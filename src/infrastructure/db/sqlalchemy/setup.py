from sqlalchemy import Table, MetaData, Column, String, Float, Date, ForeignKey
from sqlalchemy.orm import mapper, relationship

metadata = MetaData()







from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///:memory')
session = sessionmaker(bind = engine)













