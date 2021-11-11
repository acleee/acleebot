"""Bot application entry point."""
from broiestbot import start_bot_development_mode, start_bot_production_mode
from config import ENVIRONMENT

if __name__ == "__main__":
    if ENVIRONMENT == "development":
        start_bot_development_mode()
    else:
        start_bot_production_mode()
