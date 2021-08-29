"""Bot configuration variables."""
from os import environ, getenv, path

from dotenv import load_dotenv

BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, ".env"))

# Environment
ENVIRONMENT = getenv("ENVIRONMENT")

# Chatango rooms
CHATANGO_TEST_ROOM = getenv("CHATANGO_TEST_ROOM")
CHATANGO_ACLEE_ROOM = getenv("CHATANGO_ACLEE_ROOM")
CHATANGO_BLAB_ROOM = getenv("CHATANGO_BLAB_ROOM")
CHATANGO_SIXERS_ROOM = getenv("CHATANGO_SIXERS_ROOM")
CHATANGO_EAGLES_ROOM = getenv("CHATANGO_EAGLES_ROOM")
CHATANGO_PHILLIES_ROOM = getenv("CHATANGO_PHILLIES_ROOM")
CHATANGO_NFL_ROOM = getenv("CHATANGO_NFL_ROOM")
CHATANGO_OBI_ROOM = getenv("CHATANGO_OBI_ROOM")
CHATANGO_DUBS_ROOM = getenv("CHATANGO_DUBS_ROOM")
CHATANGO_REDZONE_ROOM = getenv("CHATANGO_REDZONE_ROOM")
CHATANGO_FLYERS_ROOM = getenv("CHATANGO_FLYERS_ROOM")
CHATANGO_UFC_ROOM = getenv("CHATANGO_UFC_ROOM")
CHATANGO_ROOMS = [
    CHATANGO_ACLEE_ROOM,
    CHATANGO_SIXERS_ROOM,
    CHATANGO_PHILLIES_ROOM,
    CHATANGO_FLYERS_ROOM,
    CHATANGO_EAGLES_ROOM,
    # CHATANGO_NFL_ROOM,
    CHATANGO_OBI_ROOM,
    # CHATANGO_REDZONE_ROOM,
    CHATANGO_UFC_ROOM,
]

# Chatango credentials
CHATANGO_BOT_USERNAME = getenv("CHATANGO_BOT_USERNAME")
CHATANGO_BOT_PASSWORD = getenv("CHATANGO_BOT_PASSWORD")
CHATANGO_BRO_USERNAME = getenv("CHATANGO_BRO_USERNAME")
CHATANGO_BRO_PASSWORD = getenv("CHATANGO_BRO_PASSWORD")

# Chatango users with additional features
CHATANGO_SPECIAL_USERS = getenv("CHATANGO_SPECIAL_USERS")
if CHATANGO_SPECIAL_USERS:
    CHATANGO_SPECIAL_USERS = CHATANGO_SPECIAL_USERS.split(",")

# Users to be banned on sight
CHATANGO_BLACKLISTED_USERS = getenv("CHATANGO_BLACKLISTED_USERS")

# Database
DATABASE_URI = getenv("DATABASE_URI")
DATABASE_USERS_TABLE = getenv("DATABASE_USERS_TABLE")
DATABASE_ARGS = {"ssl": {"ca": f"{BASE_DIR}/creds/ca-certificate.crt"}}

# Google Cloud
GOOGLE_APPLICATION_CREDENTIALS = "gcloud.json"
GOOGLE_BUCKET_NAME = getenv("GOOGLE_BUCKET_NAME")
GOOGLE_BUCKET_URL = getenv("GOOGLE_BUCKET_URL")

# Gifs
GIPHY_API_KEY = getenv("GIPHY_API_KEY")
GFYCAT_CLIENT_ID = getenv("GFYCAT_CLIENT_ID")
GFYCAT_CLIENT_SECRET = getenv("GFYCAT_CLIENT_SECRET")
REDGIFS_ACCESS_KEY = getenv("REDGIFS_ACCESS_KEY")

# Stock
IEX_API_TOKEN = getenv("IEX_API_TOKEN")
IEX_API_BASE_URL = "https://cloud.iexapis.com/stable/stock/"

