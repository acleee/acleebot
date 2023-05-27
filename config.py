"""Bot configuration variables."""
from os import environ, getenv, path

import pytz
from dotenv import load_dotenv

BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, ".env"))

# General
# -------------------------------------------------
ENVIRONMENT = getenv("ENVIRONMENT")
TIMEZONE_US_EASTERN = pytz.timezone("America/New_York")

# Chatango
# -------------------------------------------------

# Chatango bot credentials
CHATANGO_USERS = {
    "BROIESTBOT": {
        "USERNAME": getenv("CHATANGO_BOT_USERNAME"),
        "PASSWORD": getenv("CHATANGO_BOT_PASSWORD"),
    },
    "BROIESTBRO": {
        "USERNAME": getenv("CHATANGO_BRO_USERNAME"),
        "PASSWORD": getenv("CHATANGO_BRO_PASSWORD"),
    },
}

# Known Chatango bot usernames
CHATANGO_BOTS = ["BROIESTBRO", "BROIESTBOT", "ACLEEBOT", "LMAOLOVER"]

# All known Chatango rooms
CHATANGO_TEST_ROOM = getenv("CHATANGO_TEST_ROOM")
CHATANGO_ACLEE_ROOM = getenv("CHATANGO_ACLEE_ROOM")
CHATANGO_SIXERS_ROOM = getenv("CHATANGO_SIXERS_ROOM")
CHATANGO_ALT_ROOM = getenv("CHATANGO_ALT_ROOM")
CHATANGO_PHILLIES_ROOM = getenv("CHATANGO_PHILLIES_ROOM")
CHATANGO_NFL_ROOM = getenv("CHATANGO_NFL_ROOM")
CHATANGO_OBI_ROOM = getenv("CHATANGO_OBI_ROOM")
CHATANGO_REDZONE_ROOM = getenv("CHATANGO_REDZONE_ROOM")
CHATANGO_PATREON_ROOM = getenv("CHATANGO_PATREON_ROOM")
CHATANGO_FLYERS_ROOM = getenv("CHATANGO_FLYERS_ROOM")
CHATANGO_UFC_ROOM = getenv("CHATANGO_UFC_ROOM")
CHATANGO_UNION_ROOM = getenv("CHATANGO_UNION_ROOM")

# Chatango rooms to be joined by the bot
CHATANGO_ROOMS = [
    CHATANGO_ACLEE_ROOM,
    CHATANGO_SIXERS_ROOM,
    CHATANGO_PHILLIES_ROOM,
    # CHATANGO_FLYERS_ROOM,
    CHATANGO_ALT_ROOM,
    # CHATANGO_NFL_ROOM,
    CHATANGO_OBI_ROOM,
    # CHATANGO_REDZONE_ROOM,
    # CHATANGO_PATREON_ROOM,
    CHATANGO_UFC_ROOM,
    # CHATANGO_UNION_ROOM,
]

# List of Chatango users with privileges to special commands
CHATANGO_SPECIAL_USERS = getenv("CHATANGO_SPECIAL_USERS")
if CHATANGO_SPECIAL_USERS:
    CHATANGO_SPECIAL_USERS = CHATANGO_SPECIAL_USERS.split(",")

# Chatango users to be banned or ignored
CHATANGO_IGNORED_USERS = getenv("CHATANGO_IGNORED_USERS")
CHATANGO_IGNORED_IPS = getenv("CHATANGO_IGNORED_IPS")
CHATANGO_BANNED_IPS = getenv("CHATANGO_BANNED_IPS")
CHATANGO_EGGSER_USERNAME_WHITELIST = getenv("CHATANGO_EGGSER_USERNAME_WHITELIST")
CHATANGO_BLACKLISTED_USERS = getenv("CHATANGO_BLACKLISTED_USERS")
CHATANGO_BLACKLIST_ROOMS = [
    CHATANGO_ACLEE_ROOM,
    CHATANGO_SIXERS_ROOM,
    CHATANGO_PHILLIES_ROOM,
    CHATANGO_FLYERS_ROOM,
    CHATANGO_ALT_ROOM,
    CHATANGO_NFL_ROOM,
    CHATANGO_REDZONE_ROOM,
    CHATANGO_PATREON_ROOM,
    CHATANGO_UFC_ROOM,
    CHATANGO_UNION_ROOM,
]

