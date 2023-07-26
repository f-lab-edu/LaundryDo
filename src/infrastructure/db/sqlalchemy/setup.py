from sqlalchemy import Table, MetaData, Column, String, Float, Date, ForeignKey
from sqlalchemy.orm import mapper, relationship

metadata = MetaData()



import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

settings = config.get_setting()
SQLALCHEMY_DATABASE_URL = 'mysql://{}:{}@{}:{}/{}'.format(
    settings.DB_USER,
    settings.DB_PASSWORD,
    settings.DB_HOST,
    settings.DB_PORT,
    settings.DB_DATABASE
)


# DB_URL = 'sqlite:///./test.db'
engine = create_engine(SQLALCHEMY_DATABASE_URL) #  connect_args = {'check_same_thread' : False} only for sqlite

session = sessionmaker(autocommit = False, autoflush = False, bind = engine)


# def session_factory(engine = engine) :
#     start_mappers()
#     yield sessionmaker(bind = engine)










