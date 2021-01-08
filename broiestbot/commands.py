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
from pandas import DataFrame
from praw.exceptions import RedditAPIException
from requests import Response
from requests.exceptions import HTTPError

from broiestbot.afterdark import is_after_dark
from clients import cch, gcs, ia, reddit, sch, sms, wiki
from config import (
    CHATANGO_SPECIAL_USERS,
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
    TWILIO_SENDER_PHONE,
    TWILIO_RECIPIENT_PHONE
)
from logger import LOGGER

# Plotly
chart_studio.tools.set_credentials_file(
    username=PLOTLY_USERNAME, api_key=PLOTLY_API_KEY
)


def basic_message(message):
    """Send basic text message to room."""
    return message


def get_crypto(symbol: str) -> str:
    """
    Fetch crypto price and generate 60-day performance chart.

    :param symbol: Crypto symbol to fetch prices for.
    :type symbol: str

    :returns: str
    """
    try:
        chart = cch.get_chart(symbol)
        return chart
    except HTTPError as e:
        LOGGER.error(e)
        return emojize(
            f":warning: omg the internet died AAAAA :warning:", use_aliases=True
        )
    except Exception as e:
        LOGGER.error(e)
        return emojize(
            f":warning: yea nah idk wtf ur searching for :warning:", use_aliases=True
        )


def fetch_image_from_gcs(message) -> str:
    """Get a random image from Google Cloud Storage bucket."""
    images = gcs.bucket.list_blobs(prefix=message)
    image_list = [image.name for image in images if "." in image.name]
    rand = randint(0, len(image_list) - 1)
    image = GOOGLE_BUCKET_URL + GOOGLE_BUCKET_NAME + "/" + image_list[rand]
    return image


def giphy_image_search(query: str) -> str:
    """
    Giphy image search.

    :param query: Query used to find gif.
    :type query: str

    :returns: str
    """
    rand = randint(0, 20)
    params = {
        "api_key": GIPHY_API_KEY,
        "q": query,
        "limit": 1,
        "offset": rand,
        "rating": "R",
        "lang": "en",
    }
    try:
        req = requests.get("https://api.giphy.com/v1/gifs/search", params=params)
        if req.status_code != 200:
            return "image not found :("
        image = req.json()["data"][0]["images"]["downsized"]["url"]
        return image
    except HTTPError as e:
        LOGGER.error(f"Giphy failed to fetch `{query}`: {e.response.content}")
        return emojize(
            f":warning: omfg you broke giphy wtf :warning:", use_aliases=True
        )
    except KeyError as e:
        LOGGER.warning(f"Giphy KeyError for `{query}`: {e}")
        return emojize(
            f":warning: yea nah idk wtf ur searching for :warning:", use_aliases=True
        )
    except IndexError as e:
        LOGGER.warning(f"Giphy IndexError for `{query}`: {e}")
        return emojize(
            f":warning: yea nah idk wtf ur searching for :warning:", use_aliases=True
        )
    except Exception as e:
        LOGGER.error(f"Giphy unexpected error for `{query}`: {e}")
        return emojize(
            f":warning: AAAAAA I'M BROKEN WHAT DID YOU DO :warning:", use_aliases=True
        )


def random_image(message: str) -> str:
    """
    Randomly select a response from a given set.

    :param message: Query matching a command to set a random image from a set.
    :type message: str

    :returns: str
    """
    try:
        image_list = message.replace(" ", "").split(";")
        random_pic = image_list[randint(0, len(image_list) - 1)]
        return random_pic
    except KeyError as e:
        LOGGER.warning(f"KeyError when fetching random image: {e}")
        return emojize(
            f":warning: o shit i broke im a trash bot :warning:", use_aliases=True
        )
    except Exception as e:
        LOGGER.warning(f"Unexpected error when fetching random image: {e}")
        return emojize(
            f":warning: o shit i broke im a trash bot :warning:", use_aliases=True
        )


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


def get_stock(symbol: str) -> str:
    """
    Fetch stock price and generate 30-day performance chart.

    :param symbol: Stock symbol to fetch prices for.
    :type symbol: str

    :returns: str
    """
    try:
        chart = sch.get_chart(symbol)
        return chart
    except HTTPError as e:
        LOGGER.error(e)
        return emojize(
            f":warning: ough nough da site i get stocks from died :warning:",
            use_aliases=True,
        )
    except Exception as e:
        LOGGER.error(e)
        return emojize(
            f":warning: i broke bc im a shitty bot :warning:", use_aliases=True
        )


def get_urban_definition(term: str) -> str:
    """
    Fetch Urban Dictionary definition for a given phrase or word.

    :param term: Word or phrase to fetch UD definition for.
    :type term: str

    :returns: str
    """
    params = {"term": term}
    headers = {"Content-Type": "application/json"}
    try:
        req = requests.get(
            "http://api.urbandictionary.com/v0/define", params=params, headers=headers
        )
        results = req.json().get("list")
        if results:
            word = term.upper()
            results = sorted(results, key=lambda i: i["thumbs_down"], reverse=True)
            definition = (
                str(results[0].get("definition")).replace("[", "").replace("]", "")
            )[0:1500]
            example = results[0].get("example")
            if example:
                example = str(example).replace("[", "").replace("]", "")[0:250]
                return f"{word}:\n\n {definition} \n\n EXAMPLE: {example}"
            return f"{word}:\n\n {definition}"
        return emojize(
            ":warning: idk wtf ur trying to search for tbh :warning:", use_aliases=True
        )
    except HTTPError as e:
        LOGGER.error(
            f"HTTPError while trying to get Urban definition for `{term}`: {e.response.content}"
        )
        return emojize(
            f":warning: wtf urban dictionary is down :warning:", use_aliases=True
        )
    except KeyError as e:
        LOGGER.error(f"KeyError error when fetching Urban definition for `{term}`: {e}")
        return emojize(":warning: mfer you broke bot :warning:", use_aliases=True)
    except IndexError as e:
        LOGGER.error(
            f"IndexError error when fetching Urban definition for `{term}`: {e}"
        )
        return emojize(":warning: mfer you broke bot :warning:", use_aliases=True)
    except Exception as e:
        LOGGER.error(
            f"Unexpected error when fetching Urban definition for `{term}`: {e}"
        )
        return emojize(":warning: mfer you broke bot :warning:", use_aliases=True)