# Database
# -------------------------------------------------
SQLALCHEMY_DATABASE_URI = getenv("SQLALCHEMY_DATABASE_URI")
DATABASE_USERS_TABLE = getenv("DATABASE_USERS_TABLE")
DATABASE_ARGS = {"ssl": {"ca": f"{BASE_DIR}/creds/ca-certificate.crt"}}

# Redis
# -------------------------------------------------
REDIS_HOST = getenv("REDIS_HOST")
REDIS_USERNAME = getenv("REDIS_USERNAME")
REDIS_PASSWORD = getenv("REDIS_PASSWORD")
REDIS_PORT = getenv("REDIS_PORT")
REDIS_DB = getenv("REDIS_DB")

# Datadog
# -------------------------------------------------
DDOG_APP_KEY = getenv("DDOG_APP_KEY")
DDOG_API_KEY = getenv("DDOG_API_KEY")

# User Logging
# -------------------------------------------------
PERSIST_USER_DATA = True
PERSIST_CHAT_DATA = True

# APIs
HTTP_REQUEST_TIMEOUT = 20

# Google Cloud
# -------------------------------------------------
GOOGLE_APPLICATION_CREDENTIALS = "gcloud.json"
GOOGLE_BUCKET_NAME = getenv("GOOGLE_BUCKET_NAME")
GOOGLE_BUCKET_URL = getenv("GOOGLE_BUCKET_URL")

# Google Translate
GOOGLE_TRANSLATE_ENDPOINT = "https://google-translate1.p.rapidapi.com/language/translate/v2"
GOOGLE_TRANSLATE_API_KEY = getenv("GOOGLE_TRANSLATE_API_KEY")

# Urban Dictionary
# -------------------------------------------------
URBAN_DICTIONARY_ENDPOINT = "http://api.urbandictionary.com/v0/define"

# Gifs
# -------------------------------------------------
GIPHY_API_KEY = getenv("GIPHY_API_KEY")
REDGIFS_ACCESS_KEY = getenv("REDGIFS_ACCESS_KEY")
REDGIFS_TOKEN_ENDPOINT = "https://weblogin.redgifs.com/oauth/webtoken"
REDGIFS_IMAGE_SEARCH_ENDPOINT = "https://api.redgifs.com/v2/gifs/search"

# Stocks
# -------------------------------------------------
IEX_API_TOKEN = getenv("IEX_API_TOKEN")
IEX_API_BASE_URL = "https://cloud.iexapis.com/stable/stock/"

# Crypto
# -------------------------------------------------
ALPHA_VANTAGE_API_KEY = environ.get("ALPHA_VANTAGE_API_KEY")
ALPHA_VANTAGE_PRICE_BASE_URL = "https://api.cryptowat.ch/markets/bitfinex/"
ALPHA_VANTAGE_CHART_BASE_URL = "https://www.alphavantage.co/query/"
COINMARKETCAP_LATEST_ENDPOINT = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
COINMARKETCAP_API_KEY = getenv("COINMARKETCAP_API_KEY")

# Plotly
# -------------------------------------------------
PLOTLY_API_KEY = getenv("PLOTLY_API_KEY")
PLOTLY_USERNAME = getenv("PLOTLY_USERNAME")

# Weather
# -------------------------------------------------
WEATHERSTACK_API_ENDPOINT = "http://api.weatherstack.com/current"
WEATHERSTACK_API_KEY = getenv("WEATHERSTACK_API_KEY")
METRIC_SYSTEM_USERS = getenv("METRIC_SYSTEM_USERS")

# Email
# -------------------------------------------------
GMAIL_EMAIL = getenv("GMAIL_EMAIL")
GMAIL_PASSWORD = getenv("GMAIL_PASSWORD")

