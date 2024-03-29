# BroiestBot

![Python](https://img.shields.io/badge/python-^3.8-blue.svg?longCache=true&style=flat-square&colorA=4c566a&colorB=5e81ac&logo=Python&logoColor=white)
![Ch.py](https://img.shields.io/badge/ch.py-1.3.8-blue.svg?longCache=true&style=flat-square&colorA=4c566a&colorB=5e81ac&logo=ChatBot&logoColor=white)
![Requests](https://img.shields.io/badge/Requests-^v2.26.0-red.svg?longCache=true&style=flat-square&colorA=4c566a&colorB=5e81ac&logo=Python&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-^1.4.0-red.svg?longCache=true&style=flat-square&logo=scala&logoColor=white&colorA=4c566a&colorB=bf616a)
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
$ git clone https://github.com/toddbirchard/broiestbot.git
$ cd broiestbot
$ make install
$ make run
``` 


### Configuration

Create a `.env` file with your Chatango configuration. These variables are required:

```
CHATANGO_ROOMS=yourchatangoroom
CHATANGO_USERNAME=yourbotusername
CHATANGO_PASSWORD=yourbotpassword

DATABASE_URI=yourdatabaseuri
DATABASE_NAME=yourdatabasename
DATABASE_TABLE=yourdatabbasetable
```

These variables are optional to enable different services, such as pulling images from Google Cloud or fetching Stock prices:

```env
# Fetching images from Google Storage
GOOGLE_broiestbot_CREDENTIALS=/path/to/credentials.json
GOOGLE_BUCKET_NAME=nameOfStorageBucket

# Fetching .gifs from Giphy
GIPHY_API_KEY=yourGiphyAPIKey

# Stock market & crypto price data
IEX_API_TOKEN=yourIEXStockAPIToken
ALPHA_VANTAGE_API_KEY=yourAlphaVantageKey

# Chart generation
PLOTLY_API_KEY=yourPlotlyApiKey
PLOTLY_USERNAME=yourPlotlyUsername

# Weather by location
WEATHERSTACK_API_KEY=yourWeatherstackApiKey

# Text notifications
TWILIO_SENDER_PHONE=123456789
TWILIO_RECIPIENT_PHONE=123456789
TWILIO_AUTH_TOKEN=yourTwilioToken
TWILIO_ACCOUNT_SID=yourTwilioAccountSid

# All APIs hosted on RapidAPI
RAPID_API_KEY=yourRapidApiKey

# Song Lyrics
GENIUS_KEY_ID=yourLyricsGeniusKey
GENIUS_ACCESS_TOKEN=yourLyricsGeniusToken

# Twitch API
TWITCH_CLIENT_ID=yourTwitchClientId
TWITCH_CLIENT_SECRET=yourTwitchClientSecret
```
