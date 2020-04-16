# broiestbot

![Python](https://img.shields.io/badge/python-^3.8-blue.svg?longCache=true&style=flat-square&colorA=4c566a&colorB=5e81ac)
![Pandas](https://img.shields.io/badge/pandas-1.0.3-blue.svg?longCache=true&style=flat-square&colorA=4c566a&colorB=5e81ac)
![Ch.py](https://img.shields.io/badge/ch.py-1.3.8-blue.svg?longCache=true&style=flat-square&colorA=4c566a&colorB=5e81ac)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-1.3.16-red.svg?longCache=true&style=flat-square&logo=scala&logoColor=white&colorA=4c566a&colorB=bf616a)
![PyMySQL](https://img.shields.io/badge/PyMySQL-v0.9.3-red.svg?longCache=true&style=flat-square&logo=mysql&logoColor=white&colorA=4c566a&colorB=bf616a)
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

With [Pipenv](https://pipenv.kennethreitz.org/en/latest/):

```
$ git clone https://github.com/toddbirchard/broiestbot.git
$ cd broiestbot
$ pipenv shell
$ pipenv update
$ python3 main.py
```

With **requirements.txt**:

```
$ git clone https://github.com/toddbirchard/broiestbot.git
$ cd broiestbot
$ python3 -m pip install -r requirements.txt
$ python3 main.py
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

```
GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
GOOGLE_BUCKET_NAME=nameOfStorageBucket
GOOGLE_BUCKET_URL=http://storage.googleapis.com/
GIPHY_API_KEY=yourGiphyAPIKey
IEX_API_TOKEN=yourIEXStockAPIToken
```
