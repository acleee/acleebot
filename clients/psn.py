"""PSN account API client."""
from typing import Optional, List
from psnawp_api import PSNAWP
from psnawp_api.models.user import User


class PlaystationClient:
    def __init__(self, token: str):
        self.psn = PSNAWP(token)

    @property
    def account(self):
        """Get logged-in PSN account."""
        return self.psn.me()

    def get_online_friends(self) -> List[Optional[User]]:
        """Get friends of logged-in PSN user."""
        friends = self.account.friends_list()
        online_friends = [
            friend
            for friend in friends
            if friend.get_presence()["basicPresence"]["availability"] != "unavailable"
        ]
        return online_friends

    def get_user(self, online_id: str) -> Optional[User]:
        """
        Get PSN user profile for a given online ID.

        :param online_id str: PSN User ID.

        :returns: Optional[User]
        """
        return self.psn.user(online_id=online_id)
