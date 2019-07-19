import requests
from random import randint
from config import giphy_api_key


def random_giphy_image(searchTerm):
    """Get a random image from Giphy."""
    rand = randint(0, 50)
    params = {'api_key': giphy_api_key,
              'q': searchTerm,
              'limit': 1,
              'offset': rand,
              'rating': 'r',
              'lang': 'en'}
    res = requests.get('https://api.giphy.com/v1/gifs/search', params=params)
    if len(res.json()['data']):
        image = res.json()['data'][0]['images']['original']['url']
        return image
    else:
        return 'image not found :('