# Twilio
# -------------------------------------------------
TWILIO_SENDER_PHONE = getenv("TWILIO_SENDER_PHONE")
TWILIO_BRO_PHONE_NUMBER = getenv("TWILIO_BRO_PHONE_NUMBER")
TWILIO_ACLEE_PHONE_NUMBER = getenv("TWILIO_ACLEE_PHONE_NUMBER")
TWILIO_BALES_PHONE_NUMBER = getenv("TWILIO_BALES_PHONE_NUMBER")
TWILIO_SLANT_PHONE_NUMBER = getenv("TWILIO_SLANT_PHONE_NUMBER")
TWILIO_PIZZA_PHONE_NUMBER = getenv("TWILIO_PIZZA_PHONE_NUMBER")
TWILIO_MRSACLEE_PHONE_NUMBER = getenv("TWILIO_MRSACLEE_PHONE_NUMBER")
TWILIO_AUTH_TOKEN = getenv("TWILIO_AUTH_TOKEN")
TWILIO_ACCOUNT_SID = getenv("TWILIO_ACCOUNT_SID")
TWILIO_PHONE_NUMBERS = {
    "bro": TWILIO_BRO_PHONE_NUMBER,
    "aclee": TWILIO_ACLEE_PHONE_NUMBER,
    "bales": TWILIO_BALES_PHONE_NUMBER,
    "slant": TWILIO_SLANT_PHONE_NUMBER,
    "pizza": TWILIO_PIZZA_PHONE_NUMBER,
    "mrsaclee": TWILIO_MRSACLEE_PHONE_NUMBER,
}

# Reddit
REDDIT_CLIENT_ID = getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = getenv("REDDIT_CLIENT_SECRET")
REDDIT_USERNAME = getenv("REDDIT_USERNAME")
REDDIT_PASSWORD = getenv("REDDIT_CLIENT_SECRET")

# Rapid API
# -------------------------------------------------
RAPID_API_KEY = getenv("RAPID_API_KEY")

# IP Data
# -------------------------------------------------
IP_DATA_KEY = getenv("IP_DATA_KEY")

# Instagram
# -------------------------------------------------
INSTAGRAM_USERNAME = getenv("INSTAGRAM_USERNAME")
INSTAGRAM_PASSWORD = getenv("INSTAGRAM_PASSWORD")
INSTAGRAM_APP_ID = getenv("INSTAGRAM_APP_ID")
INSTAGRAM_APP_SECRET = getenv("INSTAGRAM_APP_SECRET")

# Covid API
# -------------------------------------------------
COVID_API_ENDPOINT = "https://covid-19-data.p.rapidapi.com/country/code"

# Lyrics Genius API
# -------------------------------------------------
GENIUS_KEY_ID = getenv("GENIUS_KEY_ID")
GENIUS_ACCESS_TOKEN = getenv("GENIUS_KEY_SECRET")

# Youtube
# -------------------------------------------------
YOUTUBE_API_KEY = getenv("YOUTUBE_API_KEY")

# Twitch
# -------------------------------------------------

# Twitch API endpoints, client ID, and client secret
TWITCH_CLIENT_ID = getenv("TWITCH_CLIENT_ID")
TWITCH_CLIENT_SECRET = getenv("TWITCH_CLIENT_SECRET")
TWITCH_TOKEN_ENDPOINT = "https://id.twitch.tv/oauth2/token"
TWITCH_STREAMS_ENDPOINT = "https://api.twitch.tv/helix/streams"

