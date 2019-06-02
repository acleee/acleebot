import requests


def get_crypto_price(message):
    """Get crypto price for provided ticker label."""
    req = requests.get(url=message)
    x = req.json()
    y = x["result"]["price"]
    z = y["change"]
    last = str(y["last"])
    high = str(y["high"])
    low = str(y["low"])
    percentage = z["percentage"]*100
    msg = "Currently at $" + last \
        + ", high today of $" + high \
        + ", low of $" + low \
        + ", change of %.3f" % percentage + "%"
    return msg
