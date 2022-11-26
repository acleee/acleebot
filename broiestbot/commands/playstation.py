"""PSN Commands"""

from clients import psn
from emoji import emojize


def get_current_psn_user():
    """Test PSN API."""
    online_id = psn.account.online_id
    friends = psn.account.friends_list()
    online_friends = [
        friend
        for friend in friends
        if friend.get_presence()["basicPresence"]["availability"] != "unavailable"
    ]
    friend_statuses = [
        f"{friend.online_id}: playing {friend.get_presence()['gameTitleInfoList'][0]['titleName']} on {friend.get_presence()['basicPresence']['platform']}"
        if friend.get_presence().get("gameTitleInfoList") is not None
        else f"{friend.online_id}"
        for friend in online_friends
    ]
    if friend_statuses:
        response = emojize(
            f"\n\n:video_game: <b>{online_id.upper()}'s online PSN friends</b>:\n", language="en"
        )
        for friend in friend_statuses:
            response += f"{friend}\n"
        return response