def weather_by_city(location: str, weather: DataFrame, room: str) -> str:
    """
    Return temperature and weather per city/state/zip.

    :param location: City or location to fetch weather for.
    :type location: str
    :param weather: Table matching types of weather to emojis.
    :type weather: DataFrame
    :param location: City or location to fetch weather for.
    :type location: str
    :param room: Name of Chatango room.
    :type room: str

    :returns: str
    """
    units = "f"
    endpoint = "http://api.weatherstack.com/current"
    params = {
        "access_key": WEATHERSTACK_API_KEY,
        "query": location.replace(";", ""),
        "units": "f",
    }
    if room == "goatfibres69":
        params["units"] = "m"
        units = "c"
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
                            (feels like {data["current"]["feelslike"]}°{units}). \
                            {data["current"]["precip"] * 100}% precipitation.'
            return response
    except HTTPError as e:
        LOGGER.error(f"Failed to get weather for `{location}`: {e.response.content}")
        return emojize(
            f":warning:️️ fk me the weather API is down :warning:",
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


def find_imdb_movie(movie_title: str) -> Optional[str]:
    """
    Get movie information from IMDB.

    :param movie_title: Movie to fetch information and box office info for.
    :type movie_title: str

    :returns: str
    """
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
        return emojize(
            f":warning: wtf kind of movie is {movie_title} :warning:", use_aliases=True
        )
    except Exception as e:
        LOGGER.error(f"Unexpected error while fetching IMDB movie `{movie_title}`: {e}")
        return emojize(
            f":warning: omfg u broke me with ur shit movie :warning:", use_aliases=True
        )


def get_boxoffice_data(movie) -> Optional[str]:
    """Get IMDB box office performance for a given film."""
    try:
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
    except KeyError as e:
        LOGGER.warning(f"No IMDB box office info found for `{movie}`: {e}")
    except Exception as e:
        LOGGER.warning(f"No IMDB box office info found for `{movie}`: {e}")


def get_redgifs_gif(query: str, after_dark_only=False) -> Optional[str]:
    """
    Fetch specific kind of gif ;).

    :param query: Query used to find gif.
    :type query: str
    :param after_dark_only: Whether results should be limited to the `after dark` timeframe.
    :type after_dark_only: bool

    :returns: Optional[str]
    """
    night_mode = is_after_dark()
    if (after_dark_only and night_mode) or after_dark_only is False:
        token = redgifs_auth_token()
        endpoint = "https://napi.redgifs.com/v1/gfycats/search"
        params = {"search_text": query, "count": 100, "start": 0}
        headers = {"Authorization": f"Bearer {token}"}
        try:
            req = requests.get(endpoint, params=params, headers=headers)
            if req.status_code == 200:
                results = req.json().get("gfycats")
                rand = randint(0, len(results) - 1)
                image_json = results[rand]
                image = image_json.get("max1mbGif")
                if image is not None:
                    return image
        except HTTPError as e:
            LOGGER.error(
                f"Failed to get nsfw image for `{query}`: {e.response.content}"
            )
            return emojize(
                f":warning: yea nah idk wtf ur searching for :warning:",
                use_aliases=True,
            )
        except KeyError as e:
            LOGGER.error(
                f"Experienced KeyError while fetching nsfw image for `{query}`: {e}"
            )
            return emojize(
                f":warning: yea nah idk wtf ur searching for :warning:",
                use_aliases=True,
            )
        except Exception as e:
            LOGGER.error(
                f"Unexpected error while fetching nsfw image for `{query}`: {e}"
            )
            return emojize(
                f":warning: yea nah idk wtf ur searching for :warning:",
                use_aliases=True,
            )
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


def redgifs_auth_token() -> Optional[str]:
    """
    Authenticate with redgifs to receive access token.

    :returns: Optional[str]
    """
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


def blaze_time_remaining() -> str:
    """
    Get remaining time until target time.

    :returns: str
    """
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


def send_text_message(message: str, user: str) -> Optional[str]:
    """
    Send SMS to Bro via Twilio.

    :param message: Text message to send via SMS
    :type message: str
    :param user: User attempting to send SMS
    :type user: str

    :returns: Optional[str]
    """
    try:
        if user.lower() in CHATANGO_SPECIAL_USERS:
            sms.messages.create(
                body=f"{user.upper()}: {message}",
                from_=TWILIO_SENDER_PHONE,
                to=TWILIO_RECIPIENT_PHONE,
            )
            return f"ty @{user} I just texted brough: {message}"
        return emojize(
            f":warning: lmao fuck off, only pizza can text brough :warning:",
            use_aliases=True,
        )
    except Exception as e:
        LOGGER.error(f"Unexpected error when sending SMS: {e}")


def get_instagram_token() -> Optional[Response]:
    """
    Generate Instagram OAuth token.

    :returns: Optional[Response]
    """
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


def create_instagram_preview(url: str) -> Optional[str]:
    """
    Generate link preview for Instagram links.

    :param url: Instagram post URL
    :type url: str

    :returns: Optional[str]
    """
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
