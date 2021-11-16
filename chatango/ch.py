import html
import queue
import random
import re
import select
import socket
import sys
import threading
import time
import urllib.parse
import urllib.request

from config import CHATANGO_USERS
from logger import LOGGER

from . import _ws

_ws_exc_info = sys.exc_info()
debug = True
userlist_recent = 0
userlist_all = 1

big_message_multiple = 0
BigMessage_Cut = 1

# minimum of 1 thread needed
Number_of_Threads = 1

Use_WebSocket = True


Channels = {
    "none": 0,
    "red": 256,
    "blue": 2048,
    "shield": 64,
    "staff": 128,
    "mod": 32768,
}

if Use_WebSocket and _ws is None:
    sys.stderr.write("Use_WebSocket is set to True, " "but couldn't import _ws.\n\n")
    import traceback

    traceback.print_exception(*_ws_exc_info, file=sys.stderr)
    exit(1)


################################################################
# Struct class
################################################################
class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)


################################################################
# Tagserver stuff
################################################################
specials = {
    "mitvcanal": 56,
    "animeultimacom": 34,
    "cricket365live": 21,
    "pokemonepisodeorg": 22,
    "animelinkz": 20,
    "sport24lt": 56,
    "narutowire": 10,
    "watchanimeonn": 22,
    "cricvid-hitcric-": 51,
    "narutochatt": 70,
    "leeplarp": 27,
    "stream2watch3": 56,
    "ttvsports": 56,
    "ver-anime": 8,
    "vipstand": 21,
    "eafangames": 56,
    "soccerjumbo": 21,
    "myfoxdfw": 67,
    "kiiiikiii": 21,
    "de-livechat": 5,
    "rgsmotrisport": 51,
    "dbzepisodeorg": 10,
    "watch-dragonball": 8,
    "peliculas-flv": 69,
    "tvanimefreak": 54,
    "tvtvanimefreak": 54,
}

# order matters
tsweights = [
    (5, 75),
    (6, 75),
    (7, 75),
    (8, 75),
    (16, 75),
    (17, 75),
    (18, 75),
    (9, 95),
    (11, 95),
    (12, 95),
    (13, 95),
    (14, 95),
    (15, 95),
    (19, 110),
    (23, 110),
    (24, 110),
    (25, 110),
    (26, 110),
    (28, 104),
    (29, 104),
    (30, 104),
    (31, 104),
    (32, 104),
    (33, 104),
    (35, 101),
    (36, 101),
    (37, 101),
    (38, 101),
    (39, 101),
    (40, 101),
    (41, 101),
    (42, 101),
    (43, 101),
    (44, 101),
    (45, 101),
    (46, 101),
    (47, 101),
    (48, 101),
    (49, 101),
    (50, 101),
    (52, 110),
    (53, 110),
    (55, 110),
    (57, 110),
    (58, 110),
    (59, 110),
    (60, 110),
    (61, 110),
    (62, 110),
    (63, 110),
    (64, 110),
    (65, 110),
    (66, 110),
    (68, 95),
    (71, 116),
    (72, 116),
    (73, 116),
    (74, 116),
    (75, 116),
    (76, 116),
    (77, 116),
    (78, 116),
    (79, 116),
    (80, 116),
    (81, 116),
    (82, 116),
    (83, 116),
    (84, 116),
]


def getServer(group):
    """
    Get the server host for a certain room.

    :type group: str
    :param group: room name

    @rtype: str
    @return: the server's hostname
    """
    try:
        sn = specials[group]
    except KeyError:
        group = group.replace("_", "q")
        group = group.replace("-", "q")
        fnv = float(int(group[:5], 36))
        lnv = group[6:9]
        if lnv:
            lnv = float(int(lnv, 36))
            lnv = max(lnv, 1000)
        else:
            lnv = 1000
        num = (fnv % lnv) / lnv
        maxnum = sum(y for x, y in tsweights)
        cumfreq = 0
        sn = 0
        for x, y in tsweights:
            cumfreq += float(y) / maxnum
            if num <= cumfreq:
                sn = x
                break
    return "s" + str(sn) + ".chatango.com"


################################################################
# Uid
################################################################
def _genUid():
    """
    generate a uid
    """
    return str(random.randrange(10 ** 15, 10 ** 16))


################################################################
# Message stuff
################################################################
def _clean_message(msg):
    """
    Clean a message and return the message, n tag and f tag.

    :type msg: str
    :param msg: the message

    @rtype: str, str, str
    @returns: cleaned message, n tag contents, f tag contents
    """
    n = re.search("<n(.*?)/>", msg)
    if n:
        n = n.group(1)
    f = re.search("<f(.*?)>", msg)
    if f:
        f = f.group(1)
    msg = re.sub("<n.*?/>", "", msg)
    msg = re.sub("<f.*?>", "", msg)
    msg = _strip_html(msg)
    msg = html.unescape(msg)
    return msg, n, f


def _strip_html(msg):
    """Strip HTML."""
    li = msg.split("<")
    if len(li) == 1:
        return li[0]
    else:
        ret = list()
        for data in li:
            data = data.split(">", 1)
            if len(data) == 1:
                ret.append(data[0])
            elif len(data) == 2:
                ret.append(data[1])
        return "".join(ret)


def _parseNameColor(n):
    """This just returns its argument, should return the name color."""
    # probably is already the name
    return n


def _parse_font(f):
    """Parses the contents of a f tag and returns color, face and size."""
    # ' xSZCOL="FONT"'
    try:  # TODO: remove quick hack
        size_color, font_face = f.split("=", 1)
        size_color = size_color.strip()
        size = int(size_color[1:3])
        col = size_color[3:6]
        if col == "":
            col = None
        face = f.split('"', 2)[1]
        return col, face, size
    except Exception:
        return None, None, None


################################################################
# Anon id
################################################################
def _getAnonId(n, ssid):
    """Gets the anon's id."""
    if n is None:
        n = "5504"
    try:
        return "".join(
            str(x + y)[-1]
            for x, y in zip((int(x) for x in n), (int(x) for x in ssid[4:]))
        )
    except ValueError:
        return "NNNN"


################################################################
# ANON PM class
################################################################
class _ANON_PM_OBJECT:
    """Manages connection with Chatango anon PM."""

    def __init__(self, mgr, name):
        self._connected = False
        self._mgr = mgr
        self._wlock = False
        self._firstCommand = True
        self._wbuf = b""
        self._wlockbuf = b""
        self._rbuf = b""
        self._pingTask = None
        self._name = name
        self._sock = None

    def _auth(self):
        self._send_command("mhs", "mini", "unknown", self._name)
        self._set_write_lock(True)
        return True

    def disconnect(self):
        """Disconnect the bot from PM"""
        self._disconnect()
        self._call_event("on_anon_pm_disconnect", get_user(self._name))

    def _disconnect(self):
        self._connected = False
        self._sock.close()
        self._sock = None
        del self.mgr.pm._persons[self._name]

    def ping(self):
        """send a ping"""
        self._send_command("")
        self._call_event("on_pm_ping")

    def message(self, user, msg):
        """send a pm to a user"""
        if msg is not None:
            self._send_command("msg", user.name, msg)

    ####
    # Feed
    ####
    def _feed(self, data):
        """
        Feed data to the connection.

        :type data: bytes
        :param data: data to be fed
        """
        self._rbuf += data
        while b"\0" in self._rbuf:
            data = self._rbuf.split(b"\x00")
            for food in data[:-1]:
                self._process(food.decode(errors="replace").rstrip("\r\n"))
            self._rbuf = data[-1]

    def _process(self, data):
        """
        Process a command string.

        :type data: str
        :param data: the command string
        """
        self._call_event("on_raw", data)
        data = data.split(":")
        cmd, args = data[0], data[1:]
        func = "_rcmd_" + cmd
        if hasattr(self, func):
            getattr(self, func)(args)

    def _get_manager(self):
        return self._mgr

    mgr = property(_get_manager)

    ####
    # Received Commands
    ####

    def _rcmd_mhs(self, args):
        """
        note to future maintainers

        args[1] is ether "online" or "offline"
        """
        self._connected = True
        self._set_write_lock(False)

    def _rcmd_msg(self, args):
        user = get_user(args[0])
        body = _strip_html(":".join(args[5:]))
        self._call_event("on_pm_message", user, body)

    ####
    # Util
    ####
    def _call_event(self, evt, *args, **kw):
        getattr(self.mgr, evt)(self, *args, **kw)
        self.mgr.on_event_called(self, evt, *args, **kw)

    def _write(self, data):
        if self._wlock:
            self._wlockbuf += data
        else:
            self.mgr._write(self, data)

    def _set_write_lock(self, lock):
        self._wlock = lock
        if not self._wlock:
            self._write(self._wlockbuf)
            self._wlockbuf = b""

    def _send_command(self, *args):
        """
        Send a command.

        :type args: [str, str, ...]
        :param args: command and list of arguments
        """
        if self._firstCommand:
            terminator = b"\x00"
            self._firstCommand = False
        else:
            terminator = b"\r\n\x00"
        self._write(":".join(args).encode() + terminator)


