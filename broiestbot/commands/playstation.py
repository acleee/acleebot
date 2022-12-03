"""PSN Commands"""
from typing import List, Optional

from clients import psn
from psnawp_api.models.user import User
from emoji import emojize

from logger import LOGGER


def get_psn_online_friends() -> str:
    """
    Get list of all online friends of a PSN user.

    :returns: str
    """
    try:
        psn_account = psn.account.online_id
        online_friends = psn.get_online_friends()
        if bool(online_friends):
            active_friends = get_active_friends(online_friends)
            if active_friends or online_friends:
                return create_psn_response(active_friends, online_friends)
        return emojize(f"\n\n:video_game: <b>{psn_account}</b> has no friends.", language="en")
    except Exception as e:
        LOGGER.error(e)
        return emojize(f"\n\n:video_game: <b>{psn_account}</b> has no friends.", language="en")


def get_active_friends(online_friends: List[User]) -> List[Optional[User]]:
    """
    Get PSN user profile for a given online ID.

    :param friends List[User]: List of PSN friends.
    :returns: List[Optional[User]]
    """
    return [
        friend
        for friend in online_friends
        if friend.get_presence()["basicPresence"].get("gameTitleInfoList") is not None
    ]


def create_psn_response(active_friends: List[User], online_friends: List[User]) -> str:
    """
    Construct chat response of active PSN friends.

    :param str user: PSN User ID.
    :param List[User] friends: List of PSN friends.

    :returns: str
    """
    response = emojize(f"\n\n:video_game: <b>BROIESTBRO's online PSN friends</b>:\n", language="en")
    LOGGER.info(f"PSN friends: {online_friends}")
    for active_friend in active_friends:
        response += create_active_psn_user_response(active_friend)
    return response


def create_active_psn_user_response(active_friend: User) -> str:
    """
    Create response for active PSN user.

    :param str account_name: PSN User ID.
    :param str friend_meta: PSN User online presence data.

    :returns: str
    """
    try:
        friend_meta = active_friend.get_presence()
        playing_game = friend_meta["basicPresence"]["gameTitleInfoList"][0]["titleName"]
        platform = friend_meta["basicPresence"]["primaryPlatformInfo"]["platform"]
        return f"• <b>{active_friend.online_id}</b>: playing {playing_game} on {platform}\n"
    except Exception as e:
        LOGGER.error(e)
        return "idk"
