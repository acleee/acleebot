"""Channel tuner/remote."""
import json
import time

import requests
from emoji import emojize

from config import (
    CHANNEL_HOST,
    CHANNEL_LIST_FILEPATH,
    CHANNEL_TUNER_HEADERS,
    CHATANGO_SPECIAL_USERS,
)
from logger import LOGGER


def parse_channel_json():
    """Parse JSON file containing channel information for tuner."""
    with open(CHANNEL_LIST_FILEPATH) as fp:
        channel_data = json.load(fp)
    return channel_data["result"]["channels"]


CHANNEL_DATA = parse_channel_json()


def current_milli_time() -> str:
    return str(round(time.time() * 1000))


def get_proper_caps(channel_name: str) -> str:
    channel = [channel for channel in CHANNEL_DATA if channel["channel"].lower() == channel_name]
    return str(channel[0]["channel"])


def get_channel_number(channel_name: str) -> str:
    """
    Fetch channel number by name.

    :params str channel_name: Name of channel to tune stream to.

    :returns: str
    """
    try:
        channel = [
            channel for channel in CHANNEL_DATA if channel["channel"].lower() == channel_name
        ]
        return str(channel[0]["channelid"])
    except IndexError:
        err_msg = f"{channel_name} wasn't found, but I found the following channels: \n"
        channel = [
            channel for channel in CHANNEL_DATA if channel_name in channel["channel"].lower()
        ]
        for name in channel:
            f"{err_msg} {name['channel']}\n"
        return err_msg
    except Exception as e:
        LOGGER.error(f"Unexpected error when getting channel number: {e}")
        return emojize(f":warning: omfg bot just broke wtf did u do :warning:", use_aliases=True)


def tuner(channel_name: str, username: str) -> str:
    """
    Fetch channel by name and tune stream if user is whitelisted.

    :param str channel_name: Name of channel to tune stream to.
    :param str username: Name of Chatango user requesting to change the channel (ex: "Cartoon Network").

    :returns: str
    """
    try:
        if username in CHATANGO_SPECIAL_USERS:
            if channel_name in ("gumball", "gumbol"):
                channel_name = "Cartoon Network"
            if channel_name == "joop":
                channel_name = "ABC"
            num = get_channel_number(channel_name)
            number = int(num)
            number = str(number)
            capped = get_proper_caps(channel_name)
            # some of this has to use ugly plus signs because format() breaks due to all the curlies
            data = (
                '{"jsonrpc":"2.0","method":"Player.Open","params":{"item":{"channelid":'
                + number
                + '}},"id":'
                + current_milli_time()
                + "}"
            )
            requests.post(
                f"{CHANNEL_HOST}jsonrpc", headers=CHANNEL_TUNER_HEADERS, data=data, verify=False
            )
            on_now = get_current_show(number)
            return emojize(f":tv: Tuning to {capped}. On now: {on_now}", use_aliases=True)
        return emojize(
            f":warning: u don't have the poughwer to change da channol :warning:",
            use_aliases=True,
        )
    except ValueError as e:
        LOGGER.info(
            f"ValueError occurred when fetching tuner channel; defaulting to {get_channel_number(channel_name)}: {e}"
        )
        return get_channel_number(channel_name)
    except Exception as e:
        LOGGER.error(f"Unexpected error when changing channel: {e}")


def get_current_show(number: str) -> str:
    """
    Fetch title of show currently on stream.

    :param str number: Channel number.

    :returns: str
    """
    data = (
        '{"id":752,"jsonrpc":"2.0","method":"PVR.GetBroadcasts","params":{"channelid":'
        + str(number)
        + ',"properties":["isactive","starttime","endtime","title"], "limits":{ "end": 2}}}'
    )
    resp = requests.post(
        f"{CHANNEL_HOST}jsonrpc", headers=CHANNEL_TUNER_HEADERS, data=data, verify=False
    )
    return resp.json()["result"]["broadcasts"][0]["title"]
