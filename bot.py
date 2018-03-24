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
import config

if sys.version_info[0] > 2:
    import urllib.request as urlreq
else:
    import urllib2 as urlreq

class bot(ch.RoomManager):
    def onInit(self):
        self.setNameColor("000000")
        self.setFontColor("000000")
        self.setFontFace("Arial")
        self.setFontSize(11)

    def onMessage(self, room, user, message):
        print("[{0}] {1}: {2}".format(room.name, user.name.title(), message.body))
        try:
            cmd, args = message.body.split(" ", 1)
        except:
            cmd, args = message.body, ""

        if cmd[0] == "!":
            prfx = True
            cmd = cmd[1:]
            message = cm(cmd.lower())
            type = message.type.values[0]
            if (type == 'basic'):
                print('message = ', message)
                room.message(message.msg.values[0])
            if (type == 'price'):
                print('price command')
                room.message('under development tbh')
            if (type == 'crypto'):
                print('crypto command')
                room.message('under development tbh')
            if (type == 'score'):
                print('score command')
                room.message('under development tbh')
            if (type == 'goal'):
                print('goal command')
                room.message('under development tbh')
            if (type == 'custom'):
                print('custom command')
                room.message('under development tbh')

        else:
            fullmsg = cmd

bot.easy_start(config.rooms,config.username,config.password)