# Twitch usernames and IDs to follow
TWITCH_BRO_USERNAME = getenv("TWITCH_BRO_USERNAME")
TWITCH_BRO_ID = getenv("TWITCH_BRO_ID")
TWITCH_ATLAS_USERNAME = getenv("TWITCH_ATLAS_USERNAME")
TWITCH_ATLAS_ID = getenv("TWITCH_ATLAS_ID")
TWITCH_ACLEE_USERNAME = getenv("TWITCH_ACLEE_USERNAME")
TWITCH_ACLEE_ID = getenv("TWITCH_ACLEE_ID")
TWITCH_PANDA_USERNAME = getenv("TWITCH_PANDA_USERNAME")
TWITCH_PANDA_ID = getenv("TWITCH_PANDA_ID")
TWITCH_RANGER_USERNAME = getenv("TWITCH_RANGER_USERNAME")
TWITCH_RANGER_ID = getenv("TWITCH_RANGER_USERNAME")
TWITCH_TRAILBLAZING_USERNAME = getenv("TWITCH_TRAILBLAZING_USERNAME")
TWITCH_TRAILBLAZING_ID = getenv("TWITCH_TRAILBLAZING_ID")
TWITCH_CUMRAG_USERNAME = getenv("TWITCH_CUMRAG_USERNAME")
TWITCH_CUMRAG_ID = getenv("TWITCH_CUMRAG_ID")

TWITCH_BROADCASTERS = {
    TWITCH_BRO_USERNAME: TWITCH_BRO_ID,
    TWITCH_ATLAS_USERNAME: TWITCH_ATLAS_ID,
    TWITCH_ACLEE_USERNAME: TWITCH_ACLEE_ID,
    TWITCH_PANDA_USERNAME: TWITCH_PANDA_ID,
    TWITCH_RANGER_USERNAME: TWITCH_RANGER_ID,
    TWITCH_TRAILBLAZING_USERNAME: TWITCH_TRAILBLAZING_ID,
    TWITCH_CUMRAG_USERNAME: TWITCH_CUMRAG_ID,
}


TWITTER_CONSUMER_KEY = getenv("TWITTER_API_KEY")
TWITTER_CONSUMER_SECRET = getenv("TWITTER_API_SECRET")
TWITTER_BEARER_TOKEN = getenv("TWITTER_BEARER_TOKEN")
TWITTER_ACCESS_TOKEN = getenv("TWITTER_ACCESS_TOKEN")
TWITTER_TOKEN_SECRET = getenv("TWITTER_TOKEN_SECRET")

# NFL
# -------------------------------------------------
NFL_GAMES_URL = "https://sportspage-feeds.p.rapidapi.com/games"
NFL_HTTP_HEADERS = {
    "content-type": "application/json",
    "x-rapidapi-key": RAPID_API_KEY,
    "x-rapidapi-host": "sportspage-feeds.p.rapidapi.com",
}

# Footy
# -------------------------------------------------

# Footy API endpoints, tokens, and headers
FOOTY_BASE_URL = "https://api-football-v1.p.rapidapi.com/v3"
FOOTY_FIXTURES_ENDPOINT = f"{FOOTY_BASE_URL}/fixtures"
FOOTY_LIVE_FIXTURE_EVENTS_ENDPOINT = f"{FOOTY_BASE_URL}/fixtures/events"
FOOTY_LIVE_FIXTURE_STATS_ENDPOINT = f"{FOOTY_BASE_URL}/fixtures/statistics"
FOOTY_PREDICTS_ENDPOINT = f"{FOOTY_BASE_URL}/predictions"
FOOTY_TOPSCORERS_ENDPOINT = f"{FOOTY_BASE_URL}/players/topscorers"
FOOTY_STANDINGS_ENDPOINT = f"{FOOTY_BASE_URL}/standings"
FOOTY_XI_ENDPOINT = "https://api-football-v1.p.rapidapi.com/v3/fixtures/lineups"
FOOTY_HTTP_HEADERS = {
    "content-type": "application/json",
    "x-rapidapi-key": RAPID_API_KEY,
    "x-rapidapi-host": "api-football-v1.p.rapidapi.com",
}

