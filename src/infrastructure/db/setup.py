from sqlalchemy import Table, MetaData, Column, String, Float, Date, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import mapper, relationship, Session, sessionmaker
import config


settings = config.get_setting()
# SQLALCHEMY_DATABASE_URL = 'mysql://{}:{}@{}:{}/{}'.format(
#     settings.DB_USER,
#     settings.DB_PASSWORD,
#     settings.DB_HOST,
#     settings.DB_PORT,
#     settings.DB_DATABASE
# )

SQLALCHEMY_DATABASE_URL = 'mysql://{}:{}/{}'.format(
    'localhost', # settings.DB_HOST,
    settings.DB_PORT,
    settings.DB_DATABASE
)

# DB_URL = 'sqlite:///./test.db'
TEMPORARY_LOCAL_URL = 'sqlite:///./laundrydo.db'
# print('DB ADDRESS :', SQLALCHEMY_DATABASE_URL)
engine = create_engine(TEMPORARY_LOCAL_URL, connect_args = {'check_same_thread' : False}, pool_size = 20, echo_pool = 'debug') # only for sqlite

session = sessionmaker(autocommit = False, autoflush = False, bind = engine)


def get_db() :
    db = session()
    try :
        yield db
    finally :
        db.close()


def get_session() :
    return session



