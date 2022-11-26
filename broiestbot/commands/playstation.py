"""PSN Commands"""

from clients import psn
from logger import LOGGER


def get_current_psn_user():
    """Test PSN API."""
    online_id = psn.account.online_id
    account_id = psn.account.account_id
    friends = psn.account.friends_list()
    friends = [
        f"{friend.online_id}\n"
        for friend in friends
        if friend.get_presence()["basicPresence"]["availability"] != "unavailable"
    ]
    LOGGER.info(f"Online ID: {online_id}\nAccount ID: {account_id}\nFriends: {friends}")
    if friends:
        response = f"\n\n{online_id}'s online PSN friends\n:"
        for friend in friends:
            response += f"{friend}\n"
        return response
