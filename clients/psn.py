"""PSN account API client."""
from typing import Optional, List
from psnawp_api import PSNAWP
from psnawp_api.models.user import User
from psnawp_api.models.client import Client


class PlaystationClient:
    def __init__(self, token: str):
        self.psn = PSNAWP(token)

    @property
    def account(self) -> Client:
        """
        Get logged-in PSN account.

        :returns: Client
        """
        return self.psn.me()

    def get_online_friends(self) -> List[Optional[User]]:
        """
        Get friends of logged-in PSN user.

        :returns: List[Optional[User]]
        """
        friends = self.account.friends_list()
        online_friends = [
            friend for friend in friends if friend.get_presence()["basicPresence"]["availability"] == "availableToPlay"
        ]
        return online_friends

    def get_user(self, online_id: str) -> Optional[User]:
        """
        Get PSN user profile for a given online ID.

        :param online_id str: PSN User ID.

        :returns: Optional[User]
        """
        return self.psn.user(online_id=online_id)
