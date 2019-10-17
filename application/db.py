"""Load directory of commands via database."""
import pandas as pd
from config import database_uri, database_schema, database_table
from sqlalchemy import create_engine, text
from . import logger


def load_commands():
    """Get list of commands from database."""
    engine = create_engine(database_uri, echo=True)
    sql = text('SELECT * from \"'
               + database_schema + '\".\"'
               + database_table + '\";')
    engine.execute(sql)
    commands_df = pd.read_sql_table(con=engine,
                                    schema=database_schema,
                                    table_name=database_table,
                                    index_col="command")
    return commands_df


commands_df = load_commands()


def get_command(message):
    """Read list of commands from database."""
    try:
        row = commands_df.loc[message]
        response = {
            'content': row['response'],
            'type': row['type']}
        return response
    except KeyError:
        logger.error(f'{message} is not a command.')
        pass
