"""External services."""
from config import (GOOGLE_BUCKET_NAME,
                    GOOGLE_BUCKET_URL,
                    DATABASE_URI,
                    DATABASE_ARGS)
from .database import Database
from .gcs import GCS
from .logging import create_logger

db = Database(DATABASE_URI, DATABASE_ARGS)
logger = create_logger()
gcs = GCS(GOOGLE_BUCKET_NAME, GOOGLE_BUCKET_URL,)
