"""Database client."""
from typing import Optional

from pandas import DataFrame
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError


class Database:
    """Database client."""

    def __init__(self, uri: str, args: dict, users_table: str):
        self.db = create_engine(uri, connect_args=args, echo=False)
        self.users_table = users_table

    def fetch_weather_icon(self, weather_query: int) -> Optional[dict]:
        """
        Fetch all rows via query.

        :param int weather_query: SQL query to run against database.

        :returns: Optional[str]
        """
        try:
            query = text(f"SELECT * FROM weather WHERE code = '{weather_query}';")
            response = self.db.execute(query).first()
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
            response = self.db.execute(query).fetchone()
            if response is not None:
                return dict(response)
        except SQLAlchemyError as e:
            print(f"Failed to execute SQL query `{command_query}`: {e}")
        except Exception as e:
            print(f"Failed to execute SQL query `{command_query}`: {e}")

    def insert_data_from_dataframe(self, df: DataFrame):
        """
        Agnostic method to insert parsed data into a provided SQL table.

        :param DataFrame df: Pandas DataFrame.
        """
        df.reset_index(inplace=True)
        df.to_sql(self.users_table, self.db, index_label="id", if_exists="replace")
        print(f"Inserted {df.head()}")
