"""Bot configuration variables."""
from os import environ


class Config:

    # Chatango rooms
    CHATANGO_TEST_ROOM = environ.get('CHATANGO_TEST_ROOM')
    CHATANGO_ACLEE_ROOM = environ.get('CHATANGO_ACLEE_ROOM')
    CHATANGO_BLAB_ROOM = environ.get('CHATANGO_BLAB_ROOM')
    CHATANGO_SIXERS_ROOM = environ.get('CHATANGO_SIXERS_ROOM')
    CHATANGO_EAGLES_ROOM = environ.get('CHATANGO_EAGLES_ROOM')
    CHATANGO_PHILLIES_ROOM = environ.get('CHATANGO_PHILLIES_ROOM')
    CHATANGO_NFL_ROOM = environ.get('CHATANGO_NFL_ROOM')
    CHATANGO_OBI_ROOM = environ.get('CHATANGO_OBI_ROOM')
    CHATANGO_ROOMS = [CHATANGO_TEST_ROOM,
                      CHATANGO_ACLEE_ROOM,
                      # CHATANGO_SIXERS_ROOM,
                      # CHATANGO_PHILLIES_ROOM,
                      # CHATANGO_EAGLES_ROOM,
                      # CHATANGO_NFL_ROOM,
                      CHATANGO_OBI_ROOM
                      ]

    # Chatango credentials
    CHATANGO_USERNAME = environ.get('CHATANGO_USERNAME')
    CHATANGO_PASSWORD = environ.get('CHATANGO_PASSWORD')

    # Database
    DATABASE_URI = environ.get('DATABASE_URI')
    DATABASE_NAME = environ.get('DATABASE_NAME')
    DATABASE_TABLE = environ.get('DATABASE_TABLE')
    DATABASE_ARGS = {'ssl': {'ca': './creds/ca-certificate.crt'}}

    # Google Cloud
    GOOGLE_APPLICATION_CREDENTIALS = environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    GOOGLE_BUCKET_NAME = environ.get('GOOGLE_BUCKET_NAME')
    GOOGLE_BUCKET_URL = environ.get('GOOGLE_BUCKET_URL')

    # Giphy
    GIPHY_API_KEY = environ.get('GIPHY_API_KEY')

    # Stock
    IEX_API_TOKEN = environ.get('IEX_API_TOKEN')
    ALPHA_VANTAGE_API = environ.get('ALPHA_VANTAGE_API')
