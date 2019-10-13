"""Load directory of commands via database."""
import pandas as pd
from config import Config
from sqlalchemy import create_engine, text


def get_commands_df():
    """Get list of commands from database."""
    engine = create_engine(Config.database_uri, echo=False)
    sql = text(f'SELECT * from {Config.database_schema}.{Config.database_table};')
    engine.execute(sql)
    commands_df = pd.read_sql_table(con=engine,
                                    schema=Config.database_schema,
                                    table_name=Config.database_table,
                                    index_col="command")
    return commands_df


commands_df = get_commands_df()
