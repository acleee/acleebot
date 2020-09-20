"""Bot commands."""
from typing import Optional
from random import randint
from datetime import datetime
import requests
from requests.exceptions import HTTPError
import chart_studio
import emoji
import wikipediaapi
from imdb import IMDb, IMDbError
import praw
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
    REDGIFS_ACCESS_KEY,
    REDDIT_CLIENT_ID,
    REDDIT_CLIENT_SECRET,
    REDDIT_PASSWORD
)
from broiestbot.clients import gcs, sch, cch
from broiestbot.logging import LOGGER
from broiestbot.afterdark import is_after_dark


reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    username='broiestbro',
    password=REDDIT_PASSWORD,
    user_agent="bot"
)


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


@LOGGER.catch
def fetch_image_from_gcs(message):
    """Get a random image from Google Cloud Storage bucket."""
    images = gcs.bucket.list_blobs(prefix=message)
    image_list = [image.name for image in images if '.' in image.name]
    rand = randint(0, len(image_list) - 1)
    image = GOOGLE_BUCKET_URL + GOOGLE_BUCKET_NAME + '/' + image_list[rand]
    return image


@LOGGER.catch
def giphy_image_search(search_term) -> Optional[str]:
    """Giphy image search."""
    rand = randint(0, 20)
    params = {
        'api_key': GIPHY_API_KEY,
        'q': search_term,
        'limit': 1,
        'offset': rand,
        'rating': 'R',
        'lang': 'en',
    }
    try:
        res = requests.get('https://api.giphy.com/v1/gifs/search', params=params)
        if len(res.json()['data']):
            image = res.json()['data'][0]['images']['original']['url']
            return image
        return 'image not found :('
    except HTTPError as e:
        LOGGER.error(f'Giphy failed to fetch `{search_term}`: {e.response.content}')
    LOGGER.warning(f'No results found for `{search_term}`.')
    return None


@LOGGER.catch
def random_image(message) -> Optional[str]:
    """Select a random image from response."""
    image_list = message.replace(' ', '').split(';')
    random_pic = image_list[randint(0, len(image_list) - 1)]
    return random_pic


@LOGGER.catch
def subreddit_image(subreddit: str) -> Optional[str]:
    """Fetch a random image from latest posts in a subreddit."""
    images = [post for post in reddit.subreddit(subreddit).new(limit=10)]
    LOGGER.info(images)


@LOGGER.catch
def nba_team_score(message):
    """Get score of an NBA game."""
    team_id = teams.find_teams_by_full_name(message)[0].get('id')
    season = datetime.now().year
    season_type = 'Regular Season'
    game = teamgamelog.TeamGameLog(team_id, season, season_type)
    LOGGER.info(game)


def get_stock(symbol):
    """Fetch stock price and generate 30-day performance chart."""
    chart = sch.get_chart(symbol)
    return chart


@LOGGER.catch
def get_urban_definition(word) -> Optional[str]:
    """Fetch UrbanDictionary word definition."""
    params = {'term': word}
    headers = {'Content-Type': 'application/json'}
    try:
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
    except HTTPError as e:
        LOGGER.error(f'Failed to get Urban definition for `{word}`: {e.response.content}')
    LOGGER.warning(f'No definitions found for `{word}`.')
    return None


@LOGGER.catch
def weather_by_city(city, weather) -> Optional[str]:
    """Return temperature and weather per city/state/zip."""
    endpoint = 'http://api.weatherstack.com/current'
    params = {
        'access_key': WEATHERSTACK_API_KEY,
        'query': city,
        'units': 'f'
    }
    try:
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
    except HTTPError as e:
        LOGGER.error(f'Failed to get weather for `{city}`: {e.response.content}')
    LOGGER.warning(f'No weather found for `{city}`.')
    return None


@LOGGER.catch
def wiki_summary(msg):
    """Fetch Wikipedia summary for a given query."""
    wiki = wikipediaapi.Wikipedia('en')
    page = wiki.page(msg)
    return page.summary


@LOGGER.catch
def find_imdb_movie(movie_title) -> Optional[str]:
    """Get movie information from IMDB."""
    ia = IMDb()
    movie_id = None
    try:
        movies = ia.search_movie(movie_title)
        movie_id = movies[0].getID()
    except IMDbError as e:
        LOGGER.error(f'IMDB failed to find `{movie_title}`: {e}')
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
                LOGGER.error(f'IMDB movie `{title}` does not have a synopsis: {e}')
        response = ' '.join(filter(None, [title, rating, genres, cast, director, synopsis, boxoffice, art]))
        return response
    LOGGER.warning(f'No IMDB info found for `{movie_title}`.')
    return None


@LOGGER.catch
def get_boxoffice_data(movie) -> Optional[str]:
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
    LOGGER.warning(f'No IMDB box office info found for `{movie}`.')
    return None


@LOGGER.catch
def get_redgifs_gif(query, after_dark_only=False) -> str:
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
        try:
            req = requests.get(endpoint, params=params, headers=headers)
            if bool(req.json()):
                results = req.json()['gfycats']
                rand = randint(0, len(results) - 1)
                image_json = results[rand]
                image = image_json.get('max5mbGif')
                return image
            return f'Sorry bruh I couldnt find any images for ur dumb ass query LEARN2SEARCH :@'
        except HTTPError as e:
            LOGGER.error(f'Failed to get nsfw image for `{query}`: {e.response.content}')
    return 'https://i.imgur.com/oGMHkqT.jpg'


@LOGGER.catch
def gfycat_auth_token() -> Optional[str]:
    """Get auth token."""
    endpoint = 'https://api.gfycat.com/v1/oauth/token'
    body = {
        "grant_type": "client_credentials",
        "client_id": GFYCAT_CLIENT_ID,
        "client_secret": GFYCAT_CLIENT_SECRET
        }
    headers = {'Content-Type': 'application/json'}
    try:
        req = requests.post(endpoint, json=body, headers=headers)
        if req.status_code == 200:
            return req.json().get('access_token')
    except HTTPError as e:
        LOGGER.error(f'Failed to get gfycat auth token: {e.response.content}')
    LOGGER.warning(f'No auth token received for gfycat request.')
    return None

1
@LOGGER.catch
def redgifs_auth_token() -> Optional[str]:
    """Get redgifs auth via webtoken method."""
    endpoint = 'https://weblogin.redgifs.com/oauth/webtoken'
    body = {"access_key": REDGIFS_ACCESS_KEY}
    headers = {'Content-Type': 'application/json'}
    try:
        req = requests.post(endpoint, json=body, headers=headers)
        if req.status_code == 200:
            return req.json()['access_token']
    except HTTPError as e:
        LOGGER.error(f'Failed to get redgifs auth token: {e.response.content}')
    LOGGER.warning(f'No auth token received for redgifs request.')
    return None
