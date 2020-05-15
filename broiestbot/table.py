"""Data structure containing all bot commands."""


class Table:
    """Table of bot commands."""

    def __init__(self, df):
        self.df = df

    def find_row(self, lookup):
        """Read list of rows from DataFrame."""
        response = None
        try:
            row = self.df.loc[lookup]
            response = row.to_dict()
        except KeyError:
            pass
        return response
