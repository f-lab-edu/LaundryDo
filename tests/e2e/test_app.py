import requests
import pytest
import config

# @pytest.mark.usefixtures('restart_api')
# def test_request_order(order_factory, clothes_factory, session) :


    # data = order_factory(clothes_list = [clothes_factory()])
    # url = config.get_api_url()
    # r = requests.post(f'{url}/orders', json = data)
    
    # assert r.json()





def test_view_order_history() :

    
    # # put order in db
    # order1 = order_factory()
    # order1.request_order(clothes_list = [clothes_factory() for _ in range(5)])
    # session.add(order1)
    # session.commit()


    pass

def test_cancel_order() :
    pass


def test_request_order_progress() :
    pass