# Crypto
ALPHA_VANTAGE_API_KEY = environ.get("ALPHA_VANTAGE_API_KEY")
ALPHA_VANTAGE_PRICE_BASE_URL = "https://api.cryptowat.ch/markets/bitfinex/"
ALPHA_VANTAGE_CHART_BASE_URL = "https://www.alphavantage.co/query/"

# Plotly
PLOTLY_API_KEY = getenv("PLOTLY_API_KEY")
PLOTLY_USERNAME = getenv("PLOTLY_USERNAME")
PLOTLY_ALT_API_KEY = getenv("PLOTLY_ALT_API_KEY")
PLOTLY_ALT_USERNAME = getenv("PLOTLY_ALT_USERNAME")

# Weather
WEATHERSTACK_API_ENDPOINT = "http://api.weatherstack.com/current"
WEATHERSTACK_API_KEY = getenv("WEATHERSTACK_API_KEY")
METRIC_SYSTEM_USERS = getenv("METRIC_SYSTEM_USERS")

# Email
GMAIL_EMAIL = getenv("GMAIL_EMAIL")
GMAIL_PASSWORD = getenv("GMAIL_PASSWORD")

# Twilio
TWILIO_SENDER_PHONE = getenv("TWILIO_SENDER_PHONE")
TWILIO_RECIPIENT_PHONE = getenv("TWILIO_RECIPIENT_PHONE")
TWILIO_AUTH_TOKEN = getenv("TWILIO_AUTH_TOKEN")
TWILIO_ACCOUNT_SID = getenv("TWILIO_ACCOUNT_SID")

# Reddit
REDDIT_CLIENT_ID = getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = getenv("REDDIT_CLIENT_SECRET")
REDDIT_PASSWORD = getenv("REDDIT_CLIENT_SECRET")

# Rapid API
RAPID_API_KEY = getenv("RAPID_API_KEY")

# IP Data
IP_DATA_KEY = getenv("IP_DATA_KEY")

# Instagram
INSTAGRAM_USERNAME = getenv("INSTAGRAM_USERNAME")
INSTAGRAM_PASSWORD = getenv("INSTAGRAM_PASSWORD")
INSTAGRAM_APP_ID = getenv("INSTAGRAM_APP_ID")
INSTAGRAM_APP_SECRET = getenv("INSTAGRAM_APP_SECRET")

# Lyrics Genius
GENIUS_KEY_ID = getenv("GENIUS_KEY_ID")
GENIUS_ACCESS_TOKEN = getenv("GENIUS_KEY_SECRET")

# Youtube
YOUTUBE_API_KEY = getenv("YOUTUBE_API_KEY")

TWITCH_CLIENT_ID = getenv("TWITCH_CLIENT_ID")
TWITCH_CLIENT_SECRET = getenv("TWITCH_CLIENT_SECRET")
TWITCH_BROADCASTER_ID = getenv("TWITCH_BROADCASTER_ID")
TWITCH_USER_LOGIN = getenv("TWITCH_USER_LOGIN")

# Rapid API Headers to send with every request
FOOTY_BASE_URL = "https://api-football-v1.p.rapidapi.com/v3"
FOOTY_FIXTURES_ENDPOINT = f"{FOOTY_BASE_URL}/fixtures"
FOOTY_LIVE_FIXTURE_EVENTS_ENDPOINT = f"{FOOTY_BASE_URL}/fixtures/events"
FOOTY_PREDICTS_ENDPOINT = f"{FOOTY_BASE_URL}/predictions"
FOOTY_TOPSCORERS_ENDPOINT = f"{FOOTY_BASE_URL}/players/topscorers"
FOOTY_STANDINGS_ENDPOINT = f"{FOOTY_BASE_URL}/standings"


FOOTY_HTTP_HEADERS = {
    "content-type": "application/json",
    "x-rapidapi-key": RAPID_API_KEY,
    "x-rapidapi-host": "api-football-v1.p.rapidapi.com",
}

