"""Load directory of commands via database."""
import pandas as pd
from sqlalchemy import create_engine


class Database:

    def __init__(self, config):
        self.URI = config.database_uri
        self.commands_table_name = config.database_table
        self.commands = self.load_sql_table()

    def load_sql_table(self):
        """Load commands from SQL database to DataFrame."""
        engine = create_engine(self.URI, echo=False)
        commands_df = pd.read_sql_table(con=engine,
                                        table_name=self.commands_table_name,
                                        index_col="command")
        return commands_df

    def fetch_bot_command(self, message):
        """Read list of rows from DataFrame."""
        try:
            row = self.commands.loc[message]
            response = {'content': row['response'],
                        'type': row['type']}
            return response
        except KeyError:
            return None
