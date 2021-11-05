from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DATABASE_ARGS, DATABASE_URI

engine = create_engine(DATABASE_URI, connect_args=DATABASE_ARGS, echo=False)
Session = sessionmaker(bind=engine, autocommit=True)
session = Session()
