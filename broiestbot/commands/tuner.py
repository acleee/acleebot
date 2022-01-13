"""Channel tuner/remote."""
import json
import time

import requests
from emoji import emojize

from config import CHANNEL_AUTH, CHANNEL_HOST, CHATANGO_SPECIAL_USERS, BASE_DIR


def open_json():
    with open(f"{BASE_DIR}/channels.json.txt") as fp:
        channel_data = json.load(fp)
    return channel_data["result"]["channels"]


def current_milli_time():
    return str(round(time.time() * 1000))


def get_proper_caps(name):
    channels = open_json()
    channel = [channel for channel in channels if channel["channel"].lower() == name.lower()]
    return str(channel[0]["channel"])


def get_number(name: str):
    channels = open_json()
    try:
        channel = [channel for channel in channels if channel["channel"].lower() == name.lower()]
        return str(channel[0]["channelid"])
    except IndexError:
        err_msg = "{} wasn't found, but I found the following channels: \n".format(name)
        channel = [channel for channel in channels if name.lower() in channel["channel"].lower()]
        for name in channel:
            err_msg += name["channel"] + "\n"
        return err_msg


# name goes here, ex: tuner("Cartoon Network")
def tuner(name, user):
    if user.lower() in CHATANGO_SPECIAL_USERS:
        if name == "gumball":
            name = "Cartoon Network"
        if name == "joop":
            name = "ABC"
        num = get_number(name)
        try:
            number = int(num)
        except ValueError:
            return num
        number = str(number)
        capped = get_proper_caps(name)
        headers = {
            "Connection": "keep-alive",
            "Authorization": CHANNEL_AUTH,
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "DNT": "1",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
            "Content-Type": "application/json",
            "Origin": CHANNEL_HOST,
            "Referer": CHANNEL_HOST,
            "Accept-Language": "en-US,en;q=0.9",
            "sec-gpc": "1",
        }

        # some of this has to use ugly plus signs because format() breaks due to all the curlies
        data = '{"jsonrpc":"2.0","method":"Player.Open","params":{"item":{"channelid":' + number + '}},"id":' + current_milli_time() + "}"
        response = requests.post(f"{CHANNEL_HOST}jsonrpc", headers=headers, data=data, verify=False)
        data2 = (
            '{"id":752,"jsonrpc":"2.0","method":"PVR.GetBroadcasts","params":{"channelid":'
            + number
            + ',"properties":["isactive","starttime","endtime","title"], "limits":{ "end": 2}}}'
        )
        response2 = requests.post(f"{CHANNEL_HOST}jsonrpc", headers=headers, data=data2, verify=False)
        data3 = json.loads(response2.content)
        onnow = data3["result"]["broadcasts"][0]["title"]
        return emojize(f":tv: Tuning to {capped}. On now: {onnow}", use_aliases=True)
    return emojize(
        f":warning: u don't have the poughwer to change da channol :warning:",
        use_aliases=True,
    )
