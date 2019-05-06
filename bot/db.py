import pandas as pd
import numpy as np


def cm(msg):
    """Read list of commands from CSV."""
    command_df = pd.read_csv('commands.csv')
    response = command_df.loc[command_df.cmd == msg]
    return response
