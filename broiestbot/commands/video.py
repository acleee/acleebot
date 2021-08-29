from datetime import datetime

import requests
from emoji import emojize

# from googleapiclient.errors import HttpError
from requests.exceptions import HTTPError

from config import (
    TWITCH_BROADCASTER_ID,
    TWITCH_CLIENT_ID,
    TWITCH_CLIENT_SECRET,
    TWITCH_USER_LOGIN,
)

# from clients import yt
from logger import LOGGER

'''def search_youtube_for_video(query: str) -> str:
    """
    Search for a Youtube video.

    :param str query: Query to fetch most relevant YouTube Video.

    :returns: str
    """
    try:
        request = yt.search().list(
            part="snippet", q=query, maxResults=1, safeSearch=None
        )
        response = request.execute()
        LOGGER.info(response)
        return response
    except HttpError as e:
        LOGGER.error(f"HttpError while fetching YouTube video: {e}")
    except Exception as e:
        LOGGER.error(f"Error while fetching YouTube video: {e}")'''


def get_live_twitch_stream():
    """Check if Twitch user is live streaming and return stream info."""
    endpoint = "https://api.twitch.tv/helix/streams"
    token = get_twitch_auth_token()
    params = {"user_id": TWITCH_BROADCASTER_ID}
    headers = {
        "Authorization": f"Bearer {token}",
        "client-id": TWITCH_CLIENT_ID,
        "Accept": "application/vnd.twitchtv.v5+json",
    }
    try:
        req = requests.get(endpoint, params=params, headers=headers)
        resp = req.json().get("data")[0]
        if resp:
            broadcaster = resp.get("user_name")
            game = resp.get("game_name")
            title = resp.get("title")
            viewers = resp.get("viewer_count")
            start_time = resp.get("started_at").replace("Z", "")
            duration = (
                datetime.utcnow() - datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S")
            ).seconds / 60
            thumbnail = (
                resp.get("thumbnail_url")
                .replace("{width}", "550")
                .replace("{height}", "300")
            )
            url = f"https://www.twitch.tv/{broadcaster}"
            return f"\n\n\n{broadcaster.upper()} is streaming {game}\n{title}\n{viewers} viewers, {int(duration)} minutes\n{url}\n\n{thumbnail}"
        return emojize(
            f":frowning: no memers streaming twitch rn :frowning:",
            use_aliases=True,
        )
    except HTTPError as e:
        LOGGER.error(f"HTTPError when fetching Twitch channel: {e.response.content}")
        return emojize(
            f":frowning: no memers streaming twitch rn :frowning:",
            use_aliases=True,
        )
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching Twitch channel: {e}")
        return emojize(
            f":frowning: no memers streaming twitch rn :frowning:",
            use_aliases=True,
        )


def get_twitch_auth_token() -> str:
    """Generate Twitch auth token."""
    try:
        endpoint = "https://id.twitch.tv/oauth2/token"
        params = {
            "client_id": TWITCH_CLIENT_ID,
            "client_secret": TWITCH_CLIENT_SECRET,
            "grant_type": "client_credentials",
        }
        resp = requests.post(endpoint, params=params)
        return resp.json().get("access_token")
    except HTTPError as e:
        LOGGER.error(f"HTTPError when fetching Twitch auth token: {e.response.content}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching Twitch auth token: {e}")
