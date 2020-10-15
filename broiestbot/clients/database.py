"""Load SQL database tables into memory for commands & functionality."""
import pandas as pd
from sqlalchemy import create_engine
from broiestbot.table import Table


class Database:
    """Database connection object."""

    def __init__(self, uri, connection_args):
        self.engine = create_engine(
            uri,
            connect_args=connection_args,
            echo=False
        )

    def get_table(self, table, index):
        """Load table from SQL database."""
        table_df = pd.read_sql_table(table, self.engine, index_col=index)
        table = Table(table_df)
        return table
