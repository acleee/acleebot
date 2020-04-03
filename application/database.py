"""Load commands via database."""
import pandas as pd
from sqlalchemy import create_engine


class Database:
    """Database connection object."""

    def __init__(self, DATABASE_COMMANDS_TABLE, DATABASE_URI, DATABASE_ARGS):
        self.table = DATABASE_COMMANDS_TABLE
        self.engine = create_engine(DATABASE_URI, connect_args=DATABASE_ARGS, echo=False)

    @property
    def commands(self):
        """Load table from SQL database."""
        table_df = pd.read_sql_table(con=self.engine,
                                     table_name=self.table,
                                     index_col='command')
        return table_df

    @property
    def weather(self):
        """Load table from SQL database."""
        weather_df = pd.read_sql_table(con=self.engine,
                                       table_name='weather',
                                       index_col='code')
        return weather_df
