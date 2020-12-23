"""Construct responses from third-party APIs."""
from datetime import datetime
from random import randint
from typing import Optional

import chart_studio
import pytz
import requests
from bs4 import BeautifulSoup
from emoji import emojize
from imdb import IMDbError
from praw.exceptions import RedditAPIException
from requests import Response
from requests.exceptions import HTTPError

from broiestbot.afterdark import is_after_dark
from clients import cch, gcs, ia, reddit, sch, wiki
from config import (
    GFYCAT_CLIENT_ID,
    GFYCAT_CLIENT_SECRET,
    GIPHY_API_KEY,
    GOOGLE_BUCKET_NAME,
    GOOGLE_BUCKET_URL,
    INSTAGRAM_APP_ID,
    PLOTLY_API_KEY,
    PLOTLY_USERNAME,
    REDGIFS_ACCESS_KEY,
    WEATHERSTACK_API_KEY,
)
from logger import LOGGER

# Plotly
chart_studio.tools.set_credentials_file(
    username=PLOTLY_USERNAME, api_key=PLOTLY_API_KEY
)


def basic_message(message):
    """Send basic text message to room."""
    return message


def get_crypto(symbol) -> Optional[str]:
    """Fetch crypto price and generate 60-day performance chart."""
    try:
        chart = cch.get_chart(symbol)
        return chart
    except HTTPError as e:
        LOGGER.error(e)
    except Exception as e:
        LOGGER.error(e)
    return None


@LOGGER.catch
def fetch_image_from_gcs(message) -> str:
    """Get a random image from Google Cloud Storage bucket."""
    images = gcs.bucket.list_blobs(prefix=message)
    image_list = [image.name for image in images if "." in image.name]
    rand = randint(0, len(image_list) - 1)
    image = GOOGLE_BUCKET_URL + GOOGLE_BUCKET_NAME + "/" + image_list[rand]
    return image


@LOGGER.catch
def giphy_image_search(search_term: str) -> Optional[str]:
    """Giphy image search."""
    rand = randint(0, 20)
    params = {
        "api_key": GIPHY_API_KEY,
        "q": search_term,
        "limit": 1,
        "offset": rand,
        "rating": "R",
        "lang": "en",
    }
    try:
        req = requests.get("https://api.giphy.com/v1/gifs/search", params=params)
        if req.status_code != 200:
            return "image not found :("
        image = req.json()["data"][0]["images"]["original"]["url"]
        return image
    except HTTPError as e:
        LOGGER.error(f"Giphy failed to fetch `{search_term}`: {e.response.content}")
        return emojize(
            f":warning: i broke bc im a shitty bot :warning:", use_aliases=True
        )
    except KeyError as e:
        LOGGER.error(f"Giphy KeyError for `{search_term}`: {e}")
        return emojize(
            f":warning: i broke bc im a shitty bot :warning:", use_aliases=True
        )
    except Exception as e:
        LOGGER.error(f"Giphy unexpected error for `{search_term}`: {e}")
        return emojize(
            f":warning: i broke bc im a shitty bot :warning:", use_aliases=True
        )


def random_image(message: str) -> Optional[str]:
    """
    Randomly select a response from a given set.

    :param message: Query matching a command to set a random image from a set.
    :type message: str

    :returns: Optional[str]
    """
    try:
        image_list = message.replace(" ", "").split(";")
        random_pic = image_list[randint(0, len(image_list) - 1)]
        return random_pic
    except KeyError as e:
        LOGGER.warning(f"Error when fetching random image: {e}")
        return None
    except Exception as e:
        LOGGER.warning(f"Unexpected error when fetching random image: {e}")
        return None


