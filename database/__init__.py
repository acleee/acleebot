"""Create SQLAlchemy database sessions."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DATABASE_ARGS, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_DATABASE_RO_URI

# Initialize Read-only database session
engine_ro = create_engine(SQLALCHEMY_DATABASE_RO_URI, connect_args=DATABASE_ARGS, echo=False)
SessionRO = sessionmaker(bind=engine_ro)
session_ro = SessionRO()

# Initialize Read/write database session
engine_rw = create_engine(SQLALCHEMY_DATABASE_URI, connect_args=DATABASE_ARGS, echo=False)
SessionRW = sessionmaker(bind=engine_rw)
session_rw = SessionRW()
