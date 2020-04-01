
class Commands:

    def __init__(self, commands_df):
        self.commands_df = commands_df

    def get(self, cmd):
        """Read list of rows from DataFrame."""
        response = None
        try:
            row = self.commands_df.loc[cmd]
            response = {'response': row['response'], 'type': row['type']}
        except KeyError:
            pass
        return response
