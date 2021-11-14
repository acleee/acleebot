"""Commands only available from 12am to 5am EST."""
from datetime import datetime
from random import randint
from time import sleep
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
    start_time = datetime(
        year=now.year, month=now.month, day=now.day, hour=22, tzinfo=now.tzinfo
    )
    end_time = datetime(
        year=now.year, month=now.month, day=now.day, hour=5, tzinfo=now.tzinfo
    )
    if start_time > now or end_time < now:
        return True
    return False


def get_redgifs_gif(
    query: str, username: str, after_dark_only: bool = False
) -> Optional[str]:
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
            params = {"search_text": query, "order": "trending"}
            headers = {"Authorization": f"Bearer {token}"}
            resp = requests.get(endpoint, params=params, headers=headers)
            if resp.status_code == 200:
                results = resp.json().get("gifs")
                if results:
                    rand = randint(0, len(results) - 1)
                    image_json = results[rand]
                    image_url = image_json["urls"].get("gif")
                    tags = ", #".join(image_json["tags"])
                    if image_url is not None:
                        image_status = requests.get(image_url)
                        if image_status.status_code != 200:
                            sleep(2)
                            for i in range(3):
                                LOGGER.warn(
                                    f"`After dark` failed with status code {resp.status_code}. Retrying {i} time..."
                                )
                                return get_redgifs_gif(
                                    query, username, after_dark_only=False
                                )
                        return f"{image_url} \n #{tags}"
                elif username == "thegreatpizza":
                    return emojize(
                        f":pizza: :heart: wow pizza ur taste in lesbians is so dank that I coughldnt find nething sry :( :heart: :pizza:",
                        use_aliases=True,
                    )
                else:
                    LOGGER.error(
                        f"Error {resp.status_code} fetching NSFW gif: {resp.content}"
                    )
                    return emojize(
                        f":warning: wow @{username} u must b a freak tf r u even searching foughr jfc :warning:",
                        use_aliases=True,
                    )
        return "https://i.imgur.com/oGMHkqT.jpg"
    except HTTPError as e:
        LOGGER.warning(
            f"HTTPError while fetching nsfw image for `{query}`: {e.response.content}"
        )
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
            LOGGER.error(
                f"Failed to get Redgifs token with status code {resp.status_code}: {resp.json()}"
            )
    except HTTPError as e:
        LOGGER.error(
            f"HTTPError when fetching redgifs auth token: {e.response.content}"
        )
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching redgifs auth token: {e}")
