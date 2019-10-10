import requests
from bs4 import BeautifulSoup
from random import randint


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
    images = [img.get('src') for img in images if 'redditstatic' not in img]
    rand = 0
    for x in range(10):
        rand = randint(1, len(images))
    if images:
        return link.find_all("img")[rand].get('src')
    return 'No luck bro'
