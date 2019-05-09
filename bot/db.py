"""Load directory of commands via database."""
import pandas as pd
import logging
from config import database_uri
from config import database_schema
from config import database_table
from sqlalchemy import create_engine, text

# Set logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


def get_commands_from_database():
    """Connect to database and load commands into DataFrame."""
    engine = create_engine(database_uri, echo=True)
    sql = text('SELECT * from \"'
               + database_schema + '\".\"'
               + database_table + '\";')
    engine.execute(sql)
    command_df = pd.read_sql_table(con=engine,
                                   schema=database_schema,
                                   table_name=database_table,
                                   index_col="cmd")
    return command_df


command_df = get_commands_from_database()


def cm(message):
    """Read list of commands from CSV."""
    # Get Table from database
    row = command_df.loc[message]
    response = {
        'content': row['msg'],
        'type': row['type']
        }
    print('response = ', response)
    return response
