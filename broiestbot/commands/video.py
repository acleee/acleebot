import requests
# from googleapiclient.errors import HttpError
from requests.exceptions import HTTPError

from config import TWITCH_BROADCASTER_ID, TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET

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
    endpoint = "https://api.twitch.tv/helix/channels"
    token = get_twitch_auth_token()
    params = {"broadcaster_id": TWITCH_BROADCASTER_ID, "user_login": "broiestbro"}
    headers = {"Authorization": f"Bearer {token}"}
    try:
        req = requests.get(endpoint, params=params, headers=headers)
        resp = req.json().get("data")
        if resp:
            return resp
    except HTTPError as e:
        LOGGER.error(f"HTTPError when fetching Twitch stream: {e.response.content}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching Twitch stream: {e}")
        
        
def get_twitch_channel_info():
    endpoint = "https://api.twitch.tv/helix/channels"
    token = get_twitch_auth_token()
    params = {"broadcaster_id": TWITCH_BROADCASTER_ID, "user_login": "broiestbro"}
    headers = {"Authorization": f"Bearer {token}"}
    try:
        req = requests.get(endpoint, params=params, headers=headers)
        resp = req.json().get("data")
        if resp:
            return resp
    except HTTPError as e:
        LOGGER.error(f"HTTPError when fetching Twitch channel: {e.response.content}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching Twitch channel: {e}")


def get_twitch_auth_token():
    try:
        endpoint = "https://id.twitch.tv/oauth2/token"
        params = {
            "client_id": TWITCH_CLIENT_ID,
            "client_secret": TWITCH_CLIENT_SECRET,
            "grant_type": "client_credentials",
        }
        resp = requests.get(endpoint, params=params)
        return resp.json().get("access_token")
    except HTTPError as e:
        LOGGER.error(f"HTTPError when fetching Twitch auth token: {e.response.content}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching Twitch auth token: {e}")
