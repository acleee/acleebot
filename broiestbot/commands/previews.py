"""Extract URL from user chat message."""
import re
from typing import Optional, Tuple

from metadata_parser import InvalidDocument, MetadataParser
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
            and ".JPG" not in url
            and ".PNG" not in url
            and ".GIF" not in url
            and ".JPEG" not in url
            and ".MP4" not in url
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
        page = MetadataParser(
            url=url,
            url_headers=headers,
            search_head_only=True,
            only_parse_http_ok=True,
            raise_on_invalid=True,
        )
        page_meta = page.parsed_result.metadata
        LOGGER.info(f"page_meta = {page_meta}")
        return create_link_preview(page, page_meta, url)
    except HTTPError as e:
        LOGGER.warning(f"Failed to fetch metadata for URL `{url}`: {e}")
    except InvalidDocument as e:
        LOGGER.warning(f"InvalidDocument encountered while fetching metadata for URL `{url}`: {e}")
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
        title, description, page_type = parse_scraped_metadata(page_meta)
        image = page.get_metadata_link("image", allow_encoded_uri=True, require_public_global=True)
        if title is not None and description is not None:
            preview = f"\n\n<b>{title}</b>\n{description}\n{url}"
            if page_type:
                preview += f"\n{page_type.title()}"
            if image:
                preview += f"\n{image}"
            return preview
    except Exception as e:
        LOGGER.error(f"Unexpected error while generating link preview card: {e}")


def parse_scraped_metadata(page_meta: dict) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Parse HTML metadata with added redundancy.

    :param dict page_meta: Metadata stored as dictionary of `og`, `twitter`, `meta`, and `page`.

    :returns: Tuple[Optional[str], Optional[str], Optional[str]]
    """
    title = None
    description = None
    page_type = None
    if page_meta.get("meta") is not None:
        title = page_meta["meta"].get("og:title")
        description = page_meta["meta"].get("og:description")
        page_type = page_meta["meta"].get("og:type")
    if page_meta.get("og") is not None:
        title = page_meta["og"].get("title") if title is None else None
        description = page_meta["og"].get("description") if description is None else None
    if page_meta.get("twitter") is not None:
        title = page_meta["twitter"].get("title") if title is None else None
        description = page_meta["twitter"].get("description") if description is None else None
    return title, description, page_type