# Footy League IDs
EPL_LEAGUE_ID = 39
UCL_LEAGUE_ID = 2
FA_CUP_ID = 45
FA_TROPHY_ID = 47
EFL_CUP_ID = 46
ENGLISH_CHAMPIONSHIP_LEAGUE_ID = 40
ENGLISH_LEAGUE_THREE_ID = 41
ENGLISH_LEAGUE_FOUR_ID = 42
ENGLISH_LEAGUE_FIVE_ID = 43
EUROPA_LEAGUE_ID = 2777
UEFA_EUROPA_ID = 3
UEFA_CONFERENCE_LEAGUE = 848
UEFA_NATIONS_LEAGUE = 5
BUND_LEAGUE_ID = 78
LIGA_LEAGUE_ID = 140
EUROS_LEAGUE_ID = 4
EUROS_QUALIFIERS_ID = 960
COPA_AMERICA_LEAGUE_ID = 9
COUPE_DE_FRANCE = 66
COPA_DEL_REY = 143
SPAIN_EL_CLASICO = 556
LIGUE_ONE_ID = 61
FRIENDLIES_LEAGUE_ID = 667
INT_FRIENDLIES_LEAGUE_ID = 10
WORLDCUP_LEAGUE_ID = 15
MLS_LEAGUE_ID = 253
CONCACAF_LEAGUE_ID = 767
CONCACAF_GOLD_CUP_ID = 22
CONCACAF_NATIONS_LEAGUE_ID = 536
CONCACAF_CHAMPIONS_LEAGUE_ID = 16
OLYMPICS_MEN_LEAGUE_ID = 480
OLYMPICS_WOMEN_LEAGUE_ID = 524
WORLD_CUP_ID = 1
WC_QUALIFIERS_CONCACAF = 31
WC_QUALIFIERS_EUROPE = 32
WC_QUALIFIERS_SOUTHAMERICA = 34
SERIE_A_LEAGUE_ID = 135
COMMUNITY_SHIELD_CUP = 528
CARABOU_CUP_ID = 48
AFCON_CUP_ID = 6
AFCON_QUALIFIERS_ID = 36
PRIMEIRA_LIGA_ID = 94
CONMEBOL_LIBERTADORES_ID = 13
CONMEBOL_SUDAMERICANA_ID = 11
CONMEBOL_RECOUPA_ID = 541
WOMENS_WORLD_CUP_ID = 8
U20_WORLD_CUP_ID = 490

