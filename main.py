"""Entrypoint for app."""
# Core imports
import sys
import urllib.request as urlreq
# Ch.py Chatango Framework
from bot import ch
# Import directoryt of commands
from bot import db
# Import commands
from bot import commands
# Import config
from config import username
from config import password
from config import testRoom
from config import acleeRoom



class bot(ch.RoomManager):
    """Main bot class."""

    def onInit(self):
        """Initialize bot."""
        self.setNameColor("000000")
        self.setFontColor("000000")
        self.setFontFace("Arial")
        self.setFontSize(11)

    def chat(self, row, room):
        """Construct a response to a valid command."""
        type = row['type']
        message = row['content']
        print('type', type)
        response = 'under development tbh'
        print('type = ', type)
        if (type == 'basic'):
            response = commands.send_basic_message(message)
        if (type == 'crypto'):
            response = commands.get_crypto_price(message)
        if (type == 'nba score'):
            response = commands.get_nba_score(message)
        if (type == 'goal'):
            print('goal command')
        if (type == 'custom'):
            print('custom command')
        room.message(response)

    def onMessage(self, room, user, message):
        """Boilerplate function trigger on message."""
        print("[{0}] {1}: {2}".format(room.name,
                                      user.name.title(),
                                      message.body))

        cmd = message.body.replace(" ", '')
        print('cmd = ', cmd)
        # Trigger if chat message is a command
        if cmd[0] == "!":
            cmd = cmd[1:].lower()
            print('THIS IS A COMMAND = ', cmd)
            response = db.cm(cmd)
            print('response = ', response)
            self.chat(response, room)
            print("TESTING")
        else:
            # Add special commands here
            fullmsg = cmd


if __name__ == "__main__":
    bot.easy_start([testRoom, acleeRoom],
                   username,
                   password)
    command_df = get_commands_from_database()
