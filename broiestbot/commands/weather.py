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
            return emojize(f":warning:️️ wtf even is `{location}` :warning:")
        data = res.json()
        if data.get("success") == "false":
            return emojize(
                f":warning:️️ {data['error']['info']} :warning:",
            )
        if data.get("current") is None:
            return emojize(
                f":warning:️️ idk wtf you did but `{location}` fucked me up b :warning:",
            )
        weather_code = data["current"]["weather_code"]
        is_day = data["current"]["is_day"]
        weather_emoji = get_weather_emoji(weather_code, is_day)
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
        )
    except KeyError as e:
        LOGGER.error(f"KeyError while fetching weather for `{location}`: {e}")
        return emojize(
            f":warning:️️ omfg u broke the bot WHAT DID YOU DO IM DEAD AHHHHHH :warning:",
        )
    except Exception as e:
        LOGGER.error(f"Failed to get weather for `{location}`: {e}")
        return emojize(
            f":warning:️️ omfg u broke the bot WHAT DID YOU DO IM DEAD AHHHHHH :warning:",
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
    weather_emoji_response = db.fetch_weather_icon(weather_code)
    if weather_emoji_response.get("icon") and is_day == "yes":
        return emojize(weather_emoji_response.get("icon"))
    elif is_day == "no" and weather_emoji_response.get("group") in [
        "sun",
        None,
    ]:
        return emojize(":night_with_stars:")
    elif weather_emoji_response.get("icon") and is_day == "no":
        return emojize(weather_emoji_response.get("icon"))
    return emojize(":sun:")