class ANON_PM:
    """Comparable wrapper for anon Chatango PM"""

    ####
    # Init
    ####
    def __init__(self, mgr):
        self._mgr = mgr
        self._wlock = False
        self._firstCommand = True
        self._persons = dict()
        self._wlockbuf = b""
        self._pingTask = None

    ####
    # Connections
    ####
    def _connect(self, name):
        self._persons[name] = _ANON_PM_OBJECT(self._mgr, name)
        sock = socket.socket()
        sock.connect((self._mgr._anon_pm_host, self._mgr._pm_port))
        sock.setblocking(False)
        self._persons[name]._sock = sock
        if not self._persons[name]._auth():
            return
        self._persons[name]._pingTask = self._mgr.set_internal(
            self._mgr._ping_delay, self._persons[name].ping
        )
        self._persons[name]._connected = True

    def message(self, user, msg):
        """send a pm to a user"""
        if user.name not in self._persons:
            self._connect(user.name)
        self._persons[user.name].message(user, msg)

    def get_connections(self):
        return list(x for x in self._persons.values() if x is not None)


################################################################
# PM class
################################################################
class PM:
    """Manages a connection with Chatango PM."""

    ####
    # Init
    ####
    def __init__(self, mgr):
        self._auth_re = re.compile(r"auth\.chatango\.com ?= ?([^;]*)", re.IGNORECASE)
        self._connected = False
        self._mgr = mgr
        self._auid = None
        self._blocklist = set()
        self._contacts = set()
        self._status = dict()
        self._wlock = False
        self._firstCommand = True
        self._wbuf = b""
        self._wlockbuf = b""
        self._rbuf = b""
        self._pingTask = None
        self._connect()

    ####
    # Connections
    ####
    def _connect(self):
        self._wbuf = b""
        self._sock = socket.socket()
        self._sock.connect((self._mgr._pm_host, self._mgr._pm_port))
        self._sock.setblocking(False)
        self._firstCommand = True
        if not self._auth():
            return
        self._pingTask = self.mgr.set_internal(self._mgr._ping_delay, self.ping)
        self._connected = True

    def _get_auth(self, name, password):
        """
        Request an auid using name and password.

        :type name: str
        :param name: name
        :type password: str
        :param password: password

        @rtype: str
        @return: auid
        """
        data = urllib.parse.urlencode(
            {
                "user_id": name,
                "password": password,
                "storecookie": "on",
                "checkerrors": "yes",
            }
        ).encode()
        try:
            resp = urllib.request.urlopen("http://chatango.com/login", data)
            headers = resp.headers
        except Exception:
            return None
        for header, value in headers.items():
            if header.lower() == "set-cookie":
                m = self._auth_re.search(value)
                if m:
                    auth = m.group(1)
                    if auth == "":
                        return None
                    return auth
        return None

    def _auth(self):
        self._auid = self._get_auth(self._mgr.name, self._mgr.password)
        if self._auid is None:
            self._sock.close()
            self._call_event("on_login_fail")
            self._sock = None
            return False
        self._send_command("tlogin", self._auid, "2")
        self._set_write_lock(True)
        return True

    def disconnect(self):
        """Disconnect the bot from PM"""
        self._disconnect()
        self._call_event("on_pm_disconnect")

    def _disconnect(self):
        self._connected = False
        self._sock.close()
        self._sock = None

    ####
    # Feed
    ####
    def _feed(self, data):
        """
        Feed data to the connection.

        :type data: bytes
        :param data: data to be fed
        """
        self._rbuf += data
        while b"\0" in self._rbuf:
            data = self._rbuf.split(b"\x00")
            for food in data[:-1]:
                self._process(food.decode(errors="replace").rstrip("\r\n"))
            self._rbuf = data[-1]

    def _process(self, data):
        """
        Process a command string.

        :type data: str
        :param data: the command string
        """
        self._call_event("on_raw", data)
        data = data.split(":")
        cmd, args = data[0], data[1:]
        func = "_rcmd_" + cmd
        if hasattr(self, func):
            getattr(self, func)(args)

    ####
    # Properties
    ####
    def _get_manager(self):
        return self._mgr

    def _get_contacts(self):
        return self._contacts

    def _get_blocklist(self):
        return self._blocklist

    mgr = property(_get_manager)
    contacts = property(_get_contacts)
    blocklist = property(_get_blocklist)

    ####
    # Received Commands
    ####
    def _rcmd_OK(self, args):
        self._set_write_lock(False)
        self._send_command("wl")
        self._send_command("getblock")
        self._call_event("on_pm_connect")

    def _rcmd_wl(self, args):
        self._contacts = set()
        for i in range(len(args) // 4):
            name, last_on, is_on, idle = args[i * 4 : i * 4 + 4]
            user = get_user(name)
            if last_on == "None":
                pass  # in case chatango gives a "None" as data argument
            elif not is_on == "on":
                self._status[user] = [int(last_on), False, 0]
            elif idle == "0":
                self._status[user] = [int(last_on), True, 0]
            else:
                self._status[user] = [int(last_on), True, time.time() - int(idle) * 60]
            self._contacts.add(user)
        self._call_event("on_pm_contactlist_receive")

    def _rcmd_block_list(self, args):
        self._blocklist = set()
        for name in args:
            if name == "":
                continue
            self._blocklist.add(get_user(name))

    def _rcmd_idleupdate(self, args):
        user = get_user(args[0])
        last_on, is_on, idle = self._status.get(user, (0, True, 0))
        if args[1] == "1":
            self._status[user] = [last_on, is_on, 0]
        else:
            self._status[user] = [last_on, is_on, time.time()]

    def _rcmd_track(self, args):
        user = get_user(args[0])
        if user in self._status:
            last_on = self._status[user][0]
        else:
            last_on = 0
        if args[1] == "0":
            idle = 0
        else:
            idle = time.time() - int(args[1]) * 60
        if args[2] == "online":
            is_on = True
        else:
            is_on = False
        self._status[user] = [last_on, is_on, idle]

    def _rcmd_DENIED(self, args):
        self._disconnect()
        self._call_event("on_login_fail")

    def _rcmd_msg(self, args):
        user = get_user(args[0])
        body = _strip_html(":".join(args[5:]))
        self._call_event("on_pm_message", user, body)

    def _rcmd_msgoff(self, args):
        user = get_user(args[0])
        body = _strip_html(":".join(args[5:]))
        self._call_event("on_pm_offline_message", user, body)

    def _rcmd_wlonline(self, args):
        user = get_user(args[0])
        last_on = float(args[1])
        self._status[user] = [last_on, True, last_on]
        self._call_event("on_pm_contact_online", user)

    def _rcmd_wloffline(self, args):
        user = get_user(args[0])
        last_on = float(args[1])
        self._status[user] = [last_on, False, 0]
        self._call_event("on_pm_contact_offline", user)

    def _rcmd_kickingoff(self, args):
        self.disconnect()

    def _rcmd_toofast(self, args):
        self.disconnect()

    def _rcmd_unblocked(self, user):
        """call when successfully unblocked"""
        if user in self._blocklist:
            self._blocklist.remove(user)
            self._call_event("on_pm_unblock", user)

    ####
    # Commands
    ####
    def ping(self):
        """send a ping"""
        self._send_command("")
        self._call_event("on_pm_ping")

    def message(self, user, msg):
        """send a pm to a user"""
        if msg is not None:
            self._send_command("msg", user.name, '<n7/><m v="1">%s</m>' % msg)

    def add_contact(self, user):
        """add contact"""
        if user not in self._contacts:
            self._send_command("wladd", user.name)
            self._contacts.add(user)
            self._call_event("on_pm_contact_add", user)

    def remove_contact(self, user):
        """remove contact"""
        if user in self._contacts:
            self._send_command("wldelete", user.name)
            self._contacts.remove(user)
            self._call_event("on_pm_contact_remove", user)

    def block(self, user):
        """block a person"""
        if user not in self._blocklist:
            self._send_command("block", user.name, user.name, "S")
            self._blocklist.add(user)
            self._call_event("on_pm_block", user)

    def unblock(self, user):
        """unblock a person"""
        if user in self._blocklist:
            self._send_command("unblock", user.name)

    def track(self, user):
        """get and store status of person for future use"""
        self._send_command("track", user.name)

    def check_online(self, user):
        """return True if online, False if offline, None if unknown"""
        if user in self._status:
            return self._status[user][1]
        else:
            return None

    def get_idle(self, user):
        """
        return last active time, time.time() if isn't idle, 0 if offline,
        None if unknown
        """
        if user not in self._status:
            return None
        if not self._status[user][1]:
            return 0
        if not self._status[user][2]:
            return time.time()
        else:
            return self._status[user][2]

    ####
    # Util
    ####
    def _call_event(self, evt, *args, **kw):
        getattr(self.mgr, evt)(self, *args, **kw)
        self.mgr.on_event_called(self, evt, *args, **kw)

    def _write(self, data):
        if self._wlock:
            self._wlockbuf += data
        else:
            self.mgr._write(self, data)

    def _set_write_lock(self, lock):
        self._wlock = lock
        if not self._wlock:
            self._write(self._wlockbuf)
            self._wlockbuf = b""

    def _send_command(self, *args):
        """
        Send a command.

        :type args: [str, str, ...]
        :param args: command and list of arguments
        """
        if self._firstCommand:
            terminator = b"\x00"
            self._firstCommand = False
        else:
            terminator = b"\r\n\x00"
        self._write(":".join(args).encode() + terminator)

    def get_connections(self):
        return [self]


################################################################
# Room class
################################################################
class Room:
    """Manages a connection with a Chatango room."""

    _default_port = 8080 if Use_WebSocket else 443

    ####
    # Init
    ####
    def __init__(self, room_name, uid=None, server=None, port=None, mgr=None):
        """init, don't overwrite"""
        # Basic stuff
        self._room_name = room_name
        self._server = server or getServer(room_name)
        self._port = port or self.__class__._default_port
        self._mgr = mgr

        # Under the hood
        self._connected = False
        self._reconnecting = False
        self._uid = uid or _genUid()
        self._rbuf = b""
        self._wbuf = b""
        self._wlockbuf = b""
        self._owner = None
        self._mods = set()
        self._mqueue = dict()
        self._uqueue = dict()
        self._history = list()
        self._userlist = list()
        self._firstCommand = True
        self._connectAmmount = 0
        self._premium = False
        self._userCount = 0
        self._pingTask = None
        self._botname = None
        self._currentname = None
        self._users = dict()
        self._msgs = dict()
        self._wlock = False
        self._silent = False
        self._banlist = dict()
        self._unbanlist = dict()
        self._headers_parsed = False

        # Inited vars
        if self._mgr:
            self._connect()

    ####
    # Connect/disconnect
    ####
    def _connect(self):
        """Connect to the server."""
        self._sock = socket.socket()
        self._sock.connect((self._server, self._port))
        self._sock.setblocking(False)
        self._firstCommand = True
        self._pingTask = self.mgr.set_internal(self.mgr._ping_delay, self.ping)
        if not self._reconnecting:
            self.connected = True
        self._headers_parsed = False
        if Use_WebSocket:
            self._wbuf = (
                b"GET / HTTP/1.1\r\n"
                + "Host: {}:{}\r\n".format(self._server, self._port).encode()
                + b"Origin: http://st.chatango.com\r\n"
                b"Connection: Upgrade\r\n"
                b"Upgrade: websocket\r\n"
                b"Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==\r\n"
                b"Sec-WebSocket-Version: 13\r\n"
                b"\r\n"
            )
        else:
            self._wbuf = b""
            self._auth()

    def reconnect(self):
        """Reconnect."""
        self._reconnect()

    def _reconnect(self):
        """Reconnect."""
        self._reconnecting = True
        if self.connected:
            self._disconnect()
        self._uid = _genUid()
        self._connect()
        self._reconnecting = False

    def disconnect(self):
        """Disconnect."""
        self._disconnect()
        self._call_event("on_disconnect")

    def _disconnect(self):
        """Disconnect from the server."""
        if not self._reconnecting:
            self.connected = False
        for user in self._userlist:
            user.clear_session_ids(self)
        self._userlist = list()
        self._pingTask.cancel()
        self._sock.close()
        if not self._reconnecting:
            del self.mgr._rooms[self.room_name]

    def _auth(self):
        """Authenticate."""
        # login as name with password
        if self.mgr.name and self.mgr.password:
            self._send_command(
                "bauth", self.room_name, self._uid, self.mgr.name, self.mgr.password
            )
            self._currentname = self.mgr.name
        # login as anon
        else:
            self._send_command("bauth", self.room_name, "", "", "")

        self._set_write_lock(True)

    ####
    # Properties
    ####
    def _get_room_name(self):
        return self._room_name

    def _get_bot_name(self):
        if self.mgr.name and self.mgr.password:
            return self.mgr.name
        elif self.mgr.name and self.mgr.password is None:
            return "#" + self.mgr.name
        elif self.mgr.name is None:
            return self._botname

    def _get_current_name(self):
        return self._currentname

    def _get_manager(self):
        return self._mgr

    def _get_userlist(self, mode=None, unique=None, memory=None):
        ul = None
        if mode is None:
            mode = self.mgr._userlist_mode
        if unique is None:
            unique = self.mgr._userlist_unique
        if memory is None:
            memory = self.mgr._userlist_memory
        if mode == userlist_recent:
            ul = map(lambda x: x.user, self._history[-memory:])
        elif mode == userlist_all:
            ul = self._userlist
        if unique:
            return list(set(ul))
        else:
            return ul

    def _get_user_names(self):
        ul = self.userlist
        return list(map(lambda x: x.name, ul))

    def _get_user(self):
        return self.mgr.user

    def _get_owner(self):
        return self._owner

    def _get_owner_name(self):
        return self._owner.name

    def _get_mods(self):
        newset = set()
        for mod in self._mods:
            newset.add(mod)
        return newset

    def _get_mod_names(self):
        mods = self._get_mods()
        return [x.name for x in mods]

    def _get_user_count(self):
        return self._userCount

    def _get_silent(self):
        return self._silent

    def _set_silent(self, val):
        self._silent = val

    def _get_banlist(self):
        return list(self._banlist.keys())

    def _get_unban_list(self):
        return [
            [record["target"], record["src"]] for record in self._unbanlist.values()
        ]

    room_name = property(_get_room_name)
    botname = property(_get_bot_name)
    currentname = property(_get_current_name)
    mgr = property(_get_manager)
    userlist = property(_get_userlist)
    usernames = property(_get_user_names)
    user = property(_get_user)
    owner = property(_get_owner)
    ownername = property(_get_owner_name)
    mods = property(_get_mods)
    modnames = property(_get_mod_names)
    usercount = property(_get_user_count)
    silent = property(_get_silent, _set_silent)
    banlist = property(_get_banlist)
    unbanlist = property(_get_unban_list)

    ####
    # Feed/process
    ####
    def _feed(self, data):
        """
        Feed data to the connection.

        :type data: bytes
        :param data: data to be fed
        """
        self._rbuf += data
        if Use_WebSocket:
            if not self._headers_parsed and b"\r\n\r\n" in self._rbuf:
                headers, self._rbuf = self._rbuf.split(b"\r\n\r\n", 1)
                key = _ws.check_headers(headers)
                if key != "s3pPLMBiTxaQ9kYGzzhZRbK+xOo=":
                    self._disconnect()
                    self._call_event("on_connect_fail")
                else:
                    self._auth()
                    self._connected = True
                self._headers_parsed = True
            else:
                r = _ws.check_frame(self._rbuf)
                while r:
                    frame = self._rbuf[:r]
                    self._rbuf = self._rbuf[r:]
                    info = _ws.frame_info(frame)
                    payload = _ws.get_payload(frame)
                    if info.opcode == _ws.CLOSE:
                        self._disconnect()
                    elif info.opcode == _ws.TEXT:
                        self._process(payload)
                    elif debug:
                        print(
                            "unhandled frame: "
                            + repr(info)
                            + " with payload "
                            + repr(payload)
                        )
                    r = _ws.check_frame(self._rbuf)
        else:
            while b"\0" in self._rbuf:
                data = self._rbuf.split(b"\x00")
                for food in data[:-1]:
                    self._process(food.decode(errors="replace").rstrip("\r\n"))
                self._rbuf = data[-1]

    def _process(self, data):
        """
        Process a command string.

        :type data: str
        :param data: the command string
        """
        self._call_event("on_raw", data)
        data = data.split(":")
        cmd, args = data[0], data[1:]
        func = "_rcmd_" + cmd
        if hasattr(self, func):
            getattr(self, func)(args)

    ####
    # Received Commands
    ####
    def _rcmd_ok(self, args):
        # if no name, join room as anon and no password
        if args[2] == "N" and self.mgr.password is None and self.mgr.name is None:
            n = args[4].rsplit(".", 1)[0]
            n = n[-4:]
            aid = args[1][0:8]
            pid = "!anon" + _getAnonId(n, aid)
            self._botname = pid
            self._currentname = pid
            self.user._name_color = n
        # if got name, join room as name and no password
        elif args[2] == "N" and self.mgr.password is None:
            self._send_command("blogin", self.mgr.name)
            self._currentname = self.mgr.name
        # if got password but fail to login
        elif args[2] != "M":  # unsuccessful login
            self._call_event("on_login_fail")
            self.disconnect()
        self._owner = get_user(args[0])
        self._uid = args[1]
        self._aid = args[1][4:8]
        self._mods = set(map(lambda x: get_user(x.split(",")[0]), args[6].split(";")))
        self._i_log = list()

    def _rcmd_denied(self, args):
        self._disconnect()
        self._call_event("on_connect_fail")

    def _rcmd_inited(self, args):
        self._send_command("g_participants", "start")
        self._send_command("getpremium", "1")
        self.request_banlist()
        self.request_unbanlist()
        if self._connectAmmount == 0:
            self._call_event("on_connect")
            for msg in reversed(self._i_log):
                user = msg.user
                self._call_event("on_history_message", user, msg)
                self._add_history(msg)
            del self._i_log
        else:
            self._call_event("on_reconnect")
        self._connectAmmount += 1
        self._set_write_lock(False)

    def _rcmd_premium(self, args):
        if float(args[1]) > time.time():
            self._premium = True
            if self.user._mbg:
                self.set_bg_mode(1)
            if self.user._mrec:
                self.set_recording_mode(1)
        else:
            self._premium = False

    def _rcmd_mods(self, args):
        modnames = args
        mods = set(map(lambda x: get_user(x.split(",")[0]), modnames))
        premods = self._mods
        for user in mods - premods:  # modded
            self._mods.add(user)
            self._call_event("on_mod_add", user)
        for user in premods - mods:  # demodded
            self._mods.remove(user)
            self._call_event("on_mod_remove", user)
        self._call_event("on_mod_change")

    def _rcmd_b(self, args):
        mtime = float(args[0])
        puid = args[3]
        ip = args[6]
        name = args[1]
        channels = int(args[7])
        channels = tuple(x for x, y in Channels.items() if channels & y)
        rawmsg = ":".join(args[9:])
        msg, n, f = _clean_message(rawmsg)
        if name == "":
            name_color = None
            name = "#" + args[2]
            if name == "#":
                name = "!anon" + _getAnonId(n, puid)
        else:
            if n:
                name_color = _parseNameColor(n)
            else:
                name_color = None
        i = args[5]
        unid = args[4]
        user = get_user(name)
        # Create an anonymous message and queue it because msgid is unknown.
        if f:
            font_color, font_face, font_size = _parse_font(f)
        else:
            font_color, font_face, font_size = None, None, None
        msg = Message(
            time=mtime,
            user=user,
            body=msg,
            raw=rawmsg,
            ip=ip,
            name_color=name_color,
            font_color=font_color,
            font_face=font_face,
            font_size=font_size,
            unid=unid,
            puid=puid,
            channels=channels,
            room=self,
        )
        self._mqueue[i] = msg

    def _rcmd_u(self, args):
        temp = Struct(**self._mqueue)
        if hasattr(temp, args[0]):
            msg = getattr(temp, args[0])
            if msg.user != self.user:
                msg.user._font_color = msg.font_color
                msg.user._font_face = msg.font_face
                msg.user._font_size = msg.font_size
                msg.user._name_color = msg.name_color
            del self._mqueue[args[0]]
            msg.attach(self, args[1])
            self._add_history(msg)
            self._call_event("on_message", msg.user, msg)
        # possible this came first (out of order)
        else:
            self._uqueue[args[0]] = args[1]

    def _rcmd_i(self, args):
        mtime = float(args[0])
        puid = args[3]
        ip = args[6]
        name = args[1]
        rawmsg = ":".join(args[9:])
        msg, n, f = _clean_message(rawmsg)
        if name == "":
            name_color = None
            name = "#" + args[2]
            if name == "#":
                name = "!anon" + _getAnonId(n, puid)
        else:
            if n:
                name_color = _parseNameColor(n)
            else:
                name_color = None
        i = args[5]
        unid = args[4]
        user = get_user(name)
        # Create an anonymous message and queue it because msgid is unknown.
        if f:
            font_color, font_face, font_size = _parse_font(f)
        else:
            font_color, font_face, font_size = None, None, None
        msg = Message(
            time=mtime,
            user=user,
            body=msg,
            raw=rawmsg,
            ip=ip,
            name_color=name_color,
            font_color=font_color,
            font_face=font_face,
            font_size=font_size,
            unid=unid,
            puid=puid,
            room=self,
        )

        # check if the msgid was already received
        temp = Struct(**self._uqueue)
        if hasattr(temp, i):
            msgid = getattr(temp, i)
            if msg.user != self.user:
                msg.user._font_color = msg.font_color
                msg.user._font_face = msg.font_face
                msg.user._font_size = msg.font_size
                msg.user._name_color = msg.name_color
            del self._uqueue[i]
            msg.attach(self, msgid)
            self._add_history(msg)
            self._call_event("on_message", msg.user, msg)
        else:
            self._mqueue[i] = msg

    def _rcmd_g_participants(self, args):
        args = ":".join(args)
        args = args.split(";")
        for data in args:
            data = data.split(":")
            name = data[3].lower()
            if name == "none":
                continue
            user = get_user(name=name, room=self)
            user.add_session_id(self, data[0])
            self._userlist.append(user)

    def _rcmd_participant(self, args):
        name = args[3].lower()
        if name == "none":
            return
        user = get_user(name)
        puid = args[2]

        if args[0] == "0":  # leave
            user.remove_session_id(self, args[1])
            self._userlist.remove(user)
            if user not in self._userlist or not self.mgr._userlist_event_unique:
                self._call_event("on_leave", user, puid)
        else:  # join
            user.add_session_id(self, args[1])
            if user not in self._userlist:
                doEvent = True
            else:
                doEvent = False
            self._userlist.append(user)
            if doEvent or not self.mgr._userlist_event_unique:
                self._call_event("on_join", user, puid)

    def _rcmd_show_fw(self, args):
        self._call_event("on_flood_warning")

    def _rcmd_show_tb(self, args):
        self._call_event("on_flood_ban")

    def _rcmd_tb(self, args):
        self._call_event("on_flood_ban_repeat")

    def _rcmd_delete(self, args):
        msg = self._msgs.get(args[0])
        if msg:
            if msg in self._history:
                self._history.remove(msg)
                self._call_event("on_message_delete", msg.user, msg)
                msg.detach()

    def _rcmd_deleteall(self, args):
        for msgid in args:
            self._rcmd_delete([msgid])

    def _rcmd_n(self, args):
        self._userCount = int(args[0], 16)
        self._call_event("on_user_count_change")

    def _rcmd_blocklist(self, args):
        self._banlist = dict()
        sections = ":".join(args).split(";")
        for section in sections:
            params = section.split(":")
            if len(params) != 5:
                continue
            if params[2] == "":
                continue
            user = get_user(params[2])
            self._banlist[user] = {
                "unid": params[0],
                "ip": params[1],
                "target": user,
                "time": float(params[3]),
                "src": get_user(params[4]),
            }
        self._call_event("on_banlist_update")

    def _rcmd_unblocklist(self, args):
        self._unbanlist = dict()
        sections = ":".join(args).split(";")
        for section in sections:
            params = section.split(":")
            if len(params) != 5:
                continue
            if params[2] == "":
                continue
            user = get_user(params[2])
            self._unbanlist[user] = {
                "unid": params[0],
                "ip": params[1],
                "target": user,
                "time": float(params[3]),
                "src": get_user(params[4]),
            }
        self._call_event("on_unbanlist_update")

    def _rcmd_blocked(self, args):
        if args[2] == "":
            return
        target = get_user(args[2])
        user = get_user(args[3])
        self._banlist[target] = {
            "unid": args[0],
            "ip": args[1],
            "target": target,
            "time": float(args[4]),
            "src": user,
        }
        self._call_event("on_ban", user, target)

    def _rcmd_unblocked(self, args):
        if args[2] == "":
            return
        target = get_user(args[2])
        user = get_user(args[3])
        del self._banlist[target]
        self._unbanlist[user] = {
            "unid": args[0],
            "ip": args[1],
            "target": target,
            "time": float(args[4]),
            "src": user,
        }
        self._call_event("on_unban", user, target)

    ####
    # Commands
    ####
    def login(self, name, password=None):
        """login as a user or set a name in room"""
        if password:
            self._send_command("blogin", name, password)
        else:
            self._send_command("blogin", name)
        self._currentname = name

    def logout(self):
        """logout of user in a room"""
        self._send_command("blogout")
        self._currentname = self._botname

    def ping(self):
        """Send a ping."""
        self._send_command("")
        self._call_event("on_ping")

    def raw_message(self, msg):
        """
        Send a message without n and f tags.

        :type msg: str
        :param msg: message
        """
        if not self._silent:
            self._send_command("bmsg:tl2r", msg)

    def message(self, msg, **kwargs):
        """
        message(msg, html=False, channels=None)
        Send a message. (Use "\\n" or "\\r" for new line)

        :param str msg: message
        :param Optional[str] html: escape html characters
        :param Tuple channels: channels of the message
        """
        if msg is None:
            return
        msg = msg.rstrip()
        if not kwargs.get("html"):
            msg = html.escape(msg)
        channels = kwargs.get("channels")
        channels_flags = 0
        if channels:
            for v in channels:
                if v.lower() in Channels:
                    channels_flags |= Channels[v.lower()]
        if len(msg) > self.mgr._max_length:
            if self.mgr._too_big_message == BigMessage_Cut:
                self.message(msg[: self.mgr._max_length], **kwargs)
            elif self.mgr._too_big_message == big_message_multiple:
                while len(msg) > 0:
                    sect = msg[: self.mgr._max_length]
                    msg = msg[self.mgr._max_length :]
                    self.message(sect, **kwargs)
            return
        font_properties = '<f x%0.2i%s="%s">' % (
            self.user.font_size,
            self.user.font_color,
            self.user.font_face,
        )
        # chatango uses \r as a newline character
        # using a \n would break the connection
        msg = msg.replace("\n", "\r")
        msg = msg.replace("~", "&#126;")
        msg = font_properties + msg
        # anons can't use custom name colors
        if self.mgr._password is not None:
            msg = "<n" + self.user.name_color + "/>" + msg
        if channels_flags:
            self._send_command("bm", "ibrs", str(channels_flags), msg)
        else:
            self.raw_message(msg)

    def set_bg_mode(self, mode):
        """turn on/off bg"""
        self._send_command("msgbg", str(mode))

    def set_recording_mode(self, mode):
        """turn on/off rcecording"""
        self._send_command("msgmedia", str(mode))

    def add_mod(self, user):
        """
        Add a moderator.

        :type user: User
        :param user: User to mod.
        """
        if self.get_level(get_user(self.currentname)) == 2:
            self._send_command("addmod", user.name)

    def remove_mod(self, user):
        """
        Remove a moderator.

        :type user: User
        :param user: User to demod.
        """
        if self.get_level(get_user(self.currentname)) == 2:
            self._send_command("removemod", user.name)

    def flag(self, message):
        """
        Flag a message.

        :type message: Message
        :param message: message to flag
        """
        self._send_command("g_flag", message.msgid)

    def flag_user(self, user):
        """
        Flag a user.

        :param User user: User to flag

        @rtype: bool
        @return: whether a message to flag was found
        """
        msg = self.get_last_message(user)
        if msg:
            self.flag(msg)
            return True
        return False

    def delete_message(self, message):
        """
        Delete a message. (Moderator only)

        :type message: Message
        :param message: message to delete
        """
        if self.get_level(self.user) > 0:
            self._send_command("delmsg", message.msgid)

    def delete_user(self, user):
        """
        Delete a message. (Moderator only)

        :param user: Delete user's last message.
        :type user: User
        """
        if self.get_level(self.user) > 0:
            msg = self.get_last_message(user)
            if msg:
                self._send_command("delmsg", msg.msgid)
            return True
        return False

    def delete(self, message):
        """
        compatibility wrapper for deleteMessage
        """
        print("[obsolete] the delete function is obsolete, " "please use deleteMessage")
        return self.delete_message(message)

    def raw_clear_user(self, unid, ip, user):
        self._send_command("delallmsg", unid, ip, user)

    def clear_user(self, user: bool):
        """
        Clear all of a user's messages. (Moderator only)

        :param User user: user to delete messages of.

        :return bool: whether a message to delete was found
        """
        if self.get_level(self.user) > 0:
            msg = self.get_last_message(user)
            if msg:
                if msg.user.name[0] in ["!", "#"]:
                    self.raw_clear_user(msg.unid, msg.ip, "")
                else:
                    self.raw_clear_user(msg.unid, msg.ip, msg.user.name)
                return True
        return False

    def clear_all(self):
        """Clear all messages. (Owner only)"""
        if self.get_level(self.user) == 2:
            self._send_command("clearall")

    def raw_ban(self, name, ip, unid):
        """
        Execute the block command using specified arguments.
        (For advanced usage)

        :param str name: name
        :param str ip: ip address
        :param str unid: unid
        """
        self._send_command("block", unid, ip, name)

    def ban(self, msg):
        """
        Ban the author of a given message. (Moderator only)

        :param msg: message to ban sender of
        :type msg: Message
        """
        if self.get_level(self.user) > 0:
            self.raw_ban(msg.user.name, msg.ip, msg.unid)

    def ban_user(self, user):
        """
        Ban a user. (Moderator only)

        :param user: Chatango user to ban from room.
        :type user: User

        @rtype: bool
        @return: whether a message to ban the user was found
        """
        msg = self.get_last_message(user)
        if msg:
            self.ban(msg)
            return True
        return False

    def request_banlist(self):
        """Request an updated banlist."""
        self._send_command("blocklist", "block", "", "next", "500")

    def request_unbanlist(self):
        """Request an updated banlist."""
        self._send_command("blocklist", "unblock", "", "next", "500")

    def raw_unban(self, name, ip, unid):
        """
        Execute the unblock command using specified arguments.
        (For advanced usage)

        :type name: str
        :param name: name
        :type ip: str
        :param ip: ip address
        :type unid: str
        :param unid: unid
        """
        self._send_command("removeblock", unid, ip, name)

    def unban(self, user):
        """
        Unban a user. (Moderator only)

        :param user: Chatango user to unban from room.
        :type user: User

        @rtype: bool
        @return: whether it succeeded
        """
        rec = self._get_ban_record(user)
        if rec:
            self.raw_unban(rec["target"].name, rec["ip"], rec["unid"])
            return True
        else:
            return False

    ####
    # Util
    ####
    def _get_ban_record(self, user):
        if user in self._banlist:
            return self._banlist[user]
        return None

    def _call_event(self, evt, *args, **kw):
        getattr(self.mgr, evt)(self, *args, **kw)
        self.mgr.on_event_called(self, evt, *args, **kw)

    def _write(self, data):
        if self._wlock:
            self._wlockbuf += data
        else:
            self.mgr._write(self, data)

    def _set_write_lock(self, lock):
        self._wlock = lock
        if not self._wlock:
            self._write(self._wlockbuf)
            self._wlockbuf = b""

    def _send_command(self, *args):
        """
        Send a command.

        :type args: [str, str, ...]
        :param args: command and list of arguments
        """
        if self._firstCommand:
            terminator = "\0"
            self._firstCommand = False
        else:
            terminator = "\r\n\0"
        payload = ":".join(args) + terminator
        if Use_WebSocket:
            frame = _ws.encode_frame(mask=True, payload=payload)
            self._write(frame)
        else:
            self._write(payload.encode())

    def get_level(self, user):
        """get the level of user in a room"""
        if user == self._owner:
            return 2
        if user.name in self.modnames:
            return 1
        return 0

    def get_last_message(self, user=None):
        """get last message said by user in a room"""
        if user:
            try:
                i = 1
                while True:
                    msg = self._history[-i]
                    if msg.user == user:
                        return msg
                    i += 1
            except IndexError:
                return None
        else:
            try:
                return self._history[-1]
            except IndexError:
                return None

    def find_user(self, name):
        """
        check if user is in the room

        return User(name) if name in room else None
        """
        name = name.lower()
        ul = self._get_userlist()
        udi = dict(zip([u.name for u in ul], ul))
        cname = None
        for n in udi.keys():
            if name in n:
                if cname:
                    return None  # ambiguous!!
                cname = n
        if cname:
            return udi[cname]
        else:
            return None

    ####
    # History
    ####
    def _add_history(self, msg):
        """
        Add a message to history.

        :type msg: Message
        :param msg: message
        """
        self._history.append(msg)
        if len(self._history) > self.mgr._max_history_length:
            rest = self._history[: -self.mgr._max_history_length]
            self._history = self._history[-self.mgr._max_history_length :]
            for msg in rest:
                msg.detach()


################################################################
# RoomManager class
################################################################
class RoomManager:
    """Class that manages multiple connections."""

    ####
    # Config
    ####
    _Room = Room
    _PM = PM
    _ANON_PM = ANON_PM
    _anon_pm_host = "b1.chatango.com"
    _pm_host = "c1.chatango.com"
    _pm_port = 5222
    _timer_resolution = 0.2  # at least x times per second
    _ping_delay = 20
    _userlist_mode = userlist_recent
    _userlist_unique = True
    _userlist_memory = 50
    _userlist_event_unique = False
    _too_big_message = big_message_multiple
    _max_length = 2500
    _max_history_length = 150

    ####
    # Init
    ####
    def __init__(self, name=None, password=None, pm=True):
        self._name = name
        self._password = password
        self._running = False
        self._tasks = set()
        self._rooms = dict()
        self._rooms_queue = queue.Queue()
        self._rooms_lock = threading.Lock()
        if pm:
            if self._password:
                self._pm = self._PM(mgr=self)
            else:
                self._pm = self._ANON_PM(mgr=self)
        else:
            self._pm = None

    def _join_thread(self):
        while True:
            room = self._rooms_queue.get()
            with self._rooms_lock:
                con = self._Room(room, mgr=self)
                self._rooms[room] = con

    ####
    # Join/leave
    ####
    def join_room(self, room):
        """
        Join a room or return None if already joined.

        :param str room: Name of Chatango room to join.

        :returns: True or None depending on if Room is joined
        """
        if room not in self._rooms:
            self._rooms_queue.put(room)
            return True
        return None

    def leave_room(self, room):
        """
        Leave a room.

        :type room: str
        :param room: room to leave
        """
        if room in self._rooms:
            with self._rooms_lock:
                con = self._rooms[room]
                con.disconnect()

    def get_room(self, room):
        """
        Get room with a name, or None if not connected to this room.

        :type room: str
        :param room: room

        @rtype: Room
        @return: the room
        """
        if room in self._rooms:
            return self._rooms[room]
        return None

    ####
    # Properties
    ####
    def _get_user(self):
        return get_user(self._name)

    def _get_name(self):
        return self._name

    def _get_password(self):
        return self._password

    def _get_rooms(self):
        return set(self._rooms.values())

    def _get_room_names(self):
        return set(self._rooms.keys())

    def _get_pm(self):
        return self._pm

    user = property(_get_user)
    name = property(_get_name)
    password = property(_get_password)
    rooms = property(_get_rooms)
    room_names = property(_get_room_names)
    pm = property(_get_pm)

    ####
    # Virtual methods
    ####
    def on_init(self):
        """Called on init."""
        pass

    @staticmethod
    def safe_print(text):
        """Use this to safely print text with unicode"""
        while True:
            try:
                print(text)
                break
            except UnicodeError as ex:
                text = text[0 : ex.start] + "(unicode)" + text[ex.end :]

    def on_connect(self, room):
        """
        Called when connected to the room.

        :param room: Chatango room recently joined by bot.
        :type room: Room
        """
        room.message("Beep boop I'm dead inside 🤖")
        LOGGER.success(
            f"[{room.room_name}] [{self.user.name}]: Successfully connected to {room.room_name}"
        )

    def on_reconnect(self, room: Room):
        """
        Called when reconnected to the room.

        :param Room room: Chatango room where the event occurred.
        """
        LOGGER.success(f"Successfully connected to {room.room_name}.")

    def on_connect_fail(self, room: Room):
        """
        Called when the connection failed.

        :param Room room: Chatango room where the event occurred
        """
        LOGGER.error(f"Failed to connect to {room.room_name}.")
        self.set_timeout(1200, self.stop)
        LOGGER.info(f"Attempting to connect to {room.room_name} again...")
        self.set_timeout(1200, self.join_room(room))

    def on_disconnect(self, room: Room):
        """
        Called when the client gets disconnected.

        :param Room room: Chatango room where the event occurred
        """
        LOGGER.error(f"Disconnected from {room.room_name}.")
        self.set_timeout(60, self.stop)
        LOGGER.info(f"Attempting to reconnect to {room.room_name}...")
        self.set_timeout(60, self.join_room(room))

    def on_login_fail(self, room: Room):
        """
        Called on login failure, disconnects after.

        :param Room room: Chatango room where the event occurred
        """
        LOGGER.error(f"Failed to join {room.room_name}. Attempting to rejoin...")
        self.on_connect_fail(room)

    @staticmethod
    def on_flood_ban(room: Room):
        """
        Called when either flood banned or flagged.

        :param room: Chatango room where the event occurred
        :type room: Room
        """
        LOGGER.error(f"Bot was spam banned from {room.room_name}.")

    def on_flood_ban_repeat(self, room):
        """
        Called when trying to send something when flood-banned.

        :param Room room: Chatango room where the event occurred
        """
        pass

    @staticmethod
    def on_flood_warning(room: Room):
        """
        Called when an overflow warning gets received.

        :param room: Chatango room where the event occurred
        :type room: Room
        """
        LOGGER.error(f"Bot is about to be banned for spamming {room.room_name}.")

    @staticmethod
    def on_message_delete(room: Room, user, message):
        """
        Listener for when a user message gets deleted.

        :param Room room: Chatango room where the event occurred
        :param User user: Chatango user who sent deleted message.
        :param Message message: User message that got deleted.
        """
        if user.name.lower() != CHATANGO_USERS.keys():
            LOGGER.info(
                f"[{room.room_name}] [{user.name.title()}] [no IP address]: {user.name} had message deleted from {room.room_name}: {message.body}",
            )

    def on_mod_change(self, room):
        """
        Called when the moderator list changes.

        :param Room room: Chatango room where the event occurred.
        """
        pass

    @staticmethod
    def on_mod_add(room: Room, user):
        """
        Logs event when a user gets modded.

        :param Room room: Chatango room where user was modded.
        :param User user: User promoted to mod.
        """
        LOGGER.info(
            f"[{room.room_name}] [{user.name.title()}] [no IP address]: {user.name} was modded in {room.room_name}."
        )

    @staticmethod
    def on_mod_remove(room: Room, user):
        """
        Called when a moderator gets removed.

        :param Room room: Chatango room where user was demodded.
        :param User user: User demoted from mod.
        """
        LOGGER.info(
            f"[{room.room_name}] [{user.name.title()}] [no IP address]: {user.name} was demodded in {room.room_name}.",
        )

    def on_message(self, room, user, message):
        """
        Called when a message gets received.

        :param Room room: Chatango room which received a message.
        :param User user: Author of message sent to chat.
        :param Message message: Received chat message
        """
        if bool(message.ip):
            LOGGER.info(
                f"[{room.room_name}] [{user.name}] [{message.ip}]: {message.body}"
            )
        else:
            LOGGER.info(
                f"[{room.room_name}] [{user.name}] [no IP address]: {message.body}"
            )

    def on_history_message(self, room, user, message):
        """
        Called when a message gets received from history.

        :param Room room: Chatango room where a user message was retrieved from history.
        :param User user: Author of the original chat message.
        :param Message message: Chat message which was retrieved.
        """
        pass

    @staticmethod
    def on_join(room, user, puid):
        """
        Called when a user joins. Anonymous users get ignored here.

        :param Room room: Chatango room where a user joined.
        :param User user: Recently joined user.
        :param str puid: Personal unique id for a user.
        """
        LOGGER.info(
            f"[{room.room_name}] [{user.name.title()}] [no IP address]: {user.name} joined {room.room_name}.",
        )

    @staticmethod
    def on_leave(room: Room, user, puid):
        """
        Called when a user leaves. Anonymous users get ignored here.

        :param Room room: Chatango room where a user left.
        :param User user: Recently departed user.
        :param str puid: Personal unique id for a user.
        """
        LOGGER.info(
            f"[{room.room_name}] [{user.name.title()}] [no IP address]: {user.name} left {room.room_name}.",
        )

    def on_raw(self, room: Room, raw):
        """
        Called before any command parsing occurs.

        :param Room room: Chatango room where the event occurred.
        :param str raw: Raw message data
        """
        pass

    def on_ping(self, room):
        """
        Called when a ping gets sent.

        :param room: Chatango room to ping.
        :type room: Room
        """
        pass

    def on_user_count_change(self, room):
        """
        Called when the user count changes.

        :param room: Chatango room where users are actively joining/leaving.
        :type room: Room
        """
        pass

    @staticmethod
    def on_ban(room: Room, user, target):
        """
        Called when a user gets banned.

        :param Room room: Chatango room where user was unbanned.
        :param User user: Moderator who unbanned user.
        :param User target: User that got unbanned.
        """
        LOGGER.info(
            f"[{room.room_name}] [{user.name.title()}] [no IP address]: {target.name} was banned from {room.room_name} by {user.name}.",
        )

    @staticmethod
    def on_unban(room, user, target):
        """
        Called when a user gets unbanned.

        :param Room room: Chatango room where user was unbanned.
        :param User user: Moderator who unbanned user.
        :param User target: User that got unbanned.
        """
        LOGGER.info(
            f"[{room.room_name}] [{user.name.title()}] [no IP address]: {target.name} was unbanned from {room.room_name} by {user.name}.",
        )

    def on_banlist_update(self, room: Room):
        """
        Called when a banlist gets updated.

        :param Room room: Chatango room where the event occurred.
        """
        pass

    def on_unbanlist_update(self, room):
        """
        Called when a unbanlist gets updated.

        :param room: Chatango room where the event occurred.
        :type room: Room
        """
        pass

    def on_pm_connect(self, pm: PM):
        """
        Triggered when a direct message is received.

        :param PM pm: Private message.
        """
        pass

    def on_anon_pm_disconnect(self, pm, user):
        """
        Called when disconnected from the pm

        :param PM pm: Private message.
        """
        pass

    def on_pm_disconnect(self, pm):
        """
        Called when disconnected from the pm

        :param PM pm: Private message.
        """
        pass

    def on_pm_ping(self, pm):
        """
        Called when sending a ping to the pm

        :param PM pm: Private message.
        """
        pass

    def on_pm_message(self, pm, user, body):
        """
        Called when a private message is received.

        :param PM pm: Private message.
        :param User user: User who sent message.
        :param Message body: Received message.
        """
        pass

    def on_pm_offline_message(self, pm, user, body):
        """
        Called when connected if a message is received while offline

        :param PM pm: the pm
        :param User user: owner of message
        :param Message body: received message
        """
        pass

    def on_pm_contactlist_receive(self, pm):
        """
        Called when the contact list is received

        :param PM pm: Private message.
        """
        pass

    def on_pm_blocklist_receive(self, pm):
        """
        Called when the block list is received

        :param PM pm: Private message.
        """
        pass

    def on_pm_contact_add(self, pm, user):
        """
        Triggered user is added as a friend from a private message.

        :param PM pm: Private message.
        :param User user: Newly added contact.
        """
        pass

    def on_pm_contact_remove(self, pm, user):
        """
        Triggered user is removed as a friend from a private message.

        :param PM pm: Private message.
        :param User user: Newly removed contact.
        """
        pass

    def on_pm_block(self, pm: PM, user):
        """
        Called when successfully block a user

        :param PM pm: Private message.
        :param User user: Blocked user.
        """
        pass

    def on_pm_unblock(self, pm, user):
        """
        Called when successfully unblock a user

        :param PM pm: Private message.
        :param User user: Unblocked user.
        """
        pass

    def on_pm_contact_online(self, pm, user):
        """
        Called when a user from the contact come online

        :param PM pm: Private message.
        :param User user: Contact that came online.
        """
        pass

    def on_pm_contact_offline(self, pm, user):
        """
        Called when a user from the contact go offline

        :param PM pm: Private message.
        :param User user: Contact that went offline.
        """
        pass

    def on_event_called(self, room, evt, *args, **kw):
        """
        Called on every room-based event.

        :param Room room: Chatango room where the event occurred.
        :param str evt: Any given event.
        """
        pass

    ####
    # Deferring
    ####
    def defer_to_thread(self, callback, func, *args, **kw):
        """
        Defer a function to a thread and callback the return value.

        :param Callable callback: function to call on completion
        :param Callable func: function to call
        """

        def f(func, callback, *args, **kw):
            ret = func(*args, **kw)
            self.set_timeout(0, callback, ret)

        threading._start_new_thread(f, (func, callback) + args, kw)

    ####
    # Scheduling
    ####
    class _Task:
        def cancel(self):
            """Sugar for remove_task."""
            self.mgr.remove_task(self)

    def _tick(self):
        now = time.time()
        for task in set(self._tasks):
            if task.target <= now:
                task.func(*task.args, **task.kw)
                if task.isInterval:
                    task.target = now + task.timeout
                else:
                    self._tasks.remove(task)

    def set_timeout(self, timeout, func, *args, **kw):
        """
        Call a function after at least timeout seconds with specified
        arguments.

        :param int timeout: Number of seconds prior to executing a passed function.
        :param Callable func: Function to call.

        :returns: Task object wrapping the function.
        """
        task = self._Task()
        task.mgr = self
        task.target = time.time() + timeout
        task.timeout = timeout
        task.func = func
        task.isInterval = False
        task.args = args
        task.kw = kw
        self._tasks.add(task)
        return task

    def set_internal(self, timeout, func, *args, **kw):
        """
        Call a function at least every timeout seconds with specified
        arguments.

        :param int timeout: timeout
        :param Callable func: function to call

        :returns: Task object wrapping the function.
        """
        task = self._Task()
        task.mgr = self
        task.target = time.time() + timeout
        task.timeout = timeout
        task.func = func
        task.isInterval = True
        task.args = args
        task.kw = kw
        self._tasks.add(task)
        return task

    def remove_task(self, task):
        """
        Cancel a task.

        :param _Task task: task to cancel
        """
        self._tasks.remove(task)

    ####
    # Util
    ####
    def _write(self, room, data):
        room._wbuf += data

    def get_connections(self):
        li = list(self._rooms.values())
        if self._pm:
            li.extend(self._pm.get_connections())
        return [c for c in li if c._sock is not None]

    ####
    # Main
    ####
    def main(self):
        self.on_init()
        self._running = True
        for l in range(0, Number_of_Threads):
            t = threading.Thread(target=self._join_thread)
            t.daemon = True
            t.start()
        while self._running:
            conns = self.get_connections()
            socks = [x._sock for x in conns]
            wsocks = [x._sock for x in conns if x._wbuf != b""]
            if not (socks or wsocks):
                self._tick()
                continue
            rd, wr, sp = select.select(socks, wsocks, [], self._timer_resolution)
            for sock in rd:
                con = [c for c in conns if c._sock == sock][0]
                try:
                    data = sock.recv(8192)
                    if data:
                        con._feed(data)
                    else:
                        con.disconnect()
                except socket.error:
                    if debug:
                        raise
            for sock in wr:
                con = [c for c in conns if c._sock == sock][0]
                try:
                    size = sock.send(con._wbuf)
                    con._wbuf = con._wbuf[size:]
                except socket.error:
                    if debug:
                        raise
            self._tick()

    @classmethod
    def easy_start(cls, rooms=None, name=None, password=None):
        """
        Prompts the user for missing info, then starts.

        :param List[Room] rooms: rooms to join
        :param str name: Username to join as ("" = None, None = unspecified)
        :param str password: User's password to join with ("" = None, None = unspecified)
        """
        if not rooms:
            rooms = input("Room names separated by semicolons: ").split(";")
            rooms = [x.strip() for x in rooms if x.strip()]
        if not name:
            name = input("User name: ")
        if name == "":
            name = None
        if not password:
            password = input("User password: ")
        if password == "":
            password = None
        self = cls(name=name, password=password)
        for room in rooms:
            self.join_room(room)
        self.main()

    def stop(self):
        for conn in list(self._rooms.values()):
            conn.disconnect()
        self._running = False

    ####
    # Commands
    ####
    def enable_bg(self):
        """Enable background if available."""
        self.user._mbg = True
        for room in self.rooms:
            room.set_bg_mode(1)

    def disable_bg(self):
        """Disable background."""
        self.user._mbg = False
        for room in self.rooms:
            room.set_bg_mode(0)

    def enable_recording(self):
        """Enable recording if available."""
        self.user._mrec = True
        for room in self.rooms:
            room.set_recording_mode(1)

    def disable_recording(self):
        """Disable recording."""
        self.user._mrec = False
        for room in self.rooms:
            room.set_recording_mode(0)

    def set_name_color(self, color3x):
        """
        Set name color.

        :param str color3x: a 3-char RGB hex code for the color
        """
        self.user._name_color = color3x

    def set_font_color(self, color3x):
        """
        Set font color.

        :param str color3x: a 3-char RGB hex code for the color
        """
        self.user._font_color = color3x

    def set_font_face(self, face):
        """
        Set font face/family.

        :param str face: the font face
        """
        self.user._font_face = face

    def set_font_size(self, size):
        """
        Set font size.

        :type size: int
        :param size: the font size (limited: 9 to 22)
        """
        if size < 9:
            size = 9
        if size > 22:
            size = 22
        self.user._font_size = size


################################################################
# User class (well, yeah, I lied, it's actually User)
################################################################
_users = dict()


def get_user(name, *args, **kw):
    if name is None:
        name = ""
    name = name.lower()
    user = _users.get(name)
    if not user:
        user = User(name=name, *args, **kw)
        _users[name] = user
    return user


class User:
    """Class that represents a user."""

    def __init__(self, name, **kw):
        self._name = name.lower()
        self._sids = dict()
        self._msgs = list()
        self._name_color = "000"
        self._font_size = 12
        self._font_face = "0"
        self._font_color = "000"
        self._mbg = False
        self._mrec = False
        for attr, val in kw.items():
            if val is None:
                continue
            setattr(self, "_" + attr, val)

    ####
    # Properties
    ####
    def _get_user_name(self):
        return self._name

    def _get_session_ids(self, room=None):
        if room:
            return self._sids.get(room, set())
        else:
            return set.union(*self._sids.values())

    def _get_rooms(self):
        return self._sids.keys()

    def _get_room_names(self):
        return [room.room_name for room in self._get_rooms()]

    def _get_font_color(self):
        return self._font_color

    def _get_font_face(self):
        return self._font_face

    def _get_font_size(self):
        return self._font_size

    def _get_name_color(self):
        return self._name_color

    name = property(_get_user_name)
    session_ids = property(_get_session_ids)
    rooms = property(_get_rooms)
    room_names = property(_get_room_names)
    font_color = property(_get_font_color)
    font_face = property(_get_font_face)
    font_size = property(_get_font_size)
    name_color = property(_get_name_color)

    ####
    # Util
    ####
    def add_session_id(self, room, sid):
        if room not in self._sids:
            self._sids[room] = set()
        self._sids[room].add(sid)

    def remove_session_id(self, room, sid):
        try:
            self._sids[room].remove(sid)
            if len(self._sids[room]) == 0:
                del self._sids[room]
        except KeyError:
            pass

    def clear_session_ids(self, room):
        try:
            del self._sids[room]
        except KeyError:
            pass

    def has_session_id(self, room, sid):
        try:
            if sid in self._sids[room]:
                return True
            else:
                return False
        except KeyError:
            return False

    def __repr__(self):
        return "<User: %s>" % self.name


################################################################
# Message class
################################################################
class Message:
    """Class that represents a message."""

    ####
    # Attach/detach
    ####
    def attach(self, room, msgid):
        """
        Attach the Message to a message id.

        :param Room room: Chatango room to attach message to.
        :param str msgid: message id
        """
        if self._msgid is None:
            self._room = room
            self._msgid = msgid
            self._room._msgs[msgid] = self

    def detach(self):
        """Detach the Message."""
        if self._msgid is not None and self._msgid in self._room._msgs:
            del self._room._msgs[self._msgid]
            self._msgid = None

    def delete(self):
        self._room.delete_message(self)

    ####
    # Init
    ####
    def __init__(self, **kw):
        """init, don't overwrite"""
        self._msgid = None
        self._time = None
        self._user = None
        self._body = None
        self._room = None
        self._raw = ""
        self._ip = None
        self._unid = ""
        self._puid = ""
        self._uid = ""
        self._name_color = "000"
        self._font_size = 12
        self._font_face = "0"
        self._font_color = "000"
        self._channels = ()
        for attr, val in kw.items():
            if val is None:
                continue
            setattr(self, "_" + attr, val)

    ####
    # Properties
    ####
    def _get_id(self):
        return self._msgid

    def _get_time(self):
        return self._time

    def _get_msg_user(self):
        return self._user

    def _get_body(self):
        return self._body

    def _get_ip(self):
        return self._ip

    def _get_font_color(self):
        return self._font_color

    def _get_font_face(self):
        return self._font_face

    def _get_font_size(self):
        return self._font_size

    def _get_name_color(self):
        return self._name_color

    def _get_room(self):
        return self._room

    def _get_raw(self):
        return self._raw

    def _get_unid(self):
        return self._unid

    def _get_puid(self):
        return self._puid

    def _get_channels(self):
        return self._channels

    msgid = property(_get_id)
    time = property(_get_time)
    user = property(_get_msg_user)
    body = property(_get_body)
    room = property(_get_room)
    ip = property(_get_ip)
    font_color = property(_get_font_color)
    font_face = property(_get_font_face)
    font_size = property(_get_font_size)
    raw = property(_get_raw)
    name_color = property(_get_name_color)
    unid = property(_get_unid)
    puid = property(_get_puid)
    uid = property(_get_puid)  # other library use uid so we create an alias
    channels = property(_get_channels)
