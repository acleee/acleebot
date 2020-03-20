"""Load directory of commands via database."""
import pandas as pd
from sqlalchemy import create_engine


class Database:

    def __init__(self, config):
        self.DATABASE_TABLE = config.DATABASE_TABLE
        self.ALPHA_VANTAGE_API = config.ALPHA_VANTAGE_API
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
        response = None
        try:
            row = self.commands.loc[message]
            response = {'content': row['response'],
                        'type': row['type']}
        except KeyError as e:
            raise Exception(e)
        return response


    def get_market_data(self, symbol):
        """Fetch 20-day timeseries market data."""
        print(f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={self.ALPHA_VANTAGE_API}&datatype=csv&outputsize=compact', parse_dates=['timestamp'], dtype={'close': 'Float64'})
        df = pd.read_csv(f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={self.ALPHA_VANTAGE_API}&datatype=csv&outputsize=compact', parse_dates=['timestamp'], dtype={'close': 'Float64'})
        df.drop(columns=['open', 'high', 'low', 'volume'], inplace=True)
        df = df.loc[0:20]
        return df
