import requests


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
