from os import environ

import googleapiclient.discovery
import googleapiclient.errors
from config import ENVIRONMENT, YOUTUBE_API_KEY


def youtube_client():
    # Disable OAuthlib's HTTPS verification when running locally.
    if ENVIRONMENT == "development":
        environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
    api_service_name = "youtube"
    api_version = "v3"

    # Get credentials and create an API client
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=YOUTUBE_API_KEY)

    return youtube


yt = youtube_client()
