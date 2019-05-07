"""Bot configuration variables."""
import os

# Bot vars
testRoom = os.environ.get('TESTROOM')
acleeRoom = os.environ.get('ACLEEROOM')
blabroom = os.environ.get('BLABROOM')
username = os.environ.get('USERNAME')
password = os.environ.get('PASSWORD')

# DB vars

database_uri = os.environ.get('SQLALCHEMY_DATABASE_URI')
database_name = os.environ.get('SQLALCHEMY_DATABASE_NAME')
database_table = os.environ.get('SQLALCHEMY_TABLE')
database_schema = os.environ.get('SQLALCHEMY_DB_SCHEMA')
