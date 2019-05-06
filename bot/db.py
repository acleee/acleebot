"""Load directory of commands via database."""
import pandas as pd


def cm(message):
    """Read list of commands from CSV."""
    command_df = pd.read_csv('data/command_listing.csv', index_col="cmd")
    row = command_df.loc[message]
    response = {
        'content': row['msg'],
        'type': row['type']
        }
    print('response = ', response)
    return response
