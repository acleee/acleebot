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
        resp = requests.get(WEATHERSTACK_API_ENDPOINT, params=params)
        if resp.status_code != 200:
            return emojize(f":warning:️️ wtf even is `{location}` :warning:")
        resp = resp.json()
        if resp.get("success") == "false":
            return emojize(f":warning:️️ {resp['error']['info']} :warning:")
        if resp.get("current") is None:
            return emojize(
                f":warning:️️ idk wtf you did but `{location}` fucked me up b :warning:",
            )
        weather_code = resp["current"]["weather_code"]
        is_day = resp["current"]["is_day"]
        temperature = resp["current"]["temperature"]
        feels_like = resp["current"]["feelslike"]
        precipitation = resp["current"]["precip"] * 10
        cloud_cover = resp["current"]["cloudcover"]
        humidity = resp["current"]["humidity"]
        wind_speed = resp["current"]["wind_speed"]
        local_time = resp["location"]["localtime"].split(" ")[1]
        weather_emoji = get_weather_emoji(weather_code, is_day)
        precipitation_emoji = get_precipitation_emoji(resp["current"]["precip"])
        humidity_emoji = get_humidity_emoji(humidity)
        cloud_cover_emoji = get_cloud_cover_emoji(cloud_cover)
        response = emojize(
            f'\n\n<b>{resp["request"]["query"]}</b>\n \
                        {weather_emoji} {resp["current"]["weather_descriptions"][0]}\n \
                        :thermometer: Temp: {temperature}°{"c" if params["units"] == "m" else "f"} (feels like: {feels_like}{"c" if params["units"] == "m" else "f"}°)\n \
                        {precipitation_emoji} Precipitation: {precipitation}%\n \
                        {humidity_emoji} Humidity: {humidity}%\n \
                        {cloud_cover_emoji} Cloud cover: {cloud_cover}%\n \
                        :wind_face: Wind speed: {wind_speed}{"km/h" if params["units"] == "m" else "mph"}\n \
                        :six-thirty: {local_time}'
        )
        return response
    except HTTPError as e:
        LOGGER.error(f"Failed to get weather for `{location}`: {e.response.content}")
        return emojize(f":warning:️️ fk me the weather API is down :warning:")
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


def get_precipitation_emoji(precipitation: int) -> str:
    """
    Get emoji based on forecasted precipitation.

    :param int precipitation: Percentage chance of precipitation on the day.

    :returns: str
    """
    if precipitation > 70:
        return ":cloud_with_rain:"
    if precipitation > 50:
        return ":cloud:"
    return ":sparkles:"


def get_humidity_emoji(humidity: int) -> str:
    """
    Get emoji based on current humidity.

    :param int humidity: Current humidity percentage.

    :returns: str
    """
    if humidity > 85:
        return ":downcast_face_with_sweat:"
    if humidity > 60:
        return ":grinning_face_with_sweat:"
    return ":slightly_smiling_face:"


def get_cloud_cover_emoji(cloud_cover: int) -> str:
    """
    Get emoji based on forecasted precipitation.

    :param int cloud_cover: Percentage of current cloud cover.

    :returns: str
    """
    if cloud_cover > 80:
        return ":cloud:"
    if cloud_cover > 60:
        return ":sun_behind_cloud:"
    return ":thumbs_up_light_skin_tone:"
