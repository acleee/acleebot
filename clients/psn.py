"""PSN account API client."""
from psnawp_api import PSNAWP


class PlaystationClient:
    def __init__(self, token: str):
        self.psn = PSNAWP(token)

    @property
    def account(self):
        """Get logged-in PSN account."""
        return self.psn.me()
