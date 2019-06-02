from random import randint


def randomize_image(message):
    """Select a random image."""
    list = message.replace(' ', '').split(';')
    random_pic = list[randint(0, len(list)-1)]
    return random_pic
