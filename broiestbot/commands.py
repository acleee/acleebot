"""Bot commands."""
from typing import Optional
from random import randint
from datetime import datetime
import requests
import pandas as pd
import plotly.graph_objects as go
import chart_studio.plotly as py
import chart_studio
import emoji
import wikipediaapi
from imdb import IMDb, IMDbError
from nba_api.stats.static import teams
from nba_api.stats.endpoints import teamgamelog
from config import (
    GOOGLE_BUCKET_NAME,
    GOOGLE_BUCKET_URL,
    PLOTLY_USERNAME,
    PLOTLY_API_KEY,
    GIPHY_API_KEY,
    WEATHERSTACK_API_KEY,
    GFYCAT_CLIENT_ID,
    GFYCAT_CLIENT_SECRET,
    REDGIFS_ACCESS_KEY
)
from broiestbot.clients import gcs, sch, cch
from broiestbot.clients.logging import logger
from broiestbot.afterdark import is_after_dark


chart_studio.tools.set_credentials_file(
    username=PLOTLY_USERNAME,
    api_key=PLOTLY_API_KEY
)


def basic_message(message):
    """Send basic text message to room."""
    return message


def get_crypto(symbol):
    """Fetch crypto price and generate 60-day performance chart."""
    chart = cch.get_chart(symbol)
    return chart


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
    return 'image not found :('


@logger.catch
def random_image(message):
    """Select a random image from response."""
    image_list = message.replace(' ', '').split(';')
    random_pic = image_list[randint(0, len(image_list) - 1)]
    return random_pic


def subreddit_image(message):
    """Fetch a random image from latest posts in a subreddit."""
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }
    endpoint = message + '?sort=new'
    req = requests.get(endpoint, headers=headers)
    results = req.json()['data']['children']
    images = [image['data']['secure_media']['oembed'].get('thumbnail_url') for image in results]
    images = list(filter(None, images))
    if bool(images):
        rand = randint(0, len(images) - 1)
        image = images[rand].split('?')[0]
        return image
    return 'No images found bc reddit SUCKS.'


@logger.catch
def nba_team_score(message):
    """Get score of an NBA game."""
    team_id = teams.find_teams_by_full_name(message)[0].get('id')
    season = datetime.now().year
    season_type = 'Regular Season'
    game = teamgamelog.TeamGameLog(team_id, season, season_type)


def get_stock(symbol):
    """Fetch stock price and generate 30-day performance chart."""
    chart = sch.get_chart(symbol)
    return chart


@logger.catch
def get_urban_definition(word) -> Optional[str]:
    """Fetch UrbanDictionary word definition."""
    params = {'term': word}
    headers = {'Content-Type': 'application/json'}
    req = requests.get(
        'http://api.urbandictionary.com/v0/define',
        params=params,
        headers=headers
    )
    results = req.json().get('list')
    if results:
        results = sorted(results, key=lambda i: i['thumbs_down'], reverse=True)
        definition = str(results[0].get('definition'))
        example = str(results[0].get('example'))
        word = word.upper()
        return f"{word}: {definition}. EXAMPLE: {example}."
    return None


@logger.catch
def weather_by_city(city, weather):
    """Return temperature and weather per city/state/zip."""
    endpoint = 'http://api.weatherstack.com/current'
    params = {'access_key': WEATHERSTACK_API_KEY,
              'query': city,
              'units': 'f'}
    req = requests.get(endpoint, params=params)
    data = req.json()
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
            try:
                synopsis = synopsis[0]
                synopsis = ' '.join(synopsis[0].split('. ')[:2])
            except KeyError as e:
                logger.error(f'IMDB movie `{title}` does not have a synopsis: {e}')
        response = ' '.join(filter(None, [title, rating, genres, cast, director, synopsis, boxoffice, art]))
        return response
    return None


@logger.catch
def get_boxoffice_data(movie):
    """Get IMDB box office performance for a given film."""
    response = []
    if movie.data.get('box office', None):
        budget = movie.data['box office'].get('Budget', None)
        opening_week = movie.data['box office'].get('Opening Weekend United States', None)
        gross = movie.data['box office'].get('Cumulative Worldwide Gross', None)
        if budget:
            response.append(f"BUDGET {budget}.")
        if opening_week:
            response.append(f"OPENING WEEK {opening_week}.")
        if gross:
            response.append(f"CUMULATIVE WORLDWIDE GROSS {gross}.")
        return ' ' .join(response)
    return None


@logger.catch
def get_redgifs_gif(query, after_dark_only=False):
    """Fetch specific kind of gif."""
    night_mode = is_after_dark()
    if (after_dark_only and night_mode) or after_dark_only is False:
        token = redgifs_auth_token()
        endpoint = 'https://napi.redgifs.com/v1/gfycats/search'
        params = {
            'search_text': query,
            'count': 100,
            'start': 0
        }
        headers = {
            'Authorization': f'Bearer {token}'
        }
        req = requests.get(endpoint, params=params, headers=headers)
        results = req.json()['gfycats']
        rand = randint(0, len(results) - 1)
        image_json = results[rand]
        image = image_json.get('max5mbGif')
        return image
    return 'https://i.imgur.com/oGMHkqT.jpg'


@logger.catch
def gfycat_auth_token():
    """Get auth token."""
    endpoint = 'https://api.gfycat.com/v1/oauth/token'
    body = {
        "grant_type": "client_credentials",
        "client_id": GFYCAT_CLIENT_ID,
        "client_secret": GFYCAT_CLIENT_SECRET
        }
    headers = {'Content-Type': 'application/json'}
    req = requests.post(endpoint, json=body, headers=headers)
    if req.status_code == 200:
        return req.json()['access_token']
    return None


def redgifs_auth_token():
    """Get redgifs auth via webtoken method."""
    endpoint = 'https://weblogin.redgifs.com/oauth/webtoken'
    body = {"access_key": REDGIFS_ACCESS_KEY}
    headers = {'Content-Type': 'application/json'}
    req = requests.post(endpoint, json=body, headers=headers)
    if req.status_code == 200:
        return req.json()['access_token']
    return None
