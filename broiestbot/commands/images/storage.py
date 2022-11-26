"""Fetch randomly selected meme image(s) from storage bucket."""
from random import randint

from emoji import emojize
from google.cloud.exceptions import GoogleCloudError, NotFound

from clients import gcs
from config import GOOGLE_BUCKET_NAME, GOOGLE_BUCKET_URL
from logger import LOGGER


def fetch_image_from_gcs(subdirectory: str) -> str:
    """
    Get image from Google Cloud Storage bucket.

    :param str subdirectory: Bucket directory to fetch random image from.

    :returns: str
    """
    try:
        images = gcs.bucket.list_blobs(prefix=subdirectory)
        image_list = [image.name for image in images if "." in image.name]
        rand = randint(0, len(image_list) - 1)
        image = f"{GOOGLE_BUCKET_URL}{GOOGLE_BUCKET_NAME}/{image_list[rand]}"
        return image.lower()
    except NotFound as e:
        LOGGER.warning(f"GCS `NotFound` error when fetching image for `{subdirectory}`: {e}")
        return emojize(f":warning: omfg bot just broke wtf did u do :warning:", language="en")
    except GoogleCloudError as e:
        LOGGER.warning(
            f"GCS `GoogleCloudError` error when fetching image for `{subdirectory}`: {e}"
        )
        return emojize(f":warning: omfg bot just broke wtf did u do :warning:", language="en")
    except ValueError as e:
        LOGGER.warning(f"ValueError when fetching random GCS image for `{subdirectory}`: {e}")
        return emojize(f":warning: omfg bot just broke wtf did u do :warning:", language="en")
    except Exception as e:
        LOGGER.warning(f"Unexpected error when fetching random GCS image for `{subdirectory}`: {e}")
        return emojize(f":warning: o shit i broke im a trash bot :warning:", language="en")


def gcs_random_image_spam(subdirectory: str) -> str:
    """
    Get randomized image from Google Cloud Storage bucket; post 3 times.

    :param str subdirectory: Bucket directory to fetch random image from.

    :returns: str
    """
    try:
        response = []
        images = gcs.bucket.list_blobs(prefix=subdirectory)
        image_list = [image.name for image in images if "." in image.name]
        for i in range(3):
            response.append(
                f"{GOOGLE_BUCKET_URL}{GOOGLE_BUCKET_NAME}/{image_list[randint(0, len(image_list) - 1)]}"
            )
        return " ".join(response)
    except GoogleCloudError as e:
        LOGGER.warning(
            f"GCS `GoogleCloudError` error when fetching image for `{subdirectory}`: {e}"
        )
        return emojize(f":warning: omfg bot just broke wtf did u do :warning:", language="en")
    except ValueError as e:
        LOGGER.warning(f"ValueError when fetching random GCS image for `{subdirectory}`: {e}")
        return emojize(f":warning: omfg bot just broke wtf did u do :warning:", language="en")
    except Exception as e:
        LOGGER.warning(f"Unexpected error when fetching random GCS image for `{subdirectory}`: {e}")
        return emojize(f":warning: o shit i broke im a trash bot :warning:", language="en")


def gcs_count_images_in_bucket(subdirectory: str) -> str:
    """
    Get randomized image from Google Cloud Storage bucket; post 3 times.

    :param str subdirectory: Bucket directory from which to return total image count.

    :returns: str
    """
    try:
        response = "\n\n\n"
        images = gcs.bucket.list_blobs(prefix=subdirectory)
        image_list = [image.name for image in images if "." in image.name]
        if len(image_list) > 0:
            response += f"<b>{subdirectory.upper()} image count:</b>\n"
            response += f":keycap_#: {len(image_list)}"
            return emojize(response, language="en")
        return emojize(
            f":warning: uhhh I couldnt find any images for {subdirectory.upper()} :warning:",
            language="en",
        )
    except GoogleCloudError as e:
        LOGGER.warning(
            f"GCS `GoogleCloudError` error when fetching image for `{subdirectory}`: {e}"
        )
        return emojize(f":warning: omfg bot just broke wtf did u do :warning:", language="en")
    except ValueError as e:
        LOGGER.warning(f"ValueError when fetching random GCS image for `{subdirectory}`: {e}")
        return emojize(f":warning: omfg bot just broke wtf did u do :warning:", language="en")
    except Exception as e:
        LOGGER.warning(f"Unexpected error when fetching random GCS image for `{subdirectory}`: {e}")
        return emojize(f":warning: o shit i broke im a trash bot :warning:", language="en")
