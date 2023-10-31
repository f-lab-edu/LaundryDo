from sqlalchemy import Table, MetaData, Column, String, Float, Date, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import mapper, relationship, Session, sessionmaker
from fastapi import Depends
from src.application.unit_of_work import SqlAlchemyUnitOfWork
import config


settings = config.get_setting()

SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(
    settings.DB_USER,
    settings.DB_PASSWORD,
    settings.DB_HOST,
    settings.DB_PORT,
    settings.DB_DATABASE
)


SQLALCHEMY_ASYNC_DATABASE_URL = 'mysql+aiomysql://{}:{}@{}:{}/{}'.format(
    settings.DB_USER,
    settings.DB_PASSWORD,
    settings.DB_HOST,
    settings.DB_PORT,
    settings.DB_DATABASE
)

TEMPORARY_URL = 'sqlite:///./laundrydo.db'
engine = create_engine(SQLALCHEMY_DATABASE_URL) # only for sqlite

session = sessionmaker(autocommit = False, autoflush = False, bind = engine)


def get_db() :
    db = session()
    try :
        yield db
    finally :
        db.close()


def get_session() :
    return session


def get_uow(session_factory : Session = Depends(get_session)) : 
    return SqlAlchemyUnitOfWork(session_factory)