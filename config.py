import os
from sqlalchemy.engine.url import URL

def get_api_url() :
    host = os.environ.get('API_HOST', 'localhost')
    port = 80 if host == 'localhost' else 5005
    return f"http://{host}:{port}"

DB_URL = str(URL.create(
    "mysql",
    username="user",
    port = '3306',
    password="test1234",  # plain (unescaped) text
    host="localhost",
    database="db",
))

