import requests
from config import iex_api_key


def get_stock_price(symbol):
    params = {'token': iex_api_key}
    req = requests.get('https://sandbox.iexapis.com/stable/stock/' + symbol + '/quote', params=params)
    print(req.status_code)
    if req.status_code == 200:
        price = req.json()['latestPrice']
        companyName = req.json()["companyName"]
        high = req.json()["high"]
        low = req.json()["low"]
        change = round(req.json()["ytdChange"], 4)
        message = f"{companyName} current price of ${price}. Percent change of {change}"
        return message
    return f'theres no such company as {symbol} :@'
