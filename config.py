"""Bot configuration variables."""
from os import environ

# Chatango Vars
testRoom = environ.get('CHATANGO_TEST_ROOM')
acleeRoom = environ.get('CHATANGO_ACLEE_ROOM')
blabRoom = environ.get('CHATANGO_BLAB_ROOM')
sixersRoom = environ.get('CHATANGO_SIXERS_ROOM')
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