# Footy Leagues, cups and tournaments
FOOTY_LEAGUES = {
    ":lion: EPL": EPL_LEAGUE_ID,
    ":blue_circle: UCL": UCL_LEAGUE_ID,
    ":orange_circle: UEFA EUROPA": UEFA_EUROPA_ID,
    ":green_circle: UEFA CONFERENCE": UEFA_CONFERENCE_LEAGUE,
    ":trophy: :baby_light_skin_tone: U20 WORLD CUP": U20_WORLD_CUP_ID,
    # ":England: EFL CHAMPIONSHIP": ENGLISH_CHAMPIONSHIP_LEAGUE_ID,
    # ":England: EFL LEAGUE 3": ENGLISH_LEAGUE_THREE_ID,
    # ":England: EFL LEAGUE 4": ENGLISH_LEAGUE_FOUR_ID,
    # ":England: EFL LEAGUE 5": ENGLISH_LEAGUE_FIVE_ID,
    # ":trophy: UEFA NATIONS LEAGUE": UEFA_NATIONS_LEAGUE,
    ":United_States: MLS": MLS_LEAGUE_ID,
    ":trophy: :England: FA CUP": FA_CUP_ID,
    # ":trophy: :rainbow: EUROS 2024": EUROS_LEAGUE_ID,
    # ":cow_face: CARABOU CUP": CARABOU_CUP_ID,
    ":Spain: LA LIGA": LIGA_LEAGUE_ID,
    # ":Germany: BUND": BUND_LEAGUE_ID,
    # ":Portugal: PRIMEIRA LIGA": PRIMEIRA_LIGA_ID,
    # ":Italy: SERIE A": SERIE_A_LEAGUE_ID,
    # ":France: LIGUE 1": LIGUE_ONE_ID,
    # ":trophy: :monkey: AFCON:": AFCON_CUP_ID,
    # ":Spain: EL CLÁSICO": SPAIN_EL_CLASICO,
    # ":trophy: :Spain: COPA DEL REY": COPA_DEL_REY,
    # ":trophy: :England: FA TROPHY": FA_TROPHY_ID,
    # ":trophy: :France: COUPE DE FRANCE": COUPE_DE_FRANCE,
    # ":shield: COMMUNITY SHIELD": COMMUNITY_SHIELD_CUP,
    # ":European_Union: :rainbow: EUROS 2024 QUALIFIERS": EUROS_QUALIFIERS_ID,
    # ":monkey: :globe_showing_Europe-Africa: AFCON QUALIFIERS": AFCON_QUALIFIERS_ID,
    # ":globe_showing_Americas: WC QUALIFIERS (CONCACAF)": WC_QUALIFIERS_CONCACAF,
    # ":globe_showing_Europe-Africa: WC QUALIFIERS (EUROPE)": WC_QUALIFIERS_EUROPE,
    # ":globe_showing_Americas: WC QUALIFIERS (SOUTH AMERICA)": WC_QUALIFIERS_SOUTHAMERICA,
    # ":sports_medal: OLYMPICS MEN": OLYMPICS_MEN_LEAGUE_ID,
    # ":sports_medal: OLYMPICS WOMEN": OLYMPICS_WOMEN_LEAGUE_ID,
    # ":trophy: WORLD CUP": WORLD_CUP_ID,
    ":United_States: WOMENS WORLD CUP": WOMENS_WORLD_CUP_ID,
    ":slightly_smiling_face: FRIENDLIES": FRIENDLIES_LEAGUE_ID,
    # ":slightly_smiling_face: :globe_showing_Europe-Africa: INTERNATIONAL FRIENDLIES": INT_FRIENDLIES_LEAGUE_ID,
    # ":globe_showing_Americas: COPA AMERICA": COPA_AMERICA_LEAGUE_ID,
    # ":globe_showing_Americas: CONCACAF LEAGUE": CONCACAF_LEAGUE_ID,
    # ":globe_showing_Americas: CONCACAF GOLD CUP": CONCACAF_GOLD_CUP_ID,
    # ":palm_tree: :globe_showing_Americas: CONCACAF NATIONS LEAGUE": CONCACAF_NATIONS_LEAGUE_ID,
    # ":trophy: :globe_showing_Americas: CONCACAF CHAMPIONS": CONCACAF_CHAMPIONS_LEAGUE_ID,
    ":trophy: :globe_showing_Americas: CONMEBOL RECOUPA": CONMEBOL_RECOUPA_ID,
    ":trophy: :globe_showing_Americas: CONMEBOL LIBERTADORES": CONMEBOL_LIBERTADORES_ID,
    ":trophy: :globe_showing_Americas: CONMEBOL SUDAMERICANA": CONMEBOL_SUDAMERICANA_ID,
}

