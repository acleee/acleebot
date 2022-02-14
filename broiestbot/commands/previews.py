"""Extract URL from user chat message."""
import re
from typing import Optional

from metadata_parser import MetadataParser
from requests.exceptions import HTTPError

from logger import LOGGER

headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "3600",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
}


def extract_url(chat_message: str) -> Optional[str]:
    """
    Determine if a user chat is a raw URL; used to generate link previews.

    :param str chat_message: Chatango message sent by a user potentially containing a URL.

    :returns: Optional[str]
    """
    pattern = r"^http?(s)://(.+)"
    url_match = re.match(pattern, chat_message)
    if url_match is not None:
        url = url_match.group(0)
        if (
            ".jpg" not in url
            and ".png" not in url
            and ".gif" not in url
            and ".jpeg" not in url
            and ".mp4" not in url
        ):
            return scrape_metadata_from_url(url)


def scrape_metadata_from_url(url: str) -> Optional[str]:
    """
    Fetch metadata for a given URL.

    :param str url: Link to third-party content, for which to create a link preview.

    :returns: Optional[str]
    """
    try:
        # Parse page metadata as dict
        page = MetadataParser(url=url, url_headers=headers, search_head_only=True)
        page_meta = page.metadata["meta"]
        return create_link_preview(page, page_meta, url)
    except HTTPError as e:
        LOGGER.warning(f"Failed to fetch metadata for URL `{url}`: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error while scraping metadata for URL `{url}`: {e}")


def create_link_preview(page: MetadataParser, page_meta: dict, url: str) -> Optional[str]:
    """
    Create a preview bookmark card from a URL.

    :param MetadataParser page: Page object create from URL to be parsed.
    :param dict page_meta: Page metadata parsed from the head of the target URL.
    :param str url: URL of the linked third-party post/article.

    :returns: Optional[str]
    """
    try:
        title = page_meta.get("og:title")
        description = page_meta.get("og:description")
        image = page.get_metadata_link("image", allow_encoded_uri=True, require_public_global=True)
        author = page_meta.get("author")
        publisher = page_meta.get("publisher")
        icons = page.soup.select("link[rel=icon]")
        page_type = page_meta.get("og:type")
        if title is not None and description is not None:
            preview = f"\n\n<b>{title}</b>\n{description}\n{url}"
            if page_type:
                preview += f"\n{page_type.title()}"
            if image:
                preview += f"\n{image}"
            return preview
    except Exception as e:
        LOGGER.error(f"Unexpected error while generating link preview card: {e}")
