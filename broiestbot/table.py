"""Data structure containing all bot commands."""


class Table:
    """Table of bot commands."""

    def __init__(self, df):
        self.df = df

    def find_row(self, lookup):
        """Read list of rows from DataFrame."""
        row = self.df.loc[self.df["command"] == lookup]
        if len(row):
            return row.iloc[0].to_dict()
        return None

