"""Generate link previews from URLs."""
from typing import Optional

import requests
from bs4 import BeautifulSoup
from requests import Response
from requests.exceptions import HTTPError

from config import INSTAGRAM_APP_ID
from logger import LOGGER


def create_instagram_preview(url: str) -> Optional[str]:
    """
    Generate link preview for Instagram post URLs.

    :param url: Instagram post URL (image or video).
    :type url: str
    :returns: Optional[str]
    """
    try:
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "3600",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
        }
        req = requests.get(url, headers=headers)
        html = BeautifulSoup(req.content, "html.parser")
        img_tag = html.find("meta", property="og:image")
        if img_tag is not None:
            img = img_tag.get("content")
            description = html.find("title").get_text()
            return f"{img} {description}"
        return None
    except HTTPError as e:
        LOGGER.error(
            f"HTTPError while fetching Instagram URL `{url}`: {e.response.content}"
        )
    except Exception as e:
        LOGGER.error(f"Unexpected error while creating Instagram embed: {e}")


def get_instagram_token() -> Optional[Response]:
    """
    Generate Instagram OAuth token.

    :returns: Optional[Response]
    """
    try:
        params = {
            "client_id": INSTAGRAM_APP_ID,
        }
        return requests.post(f"https://www.facebook.com/x/oauth/status", params=params)
    except HTTPError as e:
        LOGGER.error(f"HTTPError while fetching Instagram token: {e.response.content}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching Instagram token: {e}")
