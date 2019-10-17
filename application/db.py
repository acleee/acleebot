"""Load directory of commands via database."""
import pandas as pd
from config import Config
from sqlalchemy import create_engine, text
from . import logger


def load_commands():
    """Get list of commands from database."""
    engine = create_engine(Config.database_uri, echo=False)
    sql = text(f'SELECT * from {Config.database_schema}.{Config.database_table};')
    engine.execute(sql)
    commands_df = pd.read_sql_table(con=engine,
                                    schema=Config.database_schema,
                                    table_name=Config.database_table,
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
        return None
