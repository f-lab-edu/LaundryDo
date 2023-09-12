import uuid


def random_suffix():
    return uuid.uuid4().hex[:6]


def random_userid(name=""):
    return f"user-{name}-{random_suffix()}"


def random_laundrybagid(name=""):
    return f"laundrybag-{name}-{random_suffix()}-0" # <- number at the end indicates the index of laundrybag


def random_orderid(name=""):
    return f"order-{name}-{random_suffix()}"

def random_clothesid(name=""):
    return f"clothes-{name}-{random_suffix()}"
