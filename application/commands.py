"""Basic plaintext responses."""
import requests
from random import randint
from bs4 import BeautifulSoup
import random


def send_basic_message(message):
    """Send basic text message to room."""
    print('BASIC')
    msg = message
    print(msg)
    return message


def get_crypto_price(message):
    """Get crypto price for provided ticker label."""
    req = requests.get(url=message)
    x = req.json()
    y = x["result"]["price"]
    z = y["change"]
    last = str(y["last"])
    high = str(y["high"])
    low = str(y["low"])
    percentage = z["percentage"]*100
    msg = "Currently at $" + last \
        + ", high today of $" + high \
        + ", low of $" + low \
        + ", change of %.3f" % percentage + "%"
    return msg


def get_nba_score(message):
    """Get score of an NBA game."""
    if (message == "sixers" or message == "76ers"):
        team_id = '1610612755'
        if not team_id:
            return "Couldn't find the score for todays game"
        url = 'https://data.nba.com/data/5s/v2015/json/mobile_teams/nba/2017/scores/00_todays_scores.json'
        json = requests.get(url).json()
        games = json['gs']['g']
        for game in games:
            home_team_id = game['h']['tid']
            visitor_team_id = game['v']['tid']
            if home_team_id == int(team_id) or visitor_team_id == int(team_id):
                home_team_score = game['h']['s']
                visitor_team_score = game['v']['s']
                home_team_name = game['h']['tc'] + " " + game['h']['tn']
                visitor_team_name = game['v']['tc'] + " " + game['v']['tn']
                msg = home_team_name + " " + str(home_team_score) + " - " \
                    + visitor_team_name + " " \
                    + str(visitor_team_score)
                return msg


def get_hockey_goals(message):
    """Get hockey goals per player."""
    pass


def get_user_avatar(message, args):
    """Retrieve avatar for provided user."""
    name = str(args.lower())
    msg = "http://fp.chatango.com/profileimg/" \
        + name[0] + "/" \
        + name[1] + "/" \
        + name + "/full.jpg"
    return msg


def randomize_image(message):
    """Select a random image."""
    list = message.replace(' ', '').split(';')
    random_pic = list[randint(0, len(list)-1)]
    return random_pic


def say_wew():
    """Say 'wew' in chat."""
    return 'wew'


def say_lmao():
    """Reply with 'lmao' whenever a user says 'ayyy'."""
    return 'lmao'


def scrape_random_image(url):
    """Attempt to get image."""
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }
    r = requests.get(url, headers=headers)
    link = BeautifulSoup(r.content, 'html.parser')
    images = link.find_all("img")
    images = [img.get('src') for img in images if not 'redditstatic' in img]
    rand = 0
    for x in range(10):
        rand = random.randint(1, len(images))
    if images:
        return link.find_all("img")[rand].get('src')
