"""External clients."""
from config import (
    GOOGLE_BUCKET_NAME,
    GOOGLE_BUCKET_URL,
    DATABASE_URI,
    DATABASE_ARGS,
    IEX_API_BASE_URL,
    IEX_API_TOKEN,
    ALPHA_VANTAGE_PRICE_BASE_URL,
    ALPHA_VANTAGE_CHART_BASE_URL,
    ALPHA_VANTAGE_API_KEY
)
from .database import Database
from .gcs import GCS
from .logging import create_logger
from .crypto import CryptoChartHandler
from .stock import StockChartHandler


# Create handlers
db = Database(
    DATABASE_URI,
    DATABASE_ARGS
)

logger = create_logger()

gcs = GCS(
    GOOGLE_BUCKET_NAME,
    GOOGLE_BUCKET_URL
)

sch = StockChartHandler(
    token=IEX_API_TOKEN,
    endpoint=IEX_API_BASE_URL
)

cch = CryptoChartHandler(
    token=ALPHA_VANTAGE_API_KEY,
    price_endpoint=ALPHA_VANTAGE_PRICE_BASE_URL,
    chart_endpoint=ALPHA_VANTAGE_CHART_BASE_URL
)
