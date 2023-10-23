import os

from typing import Any
from sqlalchemy.engine.url import URL
# from pydantic_settings import BaseSettings
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()


class Settings :
    DB_HOST : str = os.getenv('DB_HOST', 'localhost')
    DB_PORT: Any = os.getenv('DB_PORT', 3306)
    DB_DATABASE : str = os.getenv('DB_DATABASE', 'laundrydo')
    DB_USER : str = os.getenv('DB_USER', 'test_user')
    DB_PASSWORD : str = os.getenv('DB_PASSWORD', 'test1234')


class APIConfigurations :
    title = 'LaundryDo'
    description = 'laundry service'
    version = '0.1'


@lru_cache
def get_setting() :
    return Settings()


def get_api_url() :
    host = os.environ.get('API_HOST', 'localhost')
    port = 80 if host == 'localhost' else 5005
    return f"http://{host}:{port}"