def subreddit_image(subreddit: str) -> Optional[str]:
    """Fetch a recently posted image from a subreddit."""
    try:
        images = [post for post in reddit.subreddit(subreddit).new(limit=10)]
        if images:
            return images[0]
    except RedditAPIException as e:
        LOGGER.error(f"Reddit image search failed for subreddit `{subreddit}`: {e}")
        return emojize(
            f":warning: i broke bc im a shitty bot :warning:", use_aliases=True
        )
    except Exception as e:
        LOGGER.error(f"Unexpected error when Reddit searching for `{subreddit}`: {e}")
        return emojize(
            f":warning: i broke bc im a shitty bot :warning:", use_aliases=True
        )


def get_stock(symbol: str) -> Optional[str]:
    """Fetch stock price and generate 30-day performance chart."""
    try:
        chart = sch.get_chart(symbol)
        return chart
    except HTTPError as e:
        LOGGER.error(e)
        return None
    except Exception as e:
        LOGGER.error(e)
        return None


@LOGGER.catch
def get_urban_definition(word: str) -> Optional[str]:
    """Fetch Urban Dictionary definition."""
    params = {"term": word}
    headers = {"Content-Type": "application/json"}
    try:
        req = requests.get(
            "http://api.urbandictionary.com/v0/define", params=params, headers=headers
        )
        results = req.json().get("list")
        if results:
            results = sorted(results, key=lambda i: i["thumbs_down"], reverse=True)
            definition = str(results[0].get("definition"))[0:1500].replace("[", "").replace("]", "")
            example = str(results[0].get("example")).replace("[", "").replace("]", "")
            word = word.upper()
            return f"{word}:\n\n {definition} \n\n EXAMPLE: {example}."
    except HTTPError as e:
        LOGGER.error(
            f"Failed to get Urban definition for `{word}`: {e.response.content}"
        )
        return None
    except Exception as e:
        LOGGER.error(
            f"Unexpected error when fetching Urban definition for `{word}`: {e}"
        )
        return None
    return emojize(
        ":warning: idk wtf ur trying to search for tbh :warning:", use_aliases=True
    )


def weather_by_city(location: str, weather) -> Optional[str]:
    """Return temperature and weather per city/state/zip."""
    endpoint = "http://api.weatherstack.com/current"
    params = {
        "access_key": WEATHERSTACK_API_KEY,
        "query": location.replace(";", ""),
        "units": "f",
    }
    try:
        req = requests.get(endpoint, params=params)
        data = req.json()
        if data.get("success") is False:
            LOGGER.error(
                f'Failed to get weather for `{location}`: {data["error"]["info"]}'
            )
            return emojize(
                f":warning:️️ wtf even is `{location}` :warning:", use_aliases=True
            )
        if req.status_code == 200 and data.get("current"):
            weather_code = data["current"]["weather_code"]
            weather_emoji = weather.find_row("code", weather_code).get("icon")
            if weather_emoji:
                weather_emoji = emojize(weather_emoji, use_aliases=True)
            response = f'{data["request"]["query"]}: \
                            {weather_emoji} {data["current"]["weather_descriptions"][0]}. \
                            {data["current"]["temperature"]}°f \
                            (feels like {data["current"]["feelslike"]}°f). \
                            {data["current"]["precip"] * 100}% precipitation.'
            return response
    except HTTPError as e:
        LOGGER.error(f"Failed to get weather for `{location}`: {e.response.content}")
        return emojize(
            f":warning:️️ omfg u broke the bot WHAT DID YOU DO IM DEAD AHHHHHH :warning:",
            use_aliases=True,
        )
    except KeyError as e:
        LOGGER.error(f"KeyError while fetching weather for `{location}`: {e}")
        return emojize(
            f":warning:️️ omfg u broke the bot WHAT DID YOU DO IM DEAD AHHHHHH :warning:",
            use_aliases=True,
        )
    except Exception as e:
        LOGGER.error(f"Failed to get weather for `{location}`: {e}")
        return emojize(
            f":warning:️️ omfg u broke the bot WHAT DID YOU DO IM DEAD AHHHHHH :warning:",
            use_aliases=True,
        )


