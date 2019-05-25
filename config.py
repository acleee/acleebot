"""Bot configuration variables."""
from os import environ

# Bot vars
testRoom = environ.get('TESTROOM')
acleeRoom = environ.get('ACLEEROOM')
blabroom = environ.get('BLABROOM')
username = environ.get('USERNAME')
password = environ.get('PASSWORD')

# DB vars
database_uri = environ.get('SQLALCHEMY_DATABASE_URI')
database_name = environ.get('SQLALCHEMY_DATABASE_NAME')
database_table = environ.get('SQLALCHEMY_TABLE')
database_schema = environ.get('SQLALCHEMY_DB_SCHEMA')
