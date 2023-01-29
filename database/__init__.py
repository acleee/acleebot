"""Create SQLAlchemy database session."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DATABASE_ARGS, SQLALCHEMY_DATABASE_URI

engine = create_engine(SQLALCHEMY_DATABASE_URI, connect_args=DATABASE_ARGS, echo=False)
Session = sessionmaker(bind=engine)
session = Session()
