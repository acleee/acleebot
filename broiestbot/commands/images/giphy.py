"""Perform Giphy query to fetch randomized top trending image."""
from random import randint

import requests
from emoji import emojize
from requests.exceptions import HTTPError

from config import GIPHY_API_KEY
from logger import LOGGER


def giphy_image_search(query: str, retry=False) -> str:
    """
    Perform a gif image and return a random result from the top-20 images.

    :param str query: Query passed to Giphy to find gif.
    :param bool retry: Whether the image fetch is a retry from a previous attempt.

    :returns: str
    """
    rand = randint(0, 15)
    params = {
        "api_key": GIPHY_API_KEY,
        "q": query,
        "limit": 1,
        "offset": rand,
        "rating": "R",
        "lang": "en",
    }
    try:
        resp = requests.get("https://api.giphy.com/v1/gifs/search", params=params)
        num_images = len(resp.json()["data"])
        if num_images == 0:
            return "image not found :("
        image = resp.json()["data"][0]["images"]["downsized"].get("url")
        if image is not None:
            return image
        elif retry is False:
            return giphy_image_search(query, retry=True)
        return emojize(
            f":warning: holy sht u broke the bot im telling bro :warning:",
        )
    except HTTPError as e:
        LOGGER.error(f"Giphy failed to fetch `{query}`: {e.response.content}")
        return emojize(f":warning: yoooo giphy is down rn lmao :warning:")
    except ValueError as e:
        LOGGER.error(f"ValueError while fetching Giphy `{query}`: {e}")
        return emojize(
            f":warning: holy sht u broke the bot im telling bro :warning:",
        )
    except Exception as e:
        LOGGER.error(f"Giphy unexpected error for `{query}`: {e}")
        return emojize(f":warning: AAAAAA I'M BROKEN WHAT DID YOU DO :warning:")
