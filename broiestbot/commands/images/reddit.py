"""Fetch random trending image from a given subreddit."""
from emoji import emojize
from praw.exceptions import RedditAPIException

from clients import reddit
from logger import LOGGER


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
