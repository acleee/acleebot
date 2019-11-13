import requests


def get_crypto_price(message):
    """Get crypto price for provided ticker label."""
    req = requests.get(url=message)
    prices = req.json()["result"]["price"]
    last = prices["last"]
    high = prices["high"]
    low = prices["low"]
    percentage = prices["change"]['percentage']*100
    msg = "Currently at $" + last \
        + ", high today of $" + high \
        + ", low of $" + low \
        + ", change of %.3f" % percentage + "%"
    return msg
