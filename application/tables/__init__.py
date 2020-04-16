from application.database import Database
from config import (DATABASE_COMMANDS_TABLE,
                    DATABASE_WEATHER_TABLE,
                    DATABASE_URI,
                    DATABASE_ARGS,
                    )
from .cmd import Commands
from .weather import Weather

db = Database(DATABASE_URI, DATABASE_ARGS)
commands = Commands(db.get_table(DATABASE_COMMANDS_TABLE, 'command'))
weather = Weather(db.get_table(DATABASE_WEATHER_TABLE, 'code'))