@LOGGER.catch
def wiki_summary(query: str) -> str:
    """
    Fetch Wikipedia summary for a given query.

    :param query: Query to fetch corresponding Wikipedia page.
    :type query: str

    :returns: str
    """
    try:
        wiki_page = wiki.page(query)
        if wiki_page.exists():
            return f"{wiki_page.title.upper()}: {wiki_page.summary[0:1500]}"
        return emojize(
            f":warning: bruh i couldnt find shit for `{query}` :warning:",
            use_aliases=True,
        )
    except Exception as e:
        LOGGER.error(f"Unexpected error while fetching wiki summary for `{query}`: {e}")
        return emojize(
            f":warning: BRUH YOU BROKE THE BOT WTF IS `{query}`?! :warning:",
            use_aliases=True,
        )


@LOGGER.catch
def find_imdb_movie(movie_title: str) -> Optional[str]:
    """Get movie information from IMDB."""
    try:
        movies = ia.search_movie(movie_title)
        if bool(movies):
            movie_id = movies[0].getID()
            movie = ia.get_movie(movie_id)
            if movie:
                cast = f"STARRING {', '.join([actor['name'] for actor in movie.data['cast'][:2]])}."
                art = movie.data.get("cover url", None)
                director = movie.data.get("director")
                if director:
                    director = (
                        f"DIRECTED by {movie.data.get('director')[0].get('name')}."
                    )
                year = movie.data.get("year")
                genres = f"({', '.join(movie.data.get('genres'))}, {year})."
                title = f"{movie.data.get('title').upper()},"
                rating = f"{movie.data.get('rating')}/10"
                boxoffice = get_boxoffice_data(movie)
                synopsis = movie.data.get("synopsis")
                if synopsis:
                    try:
                        synopsis = synopsis[0]
                        synopsis = " ".join(synopsis[0].split(". ")[:2])
                    except KeyError as e:
                        LOGGER.error(
                            f"IMDB movie `{title}` does not have a synopsis: {e}"
                        )
                response = " ".join(
                    filter(
                        None,
                        [
                            title,
                            rating,
                            genres,
                            cast,
                            director,
                            synopsis,
                            boxoffice,
                            art,
                        ],
                    )
                )
                return response
            LOGGER.warning(f"No IMDB info found for `{movie_title}`.")
            return emojize(
                f":warning: wtf kind of movie is {movie} :warning:", use_aliases=True
            )
    except IMDbError as e:
        LOGGER.error(f"IMDB failed to find `{movie_title}`: {e}")
        return None
    except Exception as e:
        LOGGER.error(f"Unexpected error while fetching IMDB movie `{movie_title}`: {e}")
        return None


@LOGGER.catch
def get_boxoffice_data(movie) -> Optional[str]:
    """Get IMDB box office performance for a given film."""
    response = []
    if movie.data.get("box office", None):
        budget = movie.data["box office"].get("Budget", None)
        opening_week = movie.data["box office"].get(
            "Opening Weekend United States", None
        )
        gross = movie.data["box office"].get("Cumulative Worldwide Gross", None)
        if budget:
            response.append(f"BUDGET {budget}.")
        if opening_week:
            response.append(f"OPENING WEEK {opening_week}.")
        if gross:
            response.append(f"CUMULATIVE WORLDWIDE GROSS {gross}.")
        return " ".join(response)
    LOGGER.warning(f"No IMDB box office info found for `{movie}`.")
    return None


@LOGGER.catch
def get_redgifs_gif(query: str, after_dark_only=False) -> Optional[str]:
    """Fetch specific kind of gif ;)."""
    night_mode = is_after_dark()
    if (after_dark_only and night_mode) or after_dark_only is False:
        token = redgifs_auth_token()
        endpoint = "https://napi.redgifs.com/v1/gfycats/search"
        params = {"search_text": query, "count": 100, "start": 0}
        headers = {"Authorization": f"Bearer {token}"}
        try:
            req = requests.get(endpoint, params=params, headers=headers)
            if bool(req.json()):
                results = req.json()["gfycats"]
                rand = randint(0, len(results) - 1)
                image_json = results[rand]
                image = image_json.get("max2mbGif")
                return image
            return f"Sorry bruh I couldnt find any images for ur dumb ass query LEARN2SEARCH :@"
        except HTTPError as e:
            LOGGER.error(
                f"Failed to get nsfw image for `{query}`: {e.response.content}"
            )
            return None
        except KeyError as e:
            LOGGER.error(
                f"Experienced KeyError while fetching nsfw image for `{query}`: {e}"
            )
            return None
        except Exception as e:
            LOGGER.error(
                f"Unexpected error while fetching nsfw image for `{query}`: {e}"
            )
            return None
    return "https://i.imgur.com/oGMHkqT.jpg"


