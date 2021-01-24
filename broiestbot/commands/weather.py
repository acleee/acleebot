"""Fetch weather for a given location."""
import requests
from emoji import emojize
from pandas import DataFrame
from requests.exceptions import HTTPError

from config import CHATANGO_OBI_ROOM, METRIC_SYSTEM_USERS, WEATHERSTACK_API_KEY
from logger import LOGGER


def weather_by_location(location: str, weather: DataFrame, room: str, user: str) -> str:
    """
    Return temperature and weather per city/state/zip.

    :param location: City or location to fetch weather for.
    :type location: str
    :param weather: Table matching types of weather to emojis.
    :type weather: DataFrame
    :param location: City or location to fetch weather for.
    :type location: str
    :param room: Name the Chatango room that made the request (used for metric system).
    :type room: str
    :param user: User who made the request (used for metric system).
    :type user: str
    :returns: str
    """
    units = "f"
    endpoint = "http://api.weatherstack.com/current"
    params = {
        "access_key": WEATHERSTACK_API_KEY,
        "query": location.replace(";", ""),
        "units": "f",
    }
    if room == CHATANGO_OBI_ROOM or user in METRIC_SYSTEM_USERS:
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
                            {data["current"]["temperature"]}°{units} \
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
