from google.cloud import storage
from random import randint
from os import environ


def fetch_image_from_storage(message):
    """Get a random image from Google Cloud Storage bucket."""
    storage_client = storage.Client()
    bucketName = environ.get('GOOGLE_BUCKET_NAME')
    bucket = storage_client.get_bucket(bucketName)
    images = bucket.list_blobs()
    # rand = randint(0, len(images))

    for image in images:
        print(image.name)
