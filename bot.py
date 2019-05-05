from urllib.request import urlopen
from time import sleep
from random import randint
import json
import requests
import ch
import sys
import os
import cgi
import traceback
import time
import urllib
import datetime
import binascii
import json
import threading
import random
import nba_py
from xml.etree import cElementTree as ET
from commands import cm
from config import username as username
from config import password as password
from config import room as room

if sys.version_info[0] > 2:
    import urllib.request as urlreq
else:
    import urllib2 as urlreq


class bot(ch.RoomManager):
    """Main bot class."""

    def onInit(self):
        """Initialize bot."""
        self.setNameColor("000000")
        self.setFontColor("000000")
        self.setFontFace("Arial")
        self.setFontSize(11)

    def crypto(self, message):
        """Get crypto prices."""
        print(message.msg.values[0])
        r = requests.get(url=message.msg.values[0])
        x = r.json()
        print(x)
        y = x["result"]["price"]
        z = y["change"]
        last = str(y["last"])
        high = str(y["high"])
        low = str(y["low"])
        percentage = z["percentage"]*100
        res = message.cmd.values[0] \
            + ": currently at $" + last \
            + ", high today of $" + high \
            + ", low of $" + low \
            + ", change of %.3f" % percentage + "%"
        return res

    def chat(self, message, room):
        """Trigger upon chat."""
        type = message.type.values[0]
        if (type == 'basic'):
            room.message(message.msg.values[0])
        if (type == 'price'):
            print('price command')
            room.message('under development tbh')
        if (type == 'crypto'):
            room.message(self.crypto(message))
        if (type == 'score'):
            print('score command')
            room.message('under development tbh')
        if (type == 'goal'):
            print('goal command')
            room.message('under development tbh')
        if (type == 'custom'):
            print('custom command')
            room.message('under development tbh')

    def onMessage(self, room, user, message):
        """Boilerplate function trigger on message."""
        print("[{0}] {1}: {2}".format(room.name, user.name.title(),
                                      message.body))
        try:
            cmd, args = message.body.split(" ", 1)
        except:
            cmd, args = message.body, ""

        if cmd[0] == "!":
            prfx = True
            cmd = cmd[1:]
            response = cm(cmd.lower())
            self.chat(response, room)
        else:
            fullmsg = cmd


bot.easy_start(room,
               username,
               password)
