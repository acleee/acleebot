from google.cloud import storage
from random import randint
from config import Config


def fetch_image_from_storage(message):
    """Get a random image from Google Cloud Storage bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(Config.gcloudBucketName)
    images = bucket.list_blobs(prefix=message, delimiter='minions/')
    imageList = [image.name for image in images if '.' in image.name]
    rand = randint(0, len(imageList) - 1)
    image = Config.gcloudBucketUrl + Config.gcloudBucketName + '/' + imageList[rand]
    return image
