"""Bot configuration variables."""
from os import environ

# Chatango rooms
testRoom = environ.get('CHATANGO_TEST_ROOM')
acleeRoom = environ.get('CHATANGO_ACLEE_ROOM')
blabRoom = environ.get('CHATANGO_BLAB_ROOM')
sixersRoom = environ.get('CHATANGO_SIXERS_ROOM')
ufcRoom = environ.get('CHATANGO_UFC_ROOM')
philliesRoom = environ.get('CHATANGO_PHILLIES_ROOM')
chatangoRooms = [testRoom, acleeRoom, sixersRoom, philliesRoom]

# Chatango creds
username = environ.get('CHATANGO_USERNAME')
password = environ.get('CHATANGO_PASSWORD')


# DB Vars
database_uri = environ.get('SQLALCHEMY_DATABASE_URI')
database_name = environ.get('SQLALCHEMY_DATABASE_NAME')
database_table = environ.get('SQLALCHEMY_TABLE')
database_schema = environ.get('SQLALCHEMY_DB_SCHEMA')

# Google Cloud Storage Vars
gcloudCredentials = environ.get('GOOGLE_APPLICATION_CREDENTIALS')
gcloudBucketName = environ.get('GOOGLE_BUCKET_NAME')
gcloudBucketUrl = environ.get('GOOGLE_BUCKET_URL')

# Giphy
giphy_api_key = environ.get('GIPHY_API_KEY')
iex_api_key = environ.get('IEX_API_TOKEN')
