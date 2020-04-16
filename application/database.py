"""Load commands via database."""
import pandas as pd
from sqlalchemy import create_engine


class Database:
    """Database connection object."""

    def __init__(self, DATABASE_URI, DATABASE_ARGS):
        self.engine = create_engine(DATABASE_URI,
                                    connect_args=DATABASE_ARGS,
                                    echo=False)

    def get_table(self, table, index):
        """Load table from SQL database."""
        table_df = pd.read_sql_table(con=self.engine,
                                     table_name=table,
                                     index_col=index)
        return table_df
