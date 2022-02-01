"""Fetch meme images."""
from random import randint

import requests
from emoji import emojize
from google.cloud.exceptions import GoogleCloudError, NotFound
from praw.exceptions import RedditAPIException
from requests.exceptions import HTTPError

from clients import gcs, reddit
from config import GIPHY_API_KEY, GOOGLE_BUCKET_NAME, GOOGLE_BUCKET_URL
from logger import LOGGER


def fetch_image_from_gcs(subdirectory: str) -> str:
    """
    Get image from Google Cloud Storage bucket.

    :param str subdirectory: Directory on remote CDN from which to fetch random image.

    :returns: str
    """
    try:
        images = gcs.bucket.list_blobs(prefix=subdirectory)
        image_list = [image.name for image in images if "." in image.name]
        rand = randint(0, len(image_list) - 1)
        image = GOOGLE_BUCKET_URL + GOOGLE_BUCKET_NAME + "/" + image_list[rand]
        return image.lower()
    except NotFound as e:
        LOGGER.warning(f"GCS `NotFound` error when fetching image for `{subdirectory}`: {e}")
        return emojize(f":warning: omfg bot just broke wtf did u do :warning:", use_aliases=True)
    except GoogleCloudError as e:
        LOGGER.warning(
            f"GCS `GoogleCloudError` error when fetching image for `{subdirectory}`: {e}"
        )
        return emojize(f":warning: omfg bot just broke wtf did u do :warning:", use_aliases=True)
    except ValueError as e:
        LOGGER.warning(f"ValueError when fetching random GCS image for `{subdirectory}`: {e}")
        return emojize(f":warning: omfg bot just broke wtf did u do :warning:", use_aliases=True)
    except Exception as e:
        LOGGER.warning(f"Unexpected error when fetching random GCS image for `{subdirectory}`: {e}")
        return emojize(f":warning: o shit i broke im a trash bot :warning:", use_aliases=True)


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
            use_aliases=True,
        )
    except HTTPError as e:
        LOGGER.error(f"Giphy failed to fetch `{query}`: {e.response.content}")
        return emojize(f":warning: yoooo giphy is down rn lmao :warning:", use_aliases=True)
    except KeyError as e:
        LOGGER.error(f"Giphy KeyError for `{query}`: {e}")
        return emojize(
            f":warning: holy sht u broke the bot im telling bro :warning:",
            use_aliases=True,
        )
    except IndexError as e:
        LOGGER.error(f"Giphy IndexError for `{query}`: {e}")
        return emojize(
            f":warning: holy sht u broke the bot im telling bro :warning:",
            use_aliases=True,
        )
    except Exception as e:
        LOGGER.error(f"Giphy unexpected error for `{query}`: {e}")
        return emojize(f":warning: AAAAAA I'M BROKEN WHAT DID YOU DO :warning:", use_aliases=True)


def random_image(message: str) -> str:
    """
    Select a random image from a fixed set associated with a command.
    NOTE: This is a legacy command which should later be replaced with `fetch_image_from_gcs`.

    :param str message: Query matching a command to set a random image from a set.

    :returns: str
    """
    try:
        image_list = message.replace(" ", "").split(";")
        random_pic = image_list[randint(0, len(image_list) - 1)]
        return random_pic
    except ValueError as e:
        LOGGER.warning(f"ValueError when fetching random image for `{message}`: {e}")
        return emojize(f":warning: omfg bot just broke wtf did u do :warning:", use_aliases=True)
    except Exception as e:
        LOGGER.warning(f"Unexpected error when fetching random image for `{message}`: {e}")
        return emojize(f":warning: o shit i broke im a trash bot :warning:", use_aliases=True)


def subreddit_image(subreddit: str) -> str:
    """
    Fetch most recent image posted to a subreddit.

    :param str subreddit: Name of subreddit matching URL (sans `/r/`)

    :returns: str
    """
    try:
        images = [post for post in reddit.subreddit(subreddit).new(limit=10)]
        if images:
            return images[0]
    except RedditAPIException as e:
        LOGGER.error(f"Reddit image search failed for subreddit `{subreddit}`: {e}")
        return emojize(f":warning: i broke bc im a shitty bot :warning:", use_aliases=True)
    except Exception as e:
        LOGGER.error(f"Unexpected error when Reddit searching for `{subreddit}`: {e}")
        return emojize(f":warning: i broke bc im a shitty bot :warning:", use_aliases=True)
