# BroiestBot

![Python](https://img.shields.io/badge/python-^3.8-blue.svg?longCache=true&style=flat-square&colorA=4c566a&colorB=5e81ac&logo=Python&logoColor=white)
![Ch.py](https://img.shields.io/badge/ch.py-1.3.8-blue.svg?longCache=true&style=flat-square&colorA=4c566a&colorB=5e81ac&logo=ChatBot&logoColor=white)
![Requests](https://img.shields.io/badge/Requests-^v2.28.1-red.svg?longCache=true&style=flat-square&colorA=4c566a&colorB=5e81ac&logo=Python&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-^1.4.45-red.svg?longCache=true&style=flat-square&logo=scala&logoColor=white&colorA=4c566a&colorB=bf616a)
![GitHub Last Commit](https://img.shields.io/github/last-commit/google/skia.svg?style=flat-square&colorA=4c566a&logo=GitHub&colorB=a3be8c)
[![GitHub Issues](https://img.shields.io/github/issues/toddbirchard/broiestbot.svg?style=flat-square&colorA=4c566a&logo=GitHub&colorB=ebcb8b)](https://github.com/toddbirchard/broiestbot/issues)
[![GitHub Stars](https://img.shields.io/github/stars/toddbirchard/broiestbot.svg?style=flat-square&colorA=4c566a&logo=GitHub&colorB=ebcb8b)](https://github.com/toddbirchard/broiestbot/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/toddbirchard/broiestbot.svg?style=flat-square&colorA=4c566a&logo=GitHub&colorB=ebcb8b)](https://github.com/toddbirchard/broiestbot/network)

The baddest bot in the game right now. Uses the *ch.py* framework for joining [Chantango](https://www.chatango.com/) rooms and responding to user messages.

## Commands

If a user's chat is a command (starts with `!`), a function will be fired depending on the type of command. A directory of all commands can be found [here](http://broiestbro.com/table/commands).

Chat commands have 3 properties:

* **Command name**: Text which triggers a command (ie: !test)
* **Response**: Value returned by a command, either to be sent directly as a chat, or additionally processed depending on command type.
* **Type**: Determines logic associated with a command.

## Getting Started

### Installation

Get up and running with `make deploy`:

```shell
git clone https://github.com/toddbirchard/broiestbot.git
cd broiestbot
make install
make run
```

### Configuration

Create a `.env` file with your Chatango configuration. These variables are required:

```env
ENVIRONMENT=production

CHATANGO_ROOM_1=yourChatangoRoom1
CHATANGO_ROOM_2=yourChatangoRoom2
CHATANGO_ROOM_3=yourChatangoRoom3
CHATANGO_USERNAME=yourChatangoBotUsername
CHATANGO_PASSWORD=yourChatangoBotPassword


DATABASE_URI=yourSqlDatabaseUri
DATABASE_COMMANDS_TABLE=yourSqlCommandsTable
DATABASE_WEATHER_TABLE=yourSqlWeatherTable
DATABASE_USERS_TABLE=yourSqlUsersTable
```

These variables are optional to enable different services, such as pulling images from Google Cloud or fetching Stock prices:

```env
# Fetching giphy .gifs
GIPHY_API_KEY=yourGiphyApiKey

# Fetching images from Google Cloud Storage
GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
GOOGLE_BUCKET_NAME=nameOfGcsBucket

# Third party API keys/tokens
IEX_API_TOKEN=yourIexApiToken
ALPHA_VANTAGE_API_KEY=yourAlphaVantageApiKey
IP_DATA_KEY=yourIpDataKey
WEATHERSTACK_API_KEY=yourWeatherstackApiKey
RAPID_API_KEY=yourRapidApiKey
NBA_API_KEY=yourApiBasketballKey

# Chart generation
PLOTLY_API_KEY=yourPlotlyApiKey
PLOTLY_USERNAME=yourPlotlyUsername

# Text notifications
TWILIO_SENDER_PHONE=123456789
TWILIO_RECIPIENT_PHONE=123456789
TWILIO_AUTH_TOKEN=yourTwilioToken
TWILIO_ACCOUNT_SID=yourTwilioAccountSid

# Song Lyrics
GENIUS_KEY_ID=yourLyricsGeniusKey
GENIUS_ACCESS_TOKEN=yourLyricsGeniusToken

# Twitch API
TWITCH_CLIENT_ID=yourTwitchClientId
TWITCH_CLIENT_SECRET=yourTwitchClientSecret

TWITCH_USER_1_USERNAME=yourTwitchUsername1
TWITCH_USER_1_ID=yourTwitchUserId1
TWITCH_USER_2_USERNAME=yourTwitchUsername2
TWITCH_USER_2_ID=yourTwitchUserId2

# Redis Cache
REDIS_HOST=yourRedisHost
REDIS_USERNAME=yourRedisUsername
REDIS_PASSWORD=yourRedisPassword
REDIS_PORT=yourRedisPort
REDIS_DB=yourRedisDb

# API Basketball
NBA_API_KEY=yourNbaKey
```
