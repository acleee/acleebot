"""Create SQLAlchemy database sessions."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DATABASE_ARGS, SQLALCHEMY_DATABASE_URI


# Initialize Read/write database session
engine_rw = create_engine(SQLALCHEMY_DATABASE_URI, connect_args=DATABASE_ARGS, echo=False)
SessionRW = sessionmaker(bind=engine_rw)
session_rw = SessionRW()
