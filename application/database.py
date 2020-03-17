"""Load directory of commands via database."""
import pandas as pd
from sqlalchemy import create_engine


class Database:

    def __init__(self, config):
        self.DATABASE_TABLE = config.DATABASE_TABLE
        self.engine = create_engine(config.DATABASE_URI, connect_args=config.DATABASE_ARGS, echo=False)

    def load_table(self, table, index=None):
        """Load table from SQL database."""
        table_df = pd.read_sql_table(con=self.engine,
                                     table_name=table,
                                     index_col=index)
        return table_df

    @property
    def commands(self):
        return self.load_table(self.DATABASE_TABLE, 'command')

    def fetch_bot_command(self, message):
        """Read list of rows from DataFrame."""
        try:
            row = self.commands.loc[message]
            response = {'content': row['response'],
                        'type': row['type']}
            return response
        except KeyError:
            return None
