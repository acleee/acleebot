# acleebot

![python badge](https://img.shields.io/badge/python-3.7-blue.svg?longCache=true&style=flat-square)
![pandas badge](https://img.shields.io/badge/pandas-0.24.0-blue.svg?longCache=true&style=flat-square)
![Chatango badge](https://img.shields.io/badge/platform-Chatango-lightgray.svg?longCache=true&style=flat-square)
![GitHub Last Commit](https://img.shields.io/github/last-commit/google/skia.svg?style=flat-square&colorA=36363e&logo=GitHub)
[![GitHub Issues](https://img.shields.io/github/issues/toddbirchard/acleebot.svg?style=flat-square&colorB=daa000&colorA=36363e&logo=GitHub)](https://github.com/toddbirchard/acleebot/issues)
[![GitHub Stars](https://img.shields.io/github/stars/toddbirchard/acleebot.svg?style=flat-square&colorB=daa000&colorA=36363e&logo=GitHub)](https://github.com/toddbirchard/acleebot/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/toddbirchard/acleebot.svg?style=flat-square&colorB=FCC624&colorA=36363e&logo=GitHub)](https://github.com/toddbirchard/acleebot/network)

The baddest bot in the game right now. Uses the *ch.py* Chatango framework for joining and listening for user messages. If a user's chat is a command (starts with `!`), a function will be fired depending on the type of command.

![acleebot](https://github.com/toddbirchard/acleebot/blob/master/img/acleebot.jpg)

## Commands

Chat commands have 3 properties: 
* **Command name**: Text which triggers a command (ie: !test)
* **Response**: Value returned by a command, either to be sent directly as a chat, or additionally processed depending on command type.
* **Type**: Determines logic associated with a command.

A directory of all commands can be found here: http://broiestbro.com/commands/
