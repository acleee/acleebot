from googleapiclient.errors import HttpError

from clients import yt
from logger import LOGGER


def search_youtube_for_video(query: str) -> str:
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
        LOGGER.error(f"Error while fetching YouTube video: {e}")
