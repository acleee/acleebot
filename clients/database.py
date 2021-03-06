"""Load SQL database tables into memory for commands & functionality."""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from broiestbot.table import Table


class Database:
    """Database connection object."""

    def __init__(self, uri: str, connection_args: dict):
        self.engine = create_engine(uri, connect_args=connection_args, echo=False)

    def _table(self, table_name: str, database_name: str) -> Table:
        """
        :param table_name: Name of database table to fetch
        :type table_name: str
        :param database_name: Name of database to connect to.
        :type database_name: str
        :returns: Table
        """
        return Table(
            table_name, MetaData(bind=self.engines[database_name]), autoload=True
        )

    def get_table(self, table, index) -> Table:
        """Load table from SQL database."""
        table_df = pd.read_sql_table(table, self.engine, index_col=index)
        table = Table(table_df)
        return table
