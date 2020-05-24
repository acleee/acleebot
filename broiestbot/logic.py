"""Bot commands."""
from random import randint
from datetime import datetime
from config import (GOOGLE_BUCKET_NAME,
                    GOOGLE_BUCKET_URL,
                    PLOTLY_USERNAME,
                    PLOTLY_API_KEY,
                    GIPHY_API_KEY,
                    IEX_API_TOKEN,
                    WEATHERSTACK_API_KEY,
                    ALPHA_VANTAGE_API_KEY,
                    RED_API_KEY)
import requests
import pandas as pd
import plotly.graph_objects as go
import chart_studio.plotly as py
import chart_studio
import emoji
import wikipediaapi
from imdb import IMDb, IMDbError
from broiestbot.services import gcs
from broiestbot.services.logging import logger
from nba_api.stats.static import teams
from nba_api.stats.endpoints import teamgamelog


chart_studio.tools.set_credentials_file(
    username=PLOTLY_USERNAME,
    api_key=PLOTLY_API_KEY
)


def basic_message(message):
    """Send basic text message to room."""
    return message


@logger.catch
def get_crypto_price(symbol, message):
    """Get crypto price for provided ticker label."""
    req = requests.get(url=message)
    prices = req.json()["result"]["price"]
    percentage = prices["change"]['percentage'] * 100
    if prices["last"] > 1:
        response = f'{symbol.upper()}: Currently at ${prices["last"]:.2f}. ' \
                   f'HIGH today of ${prices["high"]:.2f}, LOW of ${prices["low"]:.2f} ' \
                   f'(change of {percentage:.2f}%).'
    else:
        response = f'{symbol.upper()}: Currently at ${prices["last"]}. ' \
                   f'HIGH today of ${prices["high"]} LOW of ${prices["low"]} ' \
                   f'(change of {percentage:.2f}%).'
    return f'{response} {crypto_plotly_chart(symbol)}'


@logger.catch
def crypto_plotly_chart(symbol):
    """Generate 30-day crypto price chart."""
    params = {
        'function': 'DIGITAL_CURRENCY_DAILY',
        'symbol': symbol,
        'market': 'USD',
        'apikey': ALPHA_VANTAGE_API_KEY
    }
    r = requests.get('https://www.alphavantage.co/query', params=params)
    data = r.json()
    df = pd.DataFrame.from_dict(data['Time Series (Digital Currency Daily)'], orient='index')[:30]
    if df.empty is False:
        df = df.apply(pd.to_numeric)
        fig = go.Figure(data=[go.Candlestick(x=df.index,
                        open=df['1a. open (USD)'],
                        high=df['2a. high (USD)'],
                        low=df['3a. low (USD)'],
                        close=df['4a. close (USD)'])])
        fig.update_layout(xaxis_rangeslider_visible=False, title=symbol)
        chart = py.plot(
                fig,
                filename=symbol,
                auto_open=False,
                fileopt='overwrite',
                sharing='public'
            )
        chart_image = chart[:-1] + '.png'
        return chart_image
    return None


@logger.catch
def crypto_chart(symbol):
    """Generate 20-day crypto price chart."""
    params = {
        'function': 'DIGITAL_CURRENCY_DAILY',
        'symbol': symbol,
        'market': 'USD',
        'apikey': ALPHA_VANTAGE_API_KEY
    }
    r = requests.get('https://www.alphavantage.co/query', params=params)
    data = r.json()
    list_of_dics = data['Time Series (Digital Currency Daily)'].items()
    labels = []
    candle = []
    for k, v in list_of_dics[:20]:
        labels.append(k.split('2020-')[1])
        candle.append([int(v["3b. low (USD)"].split('.')[0]), int(v["2a. high (USD)"].split('.')[0])])
    img = ' https://quickchart.io/chart?bkg=white&width=500&height=300&format=png&c={type:%27bar%27,data:{labels:' + str(labels).replace(' ', '') + ',datasets:[{label:%27Price%27,data:' + str(candle).replace(' ', '') + '}]}}&.png'
    return img


@logger.catch
def fetch_image_from_gcs(message):
    """Get a random image from Google Cloud Storage bucket."""
    images = gcs.bucket.list_blobs(prefix=message)
    image_list = [image.name for image in images if '.' in image.name]
    rand = randint(0, len(image_list) - 1)
    image = GOOGLE_BUCKET_URL + GOOGLE_BUCKET_NAME + '/' + image_list[rand]
    return image


@logger.catch
def giphy_image_search(search_term):
    """Giphy image search."""
    rand = randint(0, 20)
    params = {'api_key': GIPHY_API_KEY,
              'q': search_term,
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


@logger.catch
def random_image(message):
    """Select a random image from response."""
    image_list = message.replace(' ', '').split(';')
    random_pic = image_list[randint(0, len(image_list) - 1)]
    return random_pic


def subreddit_image(message):
    """Fetch a random image from latest posts in a subreddit."""
    image = None
    images = []
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }
    endpoint = message + '?sort=new'
    r = requests.get(endpoint, headers=headers)
    results = r.json()['data']['children']
    try:
        images = [image['data']['secure_media']['oembed'].get('thumbnail_url') for image in results]
    except KeyError as e:
        logger.error(f'Reddit threw KeyError for `{message}`: {e}')
        raise e
    finally:
        images = list(filter(None, images))
        if bool(images):
            rand = randint(0, len(images) - 1)
            image = images[rand].split('?')[0]
        return image


@logger.catch
def nba_team_score(message):
    """Get score of an NBA game."""
    team_id = teams.find_teams_by_full_name(message)[0].get('id')
    season = datetime.now().year
    season_type = 'Regular Season'
    game = teamgamelog.TeamGameLog(team_id, season, season_type)


