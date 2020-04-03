from application.database import Database
from config import (DATABASE_COMMANDS_TABLE,
                    DATABASE_URI,
                    DATABASE_ARGS)
from .cmd import Commands
from .weather import Weather

db = Database(DATABASE_COMMANDS_TABLE, DATABASE_URI, DATABASE_ARGS)
commands = Commands(db.commands)
weather = Weather(db.weather)
