# acleebot

![Python](https://img.shields.io/badge/python-3.7-blue.svg?longCache=true&style=flat-square&colorA=4c566a&colorB=5e81ac)
![Pandas](https://img.shields.io/badge/pandas-0.24.0-blue.svg?longCache=true&style=flat-square&colorA=4c566a&colorB=5e81ac)
![Ch.py](https://img.shields.io/badge/ch.py-1.3.8-blue.svg?longCache=true&style=flat-square&colorA=4c566a&colorB=5e81ac)
![Flask-SQLAlchemy](https://img.shields.io/badge/Flask--SQLAlchemy-2.3.2-red.svg?longCache=true&style=flat-square&logo=scala&logoColor=white&colorA=4c566a&colorB=bf616a)
![PyMySQL](https://img.shields.io/badge/PyMySQL-v0.9.3-red.svg?longCache=true&style=flat-square&logo=mysql&logoColor=white&colorA=4c566a&colorB=bf616a)
![GitHub Last Commit](https://img.shields.io/github/last-commit/google/skia.svg?style=flat-square&colorA=4c566a&logo=GitHub&colorB=a3be8c)
[![GitHub Issues](https://img.shields.io/github/issues/toddbirchard/acleebot.svg?style=flat-square&colorA=4c566a&logo=GitHub&colorB=ebcb8b)](https://github.com/toddbirchard/acleebot/issues)
[![GitHub Stars](https://img.shields.io/github/stars/toddbirchard/acleebot.svg?style=flat-square&colorA=4c566a&logo=GitHub&colorB=ebcb8b)](https://github.com/toddbirchard/acleebot/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/toddbirchard/acleebot.svg?style=flat-square&colorA=4c566a&logo=GitHub&colorB=ebcb8b)](https://github.com/toddbirchard/acleebot/network)

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
```

Run the script:
```
$ pipenv shell
$ python3 main.py
```
