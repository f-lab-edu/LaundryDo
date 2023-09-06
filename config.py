import os

from typing import Any
from sqlalchemy.engine.url import URL
# from pydantic_settings import BaseSettings
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()
# class Settings(BaseSettings) :
#     DB_HOST : str
#     DB_PORT: Any
#     # DB_ROOT_PASSWORD : str
#     DB_DATABASE : str
#     DB_USER : str
#     DB_PASSWORD : str

#     class Config :
#         env_file = '.env'

class Settings :
    DB_HOST : str = os.getenv('DB_HOST')
    DB_PORT: Any = os.getenv('DB_PORT')
    # DB_ROOT_PASSWORD : str
    DB_DATABASE : str = os.getenv('DB_DATABASE')
    DB_USER : str = os.getenv('DB_USER')
    DB_PASSWORD : str = os.getenv('DB_PASSWORD')


class APIConfigurations :
    title = 'LaundryDo'
    description = 'laundry service'
    version = '0.1'


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

