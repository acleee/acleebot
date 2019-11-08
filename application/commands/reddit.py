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
    r = requests.get(endpoint, headers=headers)
    res = r.json()['data']['children']
    images = [image['preview']['images'][0]['source']['url'] for image in res if image.get('preview', None)]
    rand = randint(0, len(images) - 1)
    image = images[rand].split('?')[0]
    return image
