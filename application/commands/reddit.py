from random import randint
import requests


def random_subreddit_image(message):
    """Fetch a random image from latest posts in a subreddit."""
    headers = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET',
      'Access-Control-Allow-Headers': 'Content-Type',
      'Access-Control-Max-Age': '3600',
      'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }
    endpoint = message + 'new.json?sort=new'
    print('endpoint = ', endpoint)
    res = requests.get(endpoint, headers=headers).json()
    images = [image['data']['preview']['images'][0]['source']['url'] for image in res['data']['children']]
    rand = randint(0, len(images) - 1)
    image = images[rand]
    return image
