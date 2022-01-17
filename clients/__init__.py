"""Clients & SDKs for interacting with third-party services."""
import lyricsgenius
import praw
import wikipediaapi

# from googleapiclient.discovery import build
from imdb import IMDb
from twilio.rest import Client

from config import (  # YOUTUBE_API_KEY,
    ALPHA_VANTAGE_API_KEY,
    ALPHA_VANTAGE_CHART_BASE_URL,
    ALPHA_VANTAGE_PRICE_BASE_URL,
    GOOGLE_BUCKET_NAME,
    GOOGLE_BUCKET_URL,
    IEX_API_BASE_URL,
    IEX_API_TOKEN,
    IP_DATA_KEY,
    REDDIT_CLIENT_ID,
    REDDIT_CLIENT_SECRET,
    REDDIT_PASSWORD,
    REDDIT_USERNAME,
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
)

from .crypto import CryptoChartHandler
from .gcs import GCS
from .geo import GeoIP
from .stock import StockChartHandler

# Google Cloud Storage
gcs = GCS(GOOGLE_BUCKET_NAME, GOOGLE_BUCKET_URL)

# IEX Charts
sch = StockChartHandler(token=IEX_API_TOKEN, endpoint=IEX_API_BASE_URL)

# Crypto Charts
cch = CryptoChartHandler(
    token=ALPHA_VANTAGE_API_KEY,
    price_endpoint=ALPHA_VANTAGE_PRICE_BASE_URL,
    chart_endpoint=ALPHA_VANTAGE_CHART_BASE_URL,
)

# Wikipedia API Python SDK
wiki = wikipediaapi.Wikipedia("en")

# Twilio SMS Client
sms = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# IMDB Client
ia = IMDb()

# Reddit API Python SDK
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    username=REDDIT_USERNAME,
    password=REDDIT_PASSWORD,
    user_agent="bot",
)

# IP Data Client
geo = GeoIP(IP_DATA_KEY)

# Rap Genius
genius = lyricsgenius.Genius()
genius.remove_section_headers = True

# Youtube
# yt = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
