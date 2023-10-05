from sqlalchemy import Table, MetaData, Column, String, Float, Date, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import mapper, relationship, Session, sessionmaker, declarative_base
import config


settings = config.get_setting()
SQLALCHEMY_DATABASE_URL = 'mysql://{}:{}@{}:{}/{}'.format(
    settings.DB_USER,
    settings.DB_PASSWORD,
    settings.DB_HOST,
    settings.DB_PORT,
    settings.DB_DATABASE
)

# DB_URL = 'sqlite:///./test.db'
TEMPORARY_LOCAL_URL = 'sqlite:///./laundrydo.db'
SQLALCHEMY_DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL) #  connect_args = {'check_same_thread' : False} only for sqlite

session = sessionmaker(autocommit = False, autoflush = False, bind = engine)


def get_db() :
    db = session()
    try :
        yield db
    finally :
        db.close()


def get_session() :
    return session



