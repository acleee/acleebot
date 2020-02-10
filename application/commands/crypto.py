import requests


def get_crypto_price(symbol, message):
    """Get crypto price for provided ticker label."""
    req = requests.get(url=message)
    prices = req.json()["result"]["price"]
    last = prices["last"]
    high = prices["high"]
    low = prices["low"]
    percentage = prices["change"]['percentage']*100
    percentage = '%.2f' % (percentage)
    symbol = symbol.upper()
    msg = f'{symbol}: Currently at ${last:.2f}. \
            High today of ${high:.2f}, low of ${low:.2f}. \
            Change of {percentage}%'
    return msg
