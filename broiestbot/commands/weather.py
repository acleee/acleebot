"""Fetch weather for a given location."""
import requests
from database import session
from database.models import Weather
from emoji import emojize
from requests.exceptions import HTTPError

from config import (
    CHATANGO_OBI_ROOM,
    METRIC_SYSTEM_USERS,
    WEATHERSTACK_API_ENDPOINT,
    WEATHERSTACK_API_KEY,
)
from logger import LOGGER


def weather_by_location(location: str, room: str, user: str) -> str:
    """
    Return temperature and weather per city/state/zip.

    :param str location: Location to fetch weather for.
    :param room: Chatango room from which request originated.
    :param str user: User who made the request.

    :returns: str
    """
    temperature_units = get_preferred_units(room, user)
    params = {
        "access_key": WEATHERSTACK_API_KEY,
        "query": location.replace(";", ""),
        "units": temperature_units,
    }
    try:
        res = requests.get(WEATHERSTACK_API_ENDPOINT, params=params)
        if res.status_code != 200:
            return emojize(f":warning:️️ wtf even is `{location}` :warning:")
        data = res.json()
        if data.get("success") == "false":
            return emojize(f":warning:️️ {data['error']['info']} :warning:", use_aliases=True)
        if data.get("current") is None:
            return emojize(
                f":warning:️️ idk wtf you did but `{location}` fucked me up b :warning:",
                use_aliases=True,
            )
        weather_code = data["current"]["weather_code"]
        is_day = data["current"]["is_day"]
        weather_emoji = get_weather_emoji(weather_code, is_day)
        response = emojize(
            f'\n\n{data["request"]["query"]}\n \
                        {weather_emoji} {data["current"]["weather_descriptions"][0]}\n \
                        Temp: {data["current"]["temperature"]}°{"c" if params["units"] == "m" else "f"} (feels like: {data["current"]["feelslike"]}{"c" if params["units"] == "m" else "f"}°)\n \
                        Precipitation: {data["current"]["precip"] * 10}%\n \
                        Humidity: {data["current"]["humidity"]}%\n \
                        Cloud cover: {data["current"]["cloudcover"]}%\n \
                        Wind speed: {data["current"]["wind_speed"]}{"km/h" if params["units"] == "m" else "mph"}',
            use_aliases=True,
        )
        return response
    except HTTPError as e:
        LOGGER.error(f"Failed to get weather for `{location}`: {e.response.content}")
        return emojize(f":warning:️️ fk me the weather API is down :warning:", use_aliases=True)
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


def get_preferred_units(room: str, user: str) -> str:
    """
    Determine whether to use metric or imperial units.

    :param room: Chatango room from which request originated.
    :param str user: User who made the request.

    :returns: str
    """
    if room == CHATANGO_OBI_ROOM or user in METRIC_SYSTEM_USERS:
        return "m"
    return "f"


def get_weather_emoji(weather_code: int, is_day: str) -> str:
    """
    Fetch emoji to best represent location weather based on weather code and time of day.

    :param int weather_code: Numerical code representing general weather type.
    :param str is_day: Whether the target location is currently experiencing daylight.

    :returns: str
    """
    weather_emoji = session.query(Weather).filter(Weather.code == weather_code).one_or_none()
    if weather_emoji is not None:
        return weather_emoji.icon
    elif is_day == "no" and weather_emoji.group in [
        "sun",
        None,
    ]:
        return emojize(":night_with_stars:")
    elif weather_emoji.icon and is_day == "no":
        return weather_emoji.icon
    return ":sun:"
