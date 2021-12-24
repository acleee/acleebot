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
)
from logger import LOGGER


def is_after_dark() -> bool:
    """
    Determine if current time is in threshold for `After Dark` mode.

    :return: Boolean
    """
    tz = pytz.timezone("America/New_York")
    now = datetime.now(tz=tz)
    start_time = datetime(year=now.year, month=now.month, day=now.day, hour=22, tzinfo=now.tzinfo)
    end_time = datetime(year=now.year, month=now.month, day=now.day, hour=5, tzinfo=now.tzinfo)
    if start_time > now or end_time < now:
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
            resp = requests.get(endpoint, params=params, headers=headers)
            results = resp.json().get("gifs", None)
            if resp.status_code == 200 and results is not None:
                results = [result for result in results if result["urls"].get("gif") is not None]
                if bool(results):
                    rand = randint(0, len(results) - 1)
                    image_json = results[rand]
                    image_id = image_json["id"]
                    return get_full_gif_metadata(image_id, token)
                elif username == "thegreatpizza":
                    return emojize(
                        f":pizza: *h* wow pizza ur taste in lesbians is so dank that I coughldnt find nething sry :( *h* :pizza:",
                        use_aliases=True,
                    )
                elif username == "broiestbro":
                    return emojize(
                        f":@ bro u fgt wot r u searching 4 go2bed :@",
                        use_aliases=True,
                    )
                else:
                    return emojize(
                        f":warning: wow @{username} u must b a freak tf r u even searching foughr jfc :warning:",
                        use_aliases=True,
                    )
            else:
                LOGGER.error(f"Error {resp.status_code} fetching NSFW gif: {resp.content}")
                return emojize(
                    f":warning: omfg @{username} u broke bot with ur kinky ass bs smfh :warning:",
                    use_aliases=True,
                )
        return "https://i.imgur.com/oGMHkqT.jpg"
    except HTTPError as e:
        LOGGER.warning(f"HTTPError while fetching nsfw image for `{query}`: {e.response.content}")
        return emojize(
            f":warning: yea nah idk wtf ur searching for :warning:",
            use_aliases=True,
        )
    except IndexError as e:
        LOGGER.warning(f"IndexError while fetching nsfw image for `{query}`: {e}")
        return emojize(
            f":warning: yea nah idk wtf ur searching for :warning:",
            use_aliases=True,
        )
    except Exception as e:
        LOGGER.warning(f"Unexpected error while fetching nsfw image for `{query}`: {e}")
        return emojize(
            f":warning: dude u must b a freak cuz that just broke bot :warning:",
            use_aliases=True,
        )


def get_full_gif_metadata(image_id: str, token: str) -> str:
    """
    Fetches additional metadata for a randomly selected gif.

    :param str image_id: Unique string serving as the image ID.
    :param str token: Authorization token

    :returns: str
    """
    try:
        endpoint = f"https://api.redgifs.com/v2/gifs/{image_id}"
        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.get(endpoint, headers=headers)
        if resp.status_code == 200:
            image = resp.json().get("gif")
            likes = image["likes"]
            views = image["views"]
            duration = image["duration"]
            gif = image["urls"].get("gif")
            tags = ", #".join(image["tags"])
            return emojize(
                f"\n\n\n{gif}\n:thumbsup: Likes {likes}\n:eyes: Views {views}\n:five_o’clock: Duration {duration}s\n#{tags}",
                use_aliases=True,
            )
    except Exception as e:
        LOGGER.warning(f"Unexpected error while fetching nsfw image for id `{image_id}`: {e}")
        return emojize(
            f":warning: dude u must b a freak cuz that just broke bot :warning:",
            use_aliases=True,
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
        resp = requests.post(endpoint, json=body, headers=headers)
        if resp.status_code == 200:
            return resp.json().get("access_token")
        else:
            LOGGER.error(f"Failed to get Redgifs token with status code {resp.status_code}: {resp.json()}")
    except HTTPError as e:
        LOGGER.error(f"HTTPError when fetching Redgifs auth token: {e.response.content}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching Redgifs auth token: {e}")
