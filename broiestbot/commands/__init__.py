"""Construct responses to bot commands from third-party APIs."""
from .afterdark import get_redgifs_gif
from .definitions import get_urban_definition, wiki_summary
from .embeds import create_instagram_preview
from .footy import (
    epl_standings,
    footy_live_fixtures,
    footy_predicts_today,
    footy_upcoming_fixtures,
    golden_boot,
)
from .images import (
    fetch_image_from_gcs,
    giphy_image_search,
    random_image,
    subreddit_image,
)
from .markets import get_crypto, get_stock
from .misc import blaze_time_remaining, covid_cases_usa, send_text_message
from .movies import find_imdb_movie
from .weather import weather_by_location


def basic_message(message):
    """Send basic text message to room."""
    return message
