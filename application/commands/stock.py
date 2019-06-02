import requests


def get_stock_price(symbol):
    r = requests.get('https://api.iextrading.com/1.0/stock/'+ symbol + '/batch?types=quote')
    x = r.json()
    y = x["quote"]
    companyName = y["companyName"]
    open = str(y["open"])
    high = str(y["high"])
    low = str(y["low"])
    close = str(y["previousClose"])
    perc = y["changePercent"]*100
    if perc < 0:
        plusminus = "down"
        perc = perc*-1
    else:
        plusminus = "up"
    perc = round(perc, 2)
    pct = str(perc)
    last = str(y["latestPrice"])
    message = "%s (%s) : currently at $%s, last opened at $%s, closed yesterday at $%s, %s %s today." % (companyName, last, open, close, plusminus, pct)
    return message
