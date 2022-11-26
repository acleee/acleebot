"""Perform Giphy query to fetch randomized top trending image."""
from random import randint
from typing import Optional

import requests
from emoji import emojize
from requests.exceptions import HTTPError

from config import GIPHY_API_KEY, HTTP_REQUEST_TIMEOUT
from logger import LOGGER


def giphy_image_search(query: str) -> Optional[str]:
    """
    Perform a gif image and return a random result from the top-20 images.

    :param str query: Query passed to Giphy to find gif.

    :returns: Optional[str]
    """
    rand = randint(0, 15)
    params = {
        "api_key": GIPHY_API_KEY,
        "q": query,
        "limit": 1,
        "offset": rand,
        "rating": "r",
        "lang": "en",
    }
    try:
        resp = requests.get(
            "https://api.giphy.com/v1/gifs/search", params=params, timeout=HTTP_REQUEST_TIMEOUT
        )
        images = resp.json()["data"]
        if len(images) == 0:
            return None
        image = resp.json()["data"][0]["images"]["downsized"].get("url")
        if image is not None:
            return image
    except HTTPError as e:
        LOGGER.error(f"Giphy failed to fetch `{query}`: {e.response.content}")
        return emojize(f":warning: yoooo giphy is down rn lmao :warning:", language="en")
    except ValueError as e:
        LOGGER.error(f"ValueError while fetching Giphy `{query}`: {e}")
        return emojize(
            f":warning: holy sht u broke the bot im telling bro :warning:", language="en"
        )
    except Exception as e:
        LOGGER.error(f"Giphy unexpected error for `{query}`: {e}")
        return emojize(f":warning: AAAAAA I'M BROKEN WHAT DID YOU DO :warning:", language="en")
