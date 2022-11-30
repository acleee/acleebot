"""Commands only available from 12am to 5am EST."""
from datetime import datetime
from random import randint
from typing import Optional

import pytz
import requests
from emoji import emojize
from requests.exceptions import HTTPError

from config import (
    REDGIFS_ACCESS_KEY,
    REDGIFS_IMAGE_SEARCH_ENDPOINT,
    REDGIFS_TOKEN_ENDPOINT,
    HTTP_REQUEST_TIMEOUT,
)
from logger import LOGGER


def is_after_dark() -> bool:
    """
    Determine if current time is within threshold for `After Dark` mode.

    :return: Boolean
    """
    tz = pytz.timezone("America/New_York")
    now = datetime.now(tz=tz)
    start_time = datetime(year=now.year, month=now.month, day=now.day, hour=0, tzinfo=now.tzinfo)
    end_time = datetime(year=now.year, month=now.month, day=now.day, hour=5, tzinfo=now.tzinfo)
    if start_time > now and now < end_time:
        return True
    return False


def get_redgifs_gif(query: str, username: str, after_dark_only: bool = False) -> Optional[str]:
    """
    Fetch a special kind of gif, if you know what I mean ;).

    :param str query: Gif search query.
    :param str username: Chatango user who triggered the command.
    :param bool after_dark_only: Whether results should be limited to the `after dark` timeframe.

    :returns: Optional[str]
    """
    try:
        night_mode = is_after_dark()
        if (after_dark_only and night_mode) or after_dark_only is False:
            token = redgifs_auth_token()
            endpoint = REDGIFS_IMAGE_SEARCH_ENDPOINT
            params = {"search_text": query.title(), "order": "trending", "count": 80}
            headers = {"Authorization": f"Bearer {token}"}
            resp = requests.get(
                endpoint, params=params, headers=headers, timeout=HTTP_REQUEST_TIMEOUT
            )
            results = resp.json().get("gifs", None)
            if resp.status_code == 200 and results is not None:
                results = [result for result in results if result["urls"].get("sd") is not None]
                if bool(results):
                    rand = randint(0, len(results) - 1)
                    image_json = results[rand]
                    return get_full_gif_metadata(image_json)
                elif username == "thegreatpizza":
                    return emojize(
                        f":pizza: *h* wow pizza ur taste in lesbians is so dank that I coughldnt find nething sry :( *h* :pizza:",
                        language="en",
                    )
                elif username == "broiestbro":
                    return emojize(f"bro wot r u searching 4 go2bed", language="en")
                else:
                    return emojize(
                        f":warning: wow @{username} u must b a freak tf r u even searching foughr jfc :warning:",
                    )
            else:
                LOGGER.error(f"Error {resp.status_code} fetching NSFW gif: {resp.content}")
                return emojize(
                    f":warning: omfg @{username} u broke bot with ur kinky ass bs smfh :warning:",
                    language="en",
                )
        return "https://i.imgur.com/oGMHkqT.jpg"
    except HTTPError as e:
        LOGGER.warning(f"HTTPError while fetching nsfw image for `{query}`: {e.response.content}")
        return emojize(f":warning: yea nah idk wtf ur searching for :warning:", language="en")
    except IndexError as e:
        LOGGER.warning(f"IndexError while fetching nsfw image for `{query}`: {e}")
        return emojize(f":warning: yea nah idk wtf ur searching for :warning:", language="en")
    except Exception as e:
        LOGGER.warning(f"Unexpected error while fetching nsfw image for `{query}`: {e}")
        return emojize(
            f":warning: dude u must b a freak cuz that just broke bot :warning:", language="en"
        )


def get_full_gif_metadata(image: dict) -> str:
    """
    Parses additional metadata for a randomly selected gif.

    :param dict image: Dictionary containing a single gif response.

    :returns: str
    """
    try:
        image_url = image["urls"]["sd"].replace("-mobile", "").replace(".mp4", "-small.gif")
        likes = image["likes"]
        views = image["views"]
        tags = ", #".join(image["tags"])
        return emojize(
            f"\n\n\n{image_url}\n:thumbsup: Likes {likes}\n:eyes: Views {views}\n#{tags}",
        )
    except Exception as e:
        LOGGER.warning(f"Unexpected error while fetching nsfw image for id `{image['id']}`: {e}")
        return emojize(
            f":warning: dude u must b a freak cuz that just broke bot :warning:",
        )


def redgifs_auth_token() -> Optional[str]:
    """
    Authenticate with redgifs to receive access token.

    :returns: Optional[str]
    """
    endpoint = REDGIFS_TOKEN_ENDPOINT
    body = {"access_key": REDGIFS_ACCESS_KEY}
    headers = {"Content-Type": "application/json"}
    try:
        resp = requests.post(endpoint, json=body, headers=headers, timeout=HTTP_REQUEST_TIMEOUT)
        if resp.status_code == 200:
            return resp.json().get("access_token")
        else:
            LOGGER.error(
                f"Failed to get Redgifs token with status code {resp.status_code}: {resp.json()}"
            )
    except HTTPError as e:
        LOGGER.error(f"HTTPError when fetching Redgifs auth token: {e.response.content}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching Redgifs auth token: {e}")
