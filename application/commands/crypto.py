import requests


def get_crypto_price(symbol, message):
    """Get crypto price for provided ticker label."""
    req = requests.get(url=message)
    prices = req.json()["result"]["price"]
    last = int(prices["last"])
    high = int(prices["high"])
    low = int(prices["low"])
    percentage = prices["change"]['percentage']*100
    percentage = '%.2f' % (percentage)
    symbol = symbol.upper()
    msg = f'{symbol}: Currently at ${last}. \
            High today of ${high}, low of ${low}. \
            Change of {percentage}%'
    return msg
