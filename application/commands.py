import requests
from google.cloud import storage
from random import randint
from config import Config
from datetime import datetime
from nba_api.stats.static import teams
from nba_api.stats.endpoints import teamgamelog


def basic_message(message):
    """Send basic text message to room."""
    return message


def get_user_avatar(message, args):
    """Retrieve Chatango avatar for provided user."""
    name = str(args.lower())
    msg = f"http://fp.chatango.com/profileimg/{name[0]}/{name[1]}/{name}/full.jpg"
    return msg


def get_crypto_price(symbol, message):
    """Get crypto price for provided ticker label."""
    req = requests.get(url=message)
    prices = req.json()["result"]["price"]
    last = prices["last"]
    high = prices["high"]
    low = prices["low"]
    percentage = prices["change"]['percentage']*100
    if last > 1:
        msg = f'{symbol.upper()}: Currently at ${last:.2f}. \
                High today of ${high:.2f}, low of ${low:.2f}. \
                Change of {percentage:.2f}%'
    msg = f'{symbol.upper()}: Currently at ${last}. \
            High today of ${high}, low of ${low}. \
            Change of {percentage:.2f}%'
    return msg


def fetch_image_from_gcs(message):
    """Get a random image from Google Cloud Storage bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(Config.gcloudBucketName)
    images = bucket.list_blobs(prefix=message)
    image_list = [image.name for image in images if '.' in image.name]
    rand = randint(0, len(image_list) - 1)
    image = Config.gcloudBucketUrl + Config.gcloudBucketName + '/' + image_list[rand]
    return image


def giphy_image_search(searchTerm):
    """Giphy image search."""
    rand = randint(0, 20)
    params = {'api_key': Config.giphy_api_key,
              'q': searchTerm,
              'limit': 1,
              'offset': rand,
              'rating': 'R',
              'lang': 'en'}
    res = requests.get('https://api.giphy.com/v1/gifs/search', params=params)
    if len(res.json()['data']):
        image = res.json()['data'][0]['images']['original']['url']
        return image
    else:
        return 'image not found :('


def random_image(message):
    """Select a random image from response."""
    image_list = message.replace(' ', '').split(';')
    random_pic = image_list[randint(0, len(image_list)-1)]
    return random_pic


def random_subreddit_image(message):
    """Fetch a random image from latest posts in a subreddit."""
    headers = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET',
      'Access-Control-Allow-Headers': 'Content-Type',
      'Access-Control-Max-Age': '3600',
      'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }
    endpoint = message + 'new.json?sort=new'
    r = requests.get(endpoint, headers=headers)
    res = r.json()['data']['children']
    images = [image['preview']['images'][0]['source']['url'] for image in res if image.get('preview', None)]
    rand = randint(0, len(images) - 1)
    image = images[rand].split('?')[0]
    return image


def nba_team_score(message):
    """Get score of an NBA game."""
    team_id = teams.find_teams_by_full_name(message)[0].get('id')
    season = datetime.now().year
    season_type = 'Regular Season'
    game = teamgamelog.TeamGameLog(team_id, season, season_type)
    print(game.nba_response.__dict__)
    print(game.data_sets[0].__dict__)


def get_stock_price(symbol):
    """Get stock price by symbol."""
    params = {'token': Config.iex_api_key}
    req = requests.get(f'https://sandbox.iexapis.com/stable/stock/{symbol}/quote', params=params)
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


def urban_dictionary_defintion(word):
    """Fetch urban dictionary definition."""
    params = {'term': word}
    req = requests.get('http://api.urbandictionary.com/v0/define', params=params)
    if req.json().get('list'):
        definition = str(req.json()['list'][0].get('definition'))[0:300] + '...'
        example = str(req.json()['list'][0].get('example'))
        word = req.json()['list'][0]['word'].upper()
        if example:
            return f"{word}: {definition}. \n EXAMPLE: '{example}'"
        return f"{word}: {definition}"
    return 'word not found :('
