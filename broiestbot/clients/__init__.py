"""External clients."""
import wikipediaapi
import praw
from config import (
    GOOGLE_BUCKET_NAME,
    GOOGLE_BUCKET_URL,
    DATABASE_URI,
    DATABASE_ARGS,
    IEX_API_BASE_URL,
    IEX_API_TOKEN,
    ALPHA_VANTAGE_PRICE_BASE_URL,
    ALPHA_VANTAGE_CHART_BASE_URL,
    ALPHA_VANTAGE_API_KEY,
    REDDIT_CLIENT_ID,
    REDDIT_CLIENT_SECRET,
    REDDIT_PASSWORD,
)
from .database import Database
from .gcs import GCS
from .crypto import CryptoChartHandler
from .stock import StockChartHandler


# Bot Database
db = Database(
    DATABASE_URI,
    DATABASE_ARGS
)

# Google Cloud Storage
gcs = GCS(
    GOOGLE_BUCKET_NAME,
    GOOGLE_BUCKET_URL
)

# IEX Charts
sch = StockChartHandler(
    token=IEX_API_TOKEN,
    endpoint=IEX_API_BASE_URL
)

# Crypto Charts
cch = CryptoChartHandler(
    token=ALPHA_VANTAGE_API_KEY,
    price_endpoint=ALPHA_VANTAGE_PRICE_BASE_URL,
    chart_endpoint=ALPHA_VANTAGE_CHART_BASE_URL
)

# Wikipedia API Python SDK
wiki = wikipediaapi.Wikipedia('en')

# Reddit API Python SDK
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    username='broiestbro',
    password=REDDIT_PASSWORD,
    user_agent="bot"
)

