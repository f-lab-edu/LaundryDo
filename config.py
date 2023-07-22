import os
from sqlalchemy.engine.url import URL

def get_api_url() :
    host = os.environ.get('API_HOST', 'localhost')
    port = 80 if host == 'localhost' else 5005
    return f"http://{host}:{port}"

def get_db_url() :
    host = os.environ.get('DB_HOST', 'localhost')
    port = 3306 if host == 'localhost' else 33060
    password = os.environ.get('DB_PASSWORD', 'test1234')
    user, db_name = 'testuser', 'laundrydo'
    return f'mysql://{user}:{password}@{host}:{port}/{db_name}'

DB_URL = get_db_url()