# 2020-2021 Footy Leagues
EPL_LEAGUE_ID = 39
UCL_LEAGUE_ID = 2
FA_CUP_ID = 45
EFL_CUP_ID = 46
LEAGUE_ONE_ID = 41
EUROPA_LEAGUE_ID = 2777
UEFA_EUROPA_ID = 3
BUND_LEAGUE_ID = 78
LIGA_LEAGUE_ID = 140
EUROS_LEAGUE_ID = 4
COPA_LEAGUE_ID = 9
LIGUE_ONE_LEAGUE_ID = 61
FRIENDLIES_LEAGUE_ID = 667
WORLDCUP_LEAGUE_ID = 15
MLS_LEAGUE_ID = 253
CONCACAF_LEAGUE_ID = 767
CONCACAF_GOLD_CUP_ID = 22
CONCACAF_CHAMPIONS_LEAGUE = 16
OLYMPICS_MEN_LEAGUE_ID = 480
OLYMPICS_WOMEN_LEAGUE_ID = 524
WORLD_CUP_ID = 1
WC_QUALIFIERS_CONCACAF = 31
WC_QUALIFIERS_EUROPE = 32
SERIE_A_LEAGUE_ID = 135
COMMUNITY_SHIELD_CUP = 528

# Footy team IDs
LIVERPOOL_TEAM_ID = 33
FOXES_TEAM_ID = 46

FOOTY_LEAGUES = {
    # ":sports_medal: OLYMPICS MEN": OLYMPICS_MEN_LEAGUE_ID,
    # ":sports_medal: OLYMPICS WOMEN": OLYMPICS_WOMEN_LEAGUE_ID,
    # ":world_map: WORLD CUP QUALIFIERS CONCACAF": WC_QUALIFIERS_CONCACAF,
    # ":world_map: WORLD CUP QUALIFIERS EUROPE": WC_QUALIFIERS_EUROPE,
    ":lion: EPL": EPL_LEAGUE_ID,
    ":trophy: UCL": UCL_LEAGUE_ID,
    # ":England: FA": FA_CUP_ID,
    # ":England: EFL": EFL_CUP_ID,
    ":European_Union: EUROPA": EUROPA_LEAGUE_ID,
    ":Spain: LIGA": LIGA_LEAGUE_ID,
    ":Germany: BUND": BUND_LEAGUE_ID,
    ":Italy: Serie A": SERIE_A_LEAGUE_ID,
    ":European_Union: EUROS": EUROS_LEAGUE_ID,
    ":France: Ligue 1": LIGUE_ONE_LEAGUE_ID,
    # ":trophy: WORLD": WORLDCUP_LEAGUE_ID,
    ":United_States: MLS": MLS_LEAGUE_ID,
    # ":England: LEAGUE ONE": LEAGUE_ONE_ID,
    # ":world_map: WORLD CUP": WORLD_CUP_ID,
    # ":trophy: COMMUNITY": COMMUNITY_SHIELD_CUP,
    # ":smiley: FRIENDLIES": FRIENDLIES_LEAGUE_ID,
    # ":globe_showing_Americas: COPA": COPA_LEAGUE_ID,
    # ":globe_showing_Americas: CONCACAF LEAGUE": CONCACAF_LEAGUE_ID,
    # ":globe_showing_Americas: CONCACAF GOLD CUP": CONCACAF_GOLD_CUP_ID,
    # ":globe_showing_Americas: CONCACAF CHAMPIONS": CONCACAF_CHAMPIONS_LEAGUE,
}

FOOTY_LEAGUES_PRIORITY = {
    ":lion: EPL": EPL_LEAGUE_ID,
    ":Spain: LIGA": LIGA_LEAGUE_ID,
    ":Germany: BUND": BUND_LEAGUE_ID,
    ":Italy: Serie A": SERIE_A_LEAGUE_ID,
    ":United_States: MLS": MLS_LEAGUE_ID,
}