@LOGGER.catch
def gfycat_auth_token() -> Optional[str]:
    """Get auth token for gfycat."""
    endpoint = "https://api.gfycat.com/v1/oauth/token"
    body = {
        "grant_type": "client_credentials",
        "client_id": GFYCAT_CLIENT_ID,
        "client_secret": GFYCAT_CLIENT_SECRET,
    }
    headers = {"Content-Type": "application/json"}
    try:
        req = requests.post(endpoint, json=body, headers=headers)
        if req.status_code == 200:
            return req.json().get("access_token")
    except HTTPError as e:
        LOGGER.error(f"Failed to get gfycat auth token: {e.response.content}")
        return None
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching gfycat auth token: {e}")
        return None


@LOGGER.catch
def redgifs_auth_token() -> Optional[str]:
    """Get redgifs auth via webtoken method."""
    endpoint = "https://weblogin.redgifs.com/oauth/webtoken"
    body = {"access_key": REDGIFS_ACCESS_KEY}
    headers = {"Content-Type": "application/json"}
    try:
        req = requests.post(endpoint, json=body, headers=headers)
        if req.status_code == 200:
            return req.json()["access_token"]
    except HTTPError as e:
        LOGGER.error(f"Failed to get redgifs auth token: {e.response.content}")
        return None
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching redgifs auth token: {e}")
        return None


@LOGGER.catch
def blaze_time_remaining() -> str:
    """Get remaining time until target time."""
    now = datetime.now(tz=pytz.timezone("America/New_York"))
    am_time = now.replace(hour=4, minute=20, second=0)
    pm_time = now.replace(hour=16, minute=20, second=0)
    if am_time > now:
        remaining = f"{am_time - now}"
    elif am_time < now < pm_time:
        remaining = f"{pm_time - now}"
    else:
        tomorrow_am_time = now.replace(day=now.day + 1, hour=4, minute=20, second=0)
        remaining = f"{tomorrow_am_time - now}"
    remaining = remaining.split(":")
    return emojize(
        f":herb: :fire: \
            {remaining[0]} hours, {remaining[1]} minutes, & {remaining[2]} seconds until 4:20 \
            :smoking: :kissing_closed_eyes: :dash:",
        use_aliases=True,
    )


def get_instagram_token() -> Optional[Response]:
    """Generate Instagram OAuth token."""
    try:
        params = {
            "client_id": INSTAGRAM_APP_ID,
        }
        return requests.post(f"https://www.facebook.com/x/oauth/status", params=params)
    except HTTPError as e:
        LOGGER.error(f"Failed to get Instagram token: {e.response.content}")
        return None
    except Exception as e:
        LOGGER.error(f"Failed to get Instagram token: {e}")
        return None


def create_instagram_preview(url) -> Optional[str]:
    """Generate link preview for Instagram links."""
    try:
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "3600",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
        }
        req = requests.get(url, headers=headers)
        html = BeautifulSoup(req.content, "html.parser")
        img_tag = html.find("meta", property="og:image")
        if img_tag is not None:
            img = img_tag.get("content")
            description = html.find("title").get_text()
            return f"{img} {description}"
        return None
    except HTTPError as e:
        LOGGER.error(f"Instagram URL {url} threw status code : {e.response.content}")
    except Exception as e:
        LOGGER.error(f"Failed to get Instagram url: {e}")
        return None
