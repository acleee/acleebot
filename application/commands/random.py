from random import randint


def randomize_image(message):
    """Select a random image."""
    image_list = message.replace(' ', '').split(';')
    random_pic = image_list[randint(0, len(list)-1)]
    return random_pic
