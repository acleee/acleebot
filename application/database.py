"""Load directory of commands via database."""
import pandas as pd
from sqlalchemy import create_engine


class Database:

    def __init__(self, config):
        self.URI = config.database_uri
        self.commands_table_name = config.database_table
        self.conn_args = config.database_args
        self.engine = create_engine(self.URI, echo=False)

    def load_table(self, table, index=None):
        """Load commands from SQL database to DataFrame."""
        engine = create_engine(self.URI, connect_args=self.conn_args, echo=False)
        table_df = pd.read_sql_table(con=engine,
                                     table_name=table,
                                     index_col=index)
        return table_df

    @property
    def commands(self):
        return self.load_table(self.commands_table_name, 'command')

    def fetch_bot_command(self, message):
        """Read list of rows from DataFrame."""
        try:
            row = self.commands.loc[message]
            response = {'content': row['response'],
                        'type': row['type']}
            return response
        except KeyError:
            return None
