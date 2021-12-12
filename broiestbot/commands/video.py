from datetime import datetime
from typing import Optional

import requests
from emoji import emojize

# from clients import yt
# from googleapiclient.errors import HttpError
from requests.exceptions import HTTPError

from config import (
    TWITCH_BROADCASTERS,
    TWITCH_CLIENT_ID,
    TWITCH_CLIENT_SECRET,
    TWITCH_STREAMS_ENDPOINT,
    TWITCH_TOKEN_ENDPOINT,
)
from logger import LOGGER


def get_all_live_twitch_streams():
    token = get_twitch_auth_token()
    twitch_streams = []
    i = 0
    for user, broadcaster_id in TWITCH_BROADCASTERS.items():
        stream = get_live_twitch_stream(broadcaster_id, token)
        if bool(stream):
            i += 1
            twitch_streams.append(stream)
            if i == 1:
                twitch_streams.insert(0, "\n\n\n\n")
            if len(twitch_streams) > 2:
                return "\n-----------------------\n".join(twitch_streams)
            return "".join(twitch_streams)
    return emojize(
        f":frowning: no memers streaming twitch rn :frowning:",
        use_aliases=True,
    )


def get_live_twitch_stream(broadcaster_id: str, token: str) -> Optional[str]:
    """
    Check if Twitch user is live streaming and return stream info.

    :param str broadcaster_id: Twitch ID of broadcaster to check for a live stream.
    :param str token: Bearer token for fetching twitch streams.

    :returns: str
    """
    try:
        endpoint = TWITCH_STREAMS_ENDPOINT

        params = {"user_id": broadcaster_id}
        headers = {
            "Authorization": f"Bearer {token}",
            "client-id": TWITCH_CLIENT_ID,
            "Accept": "application/vnd.twitchtv.v5+json",
        }
        req = requests.get(endpoint, params=params, headers=headers)
        resp = req.json().get("data")
        if bool(resp):
            return format_twitch_response(resp[0])
        return None
    except HTTPError as e:
        LOGGER.error(f"HTTPError when fetching Twitch channel: {e.response.content}")
    except IndexError as e:
        LOGGER.error(f"IndexError when fetching Twitch channel: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching Twitch channel: {e}")


def format_twitch_response(stream: dict) -> str:
    """
    Construct chat message containing stream info.

    :param dict stream: Live Twitch stream metadata.

    :returns: str
    """
    broadcaster = stream.get("user_name")
    game = stream.get("game_name")
    title = stream.get("title")
    viewers = stream.get("viewer_count")
    start_time = stream.get("started_at").replace("Z", "")
    duration = (datetime.utcnow() - datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S")).seconds / 60
    thumbnail = stream.get("thumbnail_url").replace("{width}", "550").replace("{height}", "300")
    url = f"https://www.twitch.tv/{broadcaster}"
    return f"\n\n\n<b>{broadcaster}</b> is streaming <b>{game}</b>\n<i>{title}</i>\n{viewers} viewers, {int(duration)} minutes\n{url}\n\n{thumbnail}"


def get_twitch_auth_token() -> Optional[str]:
    """
    Generate Twitch auth token prior to fetching live streams.

    :returns: str
    """
    try:
        endpoint = TWITCH_TOKEN_ENDPOINT
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
