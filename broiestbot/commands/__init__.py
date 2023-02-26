"""Construct responses to bot commands from third-party APIs."""
from .afterdark import get_redgifs_gif
from .definitions import (
    get_english_definition,
    get_english_translation,
    get_urban_definition,
    wiki_summary,
)
from .embeds import create_instagram_preview
from .footy import (
    all_leagues_golden_boot,
    epl_golden_boot,
    fetch_fox_fixtures,
    footy_all_upcoming_fixtures,
    footy_live_fixtures,
    footy_predicts_today,
    footy_team_lineups,
    footy_upcoming_fixtures,
    get_footy_odds,
    today_upcoming_fixtures,
    league_table_standings,
    footy_live_fixture_stats,
)
from .images import (
    fetch_image_from_gcs,
    gcs_count_images_in_bucket,
    gcs_random_image_spam,
    giphy_image_search,
    random_image,
    subreddit_image,
)
from .lyrics import get_song_lyrics
from .markets import get_crypto_chart, get_crypto_price, get_stock, get_top_crypto
from .misc import (
    blaze_time_remaining,
    covid_cases_usa,
    send_text_message,
    time_until_wayne,
)
from .mlb import today_phillies_games
from .movies import find_imdb_movie
from .nba import live_nba_games, nba_standings, upcoming_nba_games
from .nfl import get_live_nfl_games
from .olympics import get_summer_olympic_medals, get_winter_olympic_medals
from .polls import change_or_stay_vote, tovala_counter
from .previews import extract_url
from .tuner import get_current_show, tuner

# from .video import search_youtube_for_video
from .video import get_all_live_twitch_streams
from .weather import weather_by_location
from .playstation import get_psn_online_friends


def basic_message(message):
    """Send basic text message to room."""
    return message
