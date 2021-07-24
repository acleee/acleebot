"""Fetch weather for a given location."""
import requests
from emoji import emojize
from requests.exceptions import HTTPError

from clients import db
from config import CHATANGO_OBI_ROOM, METRIC_SYSTEM_USERS, WEATHERSTACK_API_KEY
from logger import LOGGER


def weather_by_location(location: str, room: str, user: str) -> str:
    """
    Return temperature and weather per city/state/zip.

    :param str location: Location to fetch weather for.
    :param room: Chatango room from which request originated.
    :param str user: User who made the request.
    :returns: str
    """
    endpoint = "http://api.weatherstack.com/current"
    temperature_units = get_preferred_units(room, user)
    params = {
        "access_key": WEATHERSTACK_API_KEY,
        "query": location.replace(";", ""),
        "units": temperature_units,
    }
    try:
        res = requests.get(endpoint, params=params)
        if res.status_code != 200:
            return emojize(
                f":warning:️️ wtf even is `{location}` :warning:", use_aliases=True
            )
        data = res.json()
        if data.get("success") == "false":
            return emojize(
                f":warning:️️ {data['error']['info']} :warning:",
                use_aliases=True,
            )
        if data.get("current") is None:
            return emojize(
                f":warning:️️ idk wtf you did but `{location}` fucked me up b :warning:",
                use_aliases=True,
            )
        weather_code = data["current"]["weather_code"]
        weather_emoji = db.fetch_weather_icon(weather_code).get("icon")
        if weather_emoji:
            weather_emoji = emojize(weather_emoji, use_aliases=True)
        response = f'\n\n{data["request"]["query"]}\n \
                        {weather_emoji} {data["current"]["weather_descriptions"][0]}\n \
                        Temp: {data["current"]["temperature"]}°{"c" if params["units"] == "m" else "f"} (feels like: {data["current"]["feelslike"]}{"c" if params["units"] == "m" else "f"}°)\n \
                        Precipitation: {data["current"]["precip"]}%\n \
                        Humidity: {data["current"]["humidity"]}%\n \
                        Cloud cover: {data["current"]["cloudcover"]}%\n \
                        Wind speed: {data["current"]["wind_speed"]}'
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


def get_preferred_units(room: str, user: str):
    """
    Determine whether to use metric or imperial units
    """
    if room == CHATANGO_OBI_ROOM or user in METRIC_SYSTEM_USERS:
        return "m"
    return "f"