@logger.catch
def get_stock_price(symbol):
    """Get stock price by symbol."""
    params = {'token': IEX_API_TOKEN}
    req = requests.get(
        f'https://sandbox.iexapis.com/stable/stock/{symbol}/quote',
        params=params
    )
    if req.status_code == 200:
        price = req.json().get('latestPrice', None)
        company_name = req.json().get("companyName", None)
        if price and company_name:
            message = f"{company_name}: Current price of ${price:.2f}."
            change = req.json().get("ytdChange", None)
            if change:
                message = f"{message} Change of {change:.2f}%"
            return message
    return f'There\'s no such company as {symbol} :@'


@logger.catch
def stock_price_chart(symbol):
    """Get 30-day stock chart."""
    params = {'token': IEX_API_TOKEN, 'includeToday': 'true'}
    url = f'https://sandbox.iexapis.com/stable/stock/{symbol}/chart/1m/'
    r = requests.get(url, params=params)
    if r.status_code == 200:
        message = get_stock_price(symbol)
        stock_df = pd.read_json(r.content)
        if stock_df.empty is False:
            fig = go.Figure(data=[go.Candlestick(x=stock_df['date'],
                                                 open=stock_df['open'],
                                                 high=stock_df['high'],
                                                 low=stock_df['low'],
                                                 close=stock_df['close'])])
            fig.update_layout(xaxis_rangeslider_visible=False, title=message)
            chart = py.plot(
                fig,
                filename=symbol,
                auto_open=False,
                fileopt='overwrite',
                sharing='public'
            )
            chart_image = chart[:-1] + '.png'
            return f'{chart_image} {message}'
    return f'There\'s no such company as {symbol} :@'


@logger.catch
def urban_dictionary(word):
    """Fetch urban dictionary definition."""
    params = {'term': word}
    headers = {'Content-Type': 'broiestbot/json'}
    req = requests.get(
        'http://api.urbandictionary.com/v0/define',
        params=params,
        headers=headers
    )
    results = req.json()['list']
    results = sorted(results, key=lambda i: i['thumbs_down'], reverse=True)
    definition = str(results[0].get('definition'))
    example = str(results[0].get('example'))
    word = word.upper()
    return f"{word}: {definition}. EXAMPLE: {example}."


@logger.catch
def weather_by_city(city, weather):
    """Return temperature and weather per city/state/zip."""
    endpoint = 'http://api.weatherstack.com/current'
    params = {'access_key': WEATHERSTACK_API_KEY,
              'query': city,
              'units': 'f'}
    r = requests.get(endpoint, params=params)
    data = r.json()
    code = data["current"]["weather_code"]
    weather_emoji = weather.find_row(code).get('icon')
    if weather_emoji:
        weather_emoji = emoji.emojize(weather_emoji, use_aliases=True)
    response = f'{data["request"]["query"]}: \
                 {weather_emoji} {data["current"]["weather_descriptions"][0]}. \
                 {data["current"]["temperature"]}°f \
                 (feels like {data["current"]["feelslike"]}°f). \
                 {data["current"]["precip"]}% precipitation.'
    return response


@logger.catch
def wiki_summary(msg):
    """Fetch Wikipedia summary for a given query."""
    wiki = wikipediaapi.Wikipedia('en')
    page = wiki.page(msg)
    return page.summary


@logger.catch
def find_imdb_movie(movie_title):
    """Get movie information from IMDB."""
    ia = IMDb()
    movie_id = None
    try:
        movies = ia.search_movie(movie_title)
        movie_id = movies[0].getID()
    except IMDbError as e:
        logger.error(f'IMDB command threw error for command `{movie_title}`: {e}')
    if movie_id:
        movie = ia.get_movie(movie_id)
        cast = f"STARRING {', '.join([actor['name'] for actor in movie.data['cast'][:2]])}."
        art = movie.data.get('cover url', None)
        director = f"DIRECTED by {movie.data.get('director')[0].get('name')}."
        year = movie.data.get('year')
        genres = f"({', '.join(movie.data.get('genres'))}, {year})."
        title = f"{movie.data.get('title').upper()},"
        rating = f"{movie.data.get('rating')}/10"
        boxoffice = get_boxoffice_data(movie)
        synopsis = movie.data.get('synopsis')
        if synopsis:
            synopsis = synopsis[0].split('. ')[:2]
        response = ' '.join(filter(None, [title, rating, genres, cast, director, synopsis, boxoffice, art]))
        return response


@logger.catch
def get_boxoffice_data(movie):
    """Get IMDB box office performance for a given film."""
    if movie.data.get('box office', None):
        budget = f"BUDGET {movie.data['box office'].get('Budget', None)}."
        opening_week = f"OPENING WEEK {movie.data['box office'].get('Opening Weekend United States', None)}."
        gross = f"CUMULATIVE WORLDWIDE GROSS {movie.data['box office'].get('Cumulative Worldwide Gross', None)}.)"
        return ' ' .join([budget, opening_week, gross])
    return None


@logger.catch
def get_gfycat_gif(query, custom_query=False):
    """Fetch specific kind of gif."""
    if custom_query:
        index_range = randint(0, 35)
    else:
        index_range = randint(0, 200)
    endpoint = 'https://napi.redgifs.com/v1/gfycats/search'
    params = {
        'search_text': query,
        'count': 1,
        'start': index_range
    }
    headers = {
        'Authorization': f'Bearer {RED_API_KEY}'
    }
    r = requests.get(endpoint, params=params, headers=headers)
    result = r.json()['gfycats'][0]
    image = result.get('max5mbGif')
    return image

