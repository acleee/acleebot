"""Bot configuration variables."""
from os import environ


class Config:
    """Configuration variables."""

    # Chatango rooms
    testRoom = environ.get('CHATANGO_TEST_ROOM')
    acleeRoom = environ.get('CHATANGO_ACLEE_ROOM')
    blabRoom = environ.get('CHATANGO_BLAB_ROOM')
    sixersRoom = environ.get('CHATANGO_SIXERS_ROOM')
    eaglesRoom = environ.get('CHATANGO_EAGLES_ROOM')
    philliesRoom = environ.get('CHATANGO_PHILLIES_ROOM')
    nflRoom = environ.get('CHATANGO_NFL_ROOM')
    obiRoom = environ.get('CHATANGO_OBI_ROOM')
    chatangoRooms = [testRoom,
                     acleeRoom,
                     sixersRoom,
                     # philliesRoom,
                     # eaglesRoom,
                     # nflRoom,
                     obiRoom]

    # Chatango creds
    username = environ.get('CHATANGO_USERNAME')
    password = environ.get('CHATANGO_PASSWORD')

    # DB Vars
    database_uri = environ.get('SQLALCHEMY_DATABASE_URI')
    database_name = environ.get('SQLALCHEMY_DATABASE_NAME')
    database_table = environ.get('SQLALCHEMY_TABLE')
    database_args = {'ssl': {'ca': './creds/ca-certificate.crt'}}

    # Google Cloud Storage Vars
    gcloudCredentials = environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    gcloudBucketName = environ.get('GOOGLE_BUCKET_NAME')
    gcloudBucketUrl = environ.get('GOOGLE_BUCKET_URL')

    # Giphy
    giphy_api_key = environ.get('GIPHY_API_KEY')

    # Stock
    iex_api_key = environ.get('IEX_API_TOKEN')
