# acleebot

![Python](https://img.shields.io/badge/python-3.7-blue.svg?longCache=true&style=flat-square)
![Pandas](https://img.shields.io/badge/pandas-0.24.0-blue.svg?longCache=true&style=flat-square)
![Ch.py](https://img.shields.io/badge/ch.py-1.3.8-blue.svg?longCache=true&style=flat-square)
![Flask-SQLAlchemy](https://img.shields.io/badge/Flask--SQLAlchemy-2.3.2-red.svg?longCache=true&style=flat-square&logo=scala&logoColor=white&colorA=36363e)
![Psycopg2-binary](https://img.shields.io/badge/Psycopg2--Binary-v2.7.7-red.svg?longCache=true&style=flat-square&logo=PostgreSQL&logoColor=white&colorA=36363e)
![GitHub Last Commit](https://img.shields.io/github/last-commit/google/skia.svg?style=flat-square&colorA=36363e&logo=GitHub)
[![GitHub Issues](https://img.shields.io/github/issues/toddbirchard/acleebot.svg?style=flat-square&colorB=daa000&colorA=36363e&logo=GitHub)](https://github.com/toddbirchard/acleebot/issues)
[![GitHub Stars](https://img.shields.io/github/stars/toddbirchard/acleebot.svg?style=flat-square&colorB=daa000&colorA=36363e&logo=GitHub)](https://github.com/toddbirchard/acleebot/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/toddbirchard/acleebot.svg?style=flat-square&colorB=FCC624&colorA=36363e&logo=GitHub)](https://github.com/toddbirchard/acleebot/network)

The baddest bot in the game right now. Uses the *ch.py* Chatango framework for joining and listening for user messages. If a user's chat is a command (starts with `!`), a function will be fired depending on the type of command.

![acleebot](https://github.com/toddbirchard/acleebot/blob/master/img/acleebot.jpg)

## Commands

A directory of all commands can be found [here](http://broiestbro.com/commands/).

Chat commands have 3 properties: 
* **Command name**: Text which triggers a command (ie: !test)
* **Response**: Value returned by a command, either to be sent directly as a chat, or additionally processed depending on command type.
* **Type**: Determines logic associated with a command.

## Installation

Download the repo and install dependencies:
```
$ git clone https://github.com/toddbirchard/acleebot.git
$ cd acleebot
$ pipenv update
```

Create a `.env` file with your Chatango configuration:
```
ROOM=yourchatangoroom
USERNAME=yourbotusername
PASSWORD=yourbotpassword
SQLALCHEMY_DATABASE_URI=yourdatabaseuri
SQLALCHEMY_DATABASE_NAME=yourdatabasename
SQLALCHEMY_TABLE=yourdatabbasetable
SQLALCHEMY_DB_SCHEMA=yourpostgresschema
```

Run the script:
```
$ pipenv shell
$ python3 main.py
```
