import requests
from config import Config


def get_stock_price(symbol):
    params = {'token': Config.iex_api_key}
    req = requests.get('https://sandbox.iexapis.com/stable/stock/' + symbol + '/quote', params=params)
    if req.status_code == 200:
        price = req.json().get('latestPrice', None)
        company_name = req.json().get("companyName", None)
        if price and company_name:
            message = f"{company_name} current price of ${price:.2f}."
            change = req.json().get("ytdChange", None)
            if change:
                message = f"{message} Percent change of {change:.2f}"
            return message
    return f'There\'s no such company as {symbol} :@'
