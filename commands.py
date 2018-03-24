import pandas as pd
import numpy as np

cmdDF = pd.read_csv('commands.csv')

def cm(msg):
    response = cmdDF.loc[cmdDF.cmd == msg]
    return response