# Footy leagues with "live scoring" enabled
FOOTY_LIVE_SCORED_LEAGUES = {
    # ":trophy: WORLD CUP": WORLD_CUP_ID,
    ":lion: EPL": EPL_LEAGUE_ID,
    ":blue_circle: UCL": UCL_LEAGUE_ID,
    ":orange_circle: UEFA EUROPA": UEFA_EUROPA_ID,
    ":green_circle: UEFA CONFERENCE": UEFA_CONFERENCE_LEAGUE,
    ":trophy: :baby_light_skin_tone: U20 WORLD CUP": U20_WORLD_CUP_ID,
    # ":England: EFL CHAMPIONSHIP": ENGLISH_CHAMPIONSHIP_LEAGUE_ID,
    # ":England: EFL LEAGUE 3": ENGLISH_LEAGUE_THREE_ID,
    # ":England: EFL LEAGUE 4": ENGLISH_LEAGUE_FOUR_ID,
    ":United_States: MLS": MLS_LEAGUE_ID,
    # ":trophy: UEFA NATIONS LEAGUE": UEFA_NATIONS_LEAGUE,
    ":trophy: :England: FA CUP": FA_CUP_ID,
    # ":cow_face: CARABOU CUP": CARABOU_CUP_ID,
    # ":Spain: EL CLÁSICO": SPAIN_EL_CLASICO,
    # ":trophy: :Spain: COPA DEL REY": COPA_DEL_REY,
    ":Spain: LIGA": LIGA_LEAGUE_ID,
    # ":trophy: :European_Union: :rainbow: EUROS 2024": EUROS_LEAGUE_ID,
    # ":Germany: BUND": BUND_LEAGUE_ID,
    # ":Italy: Serie A": SERIE_A_LEAGUE_ID,
    ":slightly_smiling_face: :globe_showing_Europe-Africa: INTERNATIONAL FRIENDLIES": INT_FRIENDLIES_LEAGUE_ID,
    # ":rainbow: :European_Union: EUROS 2024 QUALIFIERS": EUROS_QUALIFIERS_ID,
    ":monkey: :globe_showing_Europe-Africa: AFCON QUALIFIERS": AFCON_QUALIFIERS_ID,
    # ":trophy: :globe_showing_Americas: CONCACAF CHAMPIONS": CONCACAF_CHAMPIONS_LEAGUE_ID,
    # ":palm_tree: :globe_showing_Americas: CONCACAF NATIONS LEAGUE": CONCACAF_NATIONS_LEAGUE_ID,
    ":trophy: :globe_showing_Americas: CONMEBOL RECOUPA": CONMEBOL_RECOUPA_ID,
    ":trophy: :globe_showing_Americas: CONMEBOL LIBERTADORES": CONMEBOL_LIBERTADORES_ID,
    ":trophy: :globe_showing_Americas: CONMEBOL SUDAMERICANA": CONMEBOL_SUDAMERICANA_ID,
}

# Footy leagues with "lineups" enabled
FOOTY_LEAGUES_LINEUPS = {
    ":lion: EPL": EPL_LEAGUE_ID,
    ":blue_circle: UCL": UCL_LEAGUE_ID,
    ":orange_circle: UEFA EUROPA": UEFA_EUROPA_ID,
    ":green_circle: UEFA CONFERENCE": UEFA_CONFERENCE_LEAGUE,
    # ":England: EFL CHAMPIONSHIP": ENGLISH_CHAMPIONSHIP_LEAGUE_ID,
    # ":trophy: UEFA NATIONS LEAGUE": UEFA_NATIONS_LEAGUE,
    # ":trophy: :England: FA CUP": FA_CUP_ID,
    # ":trophy: :Spain: COPA DEL REY": COPA_DEL_REY,
    # ":Spain: EL CLÁSICO": SPAIN_EL_CLASICO,
    ":Spain: LIGA": LIGA_LEAGUE_ID,
    ":United_States: MLS": MLS_LEAGUE_ID,
    # ":Italy: Serie A": SERIE_A_LEAGUE_ID,
    # ":Germany: BUND": BUND_LEAGUE_ID,
    ":trophy: :baby_light_skin_tone: U20 WORLD CUP": U20_WORLD_CUP_ID,
    ":globe_showing_Americas: CONCACAF LEAGUE": CONCACAF_LEAGUE_ID,
    ":globe_showing_Americas: CONCACAF GOLD CUP": CONCACAF_GOLD_CUP_ID,
}

# Footy leagues to be considered for "golden shoe" award
GOLDEN_SHOE_LEAGUES = {
    ":lion: EPL": EPL_LEAGUE_ID,
    ":Spain: LIGA": LIGA_LEAGUE_ID,
    ":Germany: BUND": BUND_LEAGUE_ID,
    ":Italy: SERIE A": SERIE_A_LEAGUE_ID,
    ":France: LIGUE 1": LIGUE_ONE_ID,
}

