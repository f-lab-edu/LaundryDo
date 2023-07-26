import requests
from config import get_api_url


def post_to_request_order(userid) :
    url = get_api_url()
    r = requests.post(
        f"{url}/users/{userid}/orders/", 
        json = {}
)