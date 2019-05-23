"""Entrypoint for app."""
# Ch.py Chatango Framework
from bot import ch
# Import directoryt of commands
from bot import db
# Import commands
from bot import commands
# Import config
from config import username, password, testRoom, blabroom, acleeRoom


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
        response = 'under development tbh'
        if (type == 'basic'):
            response = commands.send_basic_message(message)
        if (type == 'scrape'):
            response = commands.scrape_random_image(message)
        if (type == 'crypto'):
            response = commands.get_crypto_price(message)
        if (type == 'random'):
            response = commands.randomize_image(message)
        if (type == 'nba score'):
            response = commands.get_nba_score(message)
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
        # Trigger if chat message is a command
        try:
            if cmd[0] == "!":
                cmd = cmd[1::].lower()
                response = db.cm(cmd)
                self.chat(response, room)
        except KeyError:
            pass


if __name__ == "__main__":
    bot.easy_start([testRoom, acleeRoom, blabroom],
                   username,
                   password)
