import os

from typing import Any
from sqlalchemy.engine.url import URL
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings) :
    DB_HOST : str
    DB_PORT: Any
    # DB_ROOT_PASSWORD : str
    DB_DATABASE : str
    DB_USER : str
    DB_PASSWORD : str

    class Config :
        env_file = '.env'

@lru_cache
def get_setting() :
    return Settings()


def get_db_url() :
    settings = Settings()
    # DB_USER:DB_PASSWORD@DB_HOST:DB_PORT/DB_DATABASE
    return f'mysql://{settings.DB_HOST}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_DATABASE}'


def get_api_url() :
    host = os.environ.get('API_HOST', 'localhost')
    port = 80 if host == 'localhost' else 5005
    return f"http://{host}:{port}"

# def get_db_url() :
#     host = os.environ.get('DB_HOST', 'localhost')
#     port = 3306 if host == 'localhost' else 33060
#     password = os.environ.get('DB_PASSWORD', 'test1234')
#     user, db_name = 'testuser', 'laundrydo'
#     return f'mysql://{user}:{password}@{host}:{port}/{db_name}'
