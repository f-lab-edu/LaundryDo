import os

def get_api_url() :
    host = os.environ.get('API_HOST', 'localhost')
    port = 80 if host == 'localhost' else 5005
    return f"http://{host}:{port}"