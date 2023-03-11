"""Generate link previews from URLs."""
from typing import Optional
from datetime import datetime

import requests
from requests.models import Request
import re
from bs4 import BeautifulSoup
from requests import Response
from requests.exceptions import HTTPError
from emoji import emojize

from config import INSTAGRAM_APP_ID, HTTP_REQUEST_TIMEOUT, TWITTER_BEARER_TOKEN
from logger import LOGGER


def generate_twitter_preview(message: str) -> Optional[str]:
    """
    Check chat message for Twitter URL and generate preview.

    :param str message: Chatango message to check for Twitter URL.

    :returns: Optional[str]
    """
    try:
        twitter_match = re.search(r"^https://twitter.com/[a-zA-Z0-9_]+/status/([0-9]+)", message)
        if twitter_match:
            tweet_id = twitter_match.group(1)
            tweet_response = fetch_tweet_by_id(tweet_id)
            if tweet_response:
                LOGGER.success(f"Created Twitter link preview for Tweet: ({message})")
                return parse_tweet_preview(tweet_response, tweet_id)
        return None
    except Exception as e:
        LOGGER.error(f"Unexpected error while creating Twitter embed: {e}")


def fetch_tweet_by_id(tweet_id: str) -> Optional[dict]:
    """
    Fetch Tweet JSON by Tweet ID.

    :param str tweet_id: Tweet ID to fetch.

    :returns: Optional[dict]
    """
    try:
        params = {
            "tweet.fields": "created_at,attachments",
            "expansions": "author_id,attachments.media_keys",
            "media.fields": "url,alt_text",
            "user.fields": "url",
        }
        endpoint = f"https://api.twitter.com/2/tweets/{tweet_id}"
        resp = requests.get(endpoint, auth=twitter_bearer_oauth, params=params)
        if resp.status_code == 200:
            return resp
    except HTTPError as e:
        LOGGER.error(f"HTTPError error while fetching Tweet by ID ({tweet_id}): {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error while fetching Tweet by ID ({tweet_id}): {e}")


def parse_tweet_preview(response: Response, tweet_id: str) -> Optional[str]:
    """
    Create formatted Tweet preview chat message from JSON response.

    :param Response response: Prepared API request to fetch Tweet from Twitter API.
    :param str tweet_id: Tweet ID to fetch.

    :returns: Optional[str]
    """
    try:
        tweet_data = response.json()["data"]
        tweet_body = tweet_data["text"]
        tweet_date = tweet_data["created_at"].replace(".000Z", "")
        tweet_date_formatted = emojize(
            f":calendar: {datetime.strptime(tweet_date, '%Y-%m-%dT%H:%M:%S')}", language="en"
        )
        tweet_users = response.json()["includes"]["users"]
        tweet_author_name = tweet_users[0]["name"]
        tweet_author_username = tweet_users[0]["username"]
        # tweet_author_url = tweet_users[0]["url"]
        tweet_url = f"https://twitter.com/{tweet_author_username}/status/{tweet_id}"
        tweet_attachments = response.json()["includes"].get("media")
        if tweet_attachments:
            tweet_images = [attachment["url"] for attachment in tweet_attachments if attachment["type"] == "photo"]
            return emojize(
                f"\n\n:bust_in_silhouette: <b>{tweet_author_name}</b> <i>@{tweet_author_username}</i>\n{tweet_date_formatted}\n\n{tweet_body}\n\n{' '.join(tweet_images)}\n\n{tweet_url}",
                language="en",
            )
        return emojize(
            f"\n\n:bust_in_silhouette: <b>{tweet_author_name}</b> <i>@{tweet_author_username}</i>\n{tweet_date_formatted}\n\n{tweet_body}\n\n{tweet_url}",
            language="en",
        )
    except KeyError as e:
        LOGGER.error(f"KeyError while parsing Tweet: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error while parsing Tweet: {e}")


def twitter_bearer_oauth(req: Request) -> Request:
    """
    Method required by bearer token authentication.
    """
    req.headers["Authorization"] = f"Bearer {TWITTER_BEARER_TOKEN}"
    req.headers["User-Agent"] = "v2TweetLookupPython"
    return req


def create_instagram_preview(url: str) -> Optional[str]:
    """
    Generate link preview for Instagram post URLs.

    :param str url: Instagram post URL (image or video).

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
        req = requests.get(url, headers=headers, timeout=HTTP_REQUEST_TIMEOUT)
        html = BeautifulSoup(req.content, "html.parser")
        img_tag = html.find("meta", property="og:image")
        if img_tag is not None:
            img = img_tag.get("content")
            description = html.find("title").get_text()
            return f"{img} {description}"
        return None
    except HTTPError as e:
        LOGGER.error(f"HTTPError while fetching Instagram URL `{url}`: {e.response.content}")
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
        return requests.post(f"https://www.facebook.com/x/oauth/status", params=params, timeout=HTTP_REQUEST_TIMEOUT)
    except HTTPError as e:
        LOGGER.error(f"HTTPError while fetching Instagram token: {e.response.content}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching Instagram token: {e}")