# Footy team IDs
LIVERPOOL_TEAM_ID = 40
MANC_TEAM_ID = 50
MANU_TEAM_ID = 33
CHELSEA_TEAM_ID = 49
NEWCASTLE_TEAM_ID = 34
WESTHAM_TEAM_ID = 48
ARSENAL_TEAM_ID = 42
TOTTENHAM_TEAM_ID = 47
EVERTON_TEAM_ID = 45
FOXES_TEAM_ID = 46
VILLA_TEAM_ID = 66
LEEDS_TEAM_ID = 63
CRYSTAL_TEAM_ID = 52
NOTTINGHAM_TEAM_ID = 65
BRENTFORD_TEAM_ID = 55
SOUTHHAMPTON_TEAM_ID = 41
WOLVES_TEAM_ID = 39
FULHAM_TEAM_ID = 36
BOURNEMOUTH_TEAM_ID = 35
ENGLAND_INT_TEAM_ID = 10
WREXHAM_TEAM_ID = 1837
USA_CONCACAF_TEAM_ID = 2384
# USA_INT_TEAM_ID = 0

# Specify team IDs to be prioritized whe fetching starting XIs
FOOTY_TEAMS_PRIORITY = {
    "Pool": LIVERPOOL_TEAM_ID,
    "ManU": MANU_TEAM_ID,
    "England": ENGLAND_INT_TEAM_ID,
    "Foxes": FOXES_TEAM_ID,
    # "USMNT": USA_INT_TEAM_ID
}

# Footy team IDs for EPL
EPL_TEAM_IDS = [
    LIVERPOOL_TEAM_ID,
    MANC_TEAM_ID,
    MANU_TEAM_ID,
    CHELSEA_TEAM_ID,
    NEWCASTLE_TEAM_ID,
    WESTHAM_TEAM_ID,
    ARSENAL_TEAM_ID,
    TOTTENHAM_TEAM_ID,
    EVERTON_TEAM_ID,
    FOXES_TEAM_ID,
    VILLA_TEAM_ID,
    LEEDS_TEAM_ID,
    CRYSTAL_TEAM_ID,
    NOTTINGHAM_TEAM_ID,
    BRENTFORD_TEAM_ID,
    SOUTHHAMPTON_TEAM_ID,
    WOLVES_TEAM_ID,
    FULHAM_TEAM_ID,
    BOURNEMOUTH_TEAM_ID,
]

# MLB
# -------------------------------------------------
MLB_LEAGUE_ID = "1"
MLB_BASE_ENDPOINT = "https://api-baseball.p.rapidapi.com"
MLB_PHILLIES_ID = "27"

# Remote tuner control
# -------------------------------------------------
CHANNEL_LIST_FILEPATH = f"{BASE_DIR}/channels.json"
CHANNEL_HOST = getenv("CHANNEL_HOST")
CHANNEL_AUTH = getenv("CHANNEL_AUTH")
CHANNEL_TUNER_HEADERS = {
    "Connection": "keep-alive",
    "Authorization": CHANNEL_AUTH,
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "DNT": "1",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
    "Content-Type": "application/json",
    "Origin": CHANNEL_HOST,
    "Referer": CHANNEL_HOST,
    "Accept-Language": "en-US,en;q=0.9",
    "sec-gpc": "1",
}

# Olympics
# -------------------------------------------------
OLYMPICS_LEADERBOARD_ENDPOINT = "https://www.espn.com/olympics/summer/2020/medals/_/view/overall/sort/gold"
WINTER_OLYMPICS_LEADERBOARD_ENDPOINT = "https://www.espn.com/olympics/winter/2022/medals/_/view/overall/sort/gold"

# NBA
# -------------------------------------------------
NBA_BASE_URL = "https://api-basketball.p.rapidapi.com"
NBA_API_KEY = getenv("NBA_API_KEY")
NBA_CONFERENCE_NAMES = ["Eastern Conference", "Western Conference"]
NBA_SEASON_YEAR = "2022-2023"

# Playstation PSN
# -------------------------------------------------
PLAYSTATION_SSO_TOKEN = getenv("PLAYSTATION_SSO_TOKEN")


# DDOG
# -------------------------------------------------

DDOG_JSON_FORMAT = (
    "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] "
    "[dd.service=%(dd.service)s dd.env=%(dd.env)s dd.version=%(dd.version)s dd.trace_id=%(dd.trace_id)s dd.span_id=%(dd.span_id)s] "
    "- %(message)s"
)
