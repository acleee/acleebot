import requests
from config import Config


def get_stock_price(symbol):
    params = {'token': Config.iex_api_key}
    req = requests.get('https://sandbox.iexapis.com/stable/stock/' + symbol + '/quote', params=params)
    if req.status_code == 200:
        price = req.json().get('latestPrice', None)
        company_name = req.json().get("companyName", None)
        # high = req.json()["high"]
        # low = req.json()["low"]
        if price and company_name:
            change = round(req.json()["ytdChange"], 2)
            price = round(price, 2)
            message = f"{company_name} current price of ${price}. Percent change of {change}"
            return message
    return f'There\'s no such company as {symbol} :@'
