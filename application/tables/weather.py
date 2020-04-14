"""Data structure associating weather forecasts to emojis."""


class Weather:
    """Table of weather type associations."""

    def __init__(self, weather_df):
        self.weather_df = weather_df

    def get(self, weather):
        """Read list of rows from DataFrame."""
        response = None
        try:
            row = self.weather_df.loc[weather]
            response = row['icon']
        except KeyError:
            pass
        return response
