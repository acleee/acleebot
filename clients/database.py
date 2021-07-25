"""Database client."""
from typing import Optional

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError


class Database:
    """Database client."""

    def __init__(self, uri: str, args: dict):
        self.commands_db = create_engine(uri, connect_args=args, echo=False)
        self.weather_db = create_engine(uri, connect_args=args, echo=False)

    def fetch_weather_icon(self, weather_query: int) -> Optional[dict]:
        """
        Fetch all rows via query.

        :param int weather_query: SQL query to run against database.

        :returns: Optional[str]
        """
        try:
            query = text(f"SELECT * FROM weather WHERE code = '{weather_query}';")
            response = self.commands_db.execute(query).first()
            if response is not None:
                return dict(response)
        except SQLAlchemyError as e:
            print(f"Failed to execute SQL query `{weather_query}`: {e}")
        except Exception as e:
            print(f"Failed to execute SQL query `{weather_query}`: {e}")

    def fetch_command_response(self, command_query: str) -> Optional[dict]:
        """
        Fetch a single row; typically used to verify whether a
        record already exists (ie: users).

        :param command_query: SQL query to run against database.
        :type command_query: str
        :returns: Optional[dict]
        """
        try:
            query = text(f"SELECT * FROM commands WHERE command = '{command_query}';")
            response = self.commands_db.execute(query).fetchone()
            if response is not None:
                return dict(response)
        except SQLAlchemyError as e:
            print(f"Failed to execute SQL query `{command_query}`: {e}")
        except Exception as e:
            print(f"Failed to execute SQL query `{command_query}`: {e}")
