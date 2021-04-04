"""Commands only available from 12am to 5am EST."""
from datetime import datetime
from random import randint
from typing import Optional

import pytz
import requests
from emoji import emojize
from requests.exceptions import HTTPError

from config import GFYCAT_CLIENT_ID, GFYCAT_CLIENT_SECRET, REDGIFS_ACCESS_KEY
from logger import LOGGER


def is_after_dark() -> bool:
    """
    Determine if current time is in threshold for `After Dark` mode.
    :return: Boolean
    """
    tz = pytz.timezone("America/New_York")
    now = datetime.now(tz=tz)
    start_time = datetime(
        year=now.year, month=now.month, day=now.day, hour=0, tzinfo=now.tzinfo
    )
    end_time = datetime(
        year=now.year, month=now.month, day=now.day, hour=5, tzinfo=now.tzinfo
    )
    if start_time < now < end_time:
        return True
    return False


def get_redgifs_gif(query: str, after_dark_only: bool = False) -> Optional[str]:
    """
    Fetch a special kind of gif, if you know what I mean ;).

    :param query: Gif search query.
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
                if results:
                    rand = randint(0, len(results) - 1)
                    image_json = results[rand]
                    image_url = image_json.get("max1mbGif")
                    if image_url is not None:
                        image_status = requests.get(image_url)
                        if image_status.status_code != 200:
                            get_redgifs_gif(query, after_dark_only=False)
                        return image_url
        except HTTPError as e:
            LOGGER.warning(
                f"HTTPError while fetching nsfw image for `{query}`: {e.response.content}"
            )
            return emojize(
                f":warning: yea nah idk wtf ur searching for :warning:",
                use_aliases=True,
            )
        except KeyError as e:
            LOGGER.warning(f"KeyError while fetching nsfw image for `{query}`: {e}")
            return emojize(
                f":warning: yea nah idk wtf ur searching for :warning:",
                use_aliases=True,
            )
        except Exception as e:
            LOGGER.warning(
                f"Unexpected error while fetching nsfw image for `{query}`: {e}"
            )
            return emojize(
                f":warning: dude u must b a freak cuz that just broke bot :warning:",
                use_aliases=True,
            )
        return emojize(
            f":warning: yo u must b a freak tf r u even searching foughr jfc :warning:",
            use_aliases=True,
        )
    return "https://i.imgur.com/oGMHkqT.jpg"


@LOGGER.catch
def gfycat_auth_token() -> Optional[str]:
    """
    Get auth token for gfycat.

    :returns: Optional[str]
    """
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
        LOGGER.error(f"HTTPError when fetching gfycat auth token: {e.response.content}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching gfycat auth token: {e}")


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
        LOGGER.error(
            f"HTTPError when fetching redgifs auth token: {e.response.content}"
        )
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching redgifs auth token: {e}")
