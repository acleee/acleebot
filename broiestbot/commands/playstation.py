"""PSN Commands"""
from typing import List

from clients import psn
from psnawp_api.models.user import User
from emoji import emojize

from logger import LOGGER


def get_current_psn_user():
    """Get list of all online friends of a PSN user."""
    user = psn.account.online_id
    online_friends = psn.get_online_friends()
    if bool(online_friends):
        LOGGER.info(f"PSN friends found: {online_friends}")
        friends = _get_psn_friend_profiles(online_friends)
        return _create_psn_response(user, friends)
    return emojize(f"\n\n:video_game: <b>{user}</b> has no friends.", language="en")


def _get_psn_friend_profiles(online_friends: List[User]) -> List[dict]:
    """
    Get PSN user profile for a given online ID.
    :param friends List[User]: List of PSN friends.
    :returns: List[dict]
    """
    return [
        friend
        for friend in online_friends
        if friend.get_presence().get("gameTitleInfoList") is not None
    ]


def _create_psn_response(user, friends: List[User]) -> str:
    """
    Construct chat response of active PSN friends.

    :param user str: PSN User ID.
    :param friends List[User]: List of PSN friends.

    :returns: str
    """
    response = emojize(
        f"\n\n:video_game: <b>{user.upper()}'s online PSN friends</b>:\n", language="en"
    )
    for friend in friends:
        LOGGER.info(f"friend: {friend.online_id}")
        account_name = friend.online_id
        game = friend.get_presence()["gameTitleInfoList"][0]["titleName"]
        LOGGER.info(f"game: {game}")
        platform = friend.get_presence()["basicPresence"]["platform"]
        LOGGER.info(f"platform: {platform}")
        response += f"<b>{account_name}</b>: playing {game} on {platform}\n"
        return response
