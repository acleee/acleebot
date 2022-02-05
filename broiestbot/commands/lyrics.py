from emoji import emojize

from clients import genius
from logger import LOGGER


def get_song_lyrics(song_title_query: str) -> str:
    """
    Search for song lyrics by song title.

    :param str song_title_query: Song title to fetch lyrics for.

    :returns: str
    """
    try:
        song = genius.search_song(song_title_query)
        if song is not None and song.lyrics is not None:
            lyrics = song.lyrics[:1800].replace("Embed", "")
            return f"{song.full_title} \n\n {lyrics}..."
        return emojize(
            f":warning: wtf kind of song is `{song_title_query}` :warning:", use_aliases=True
        )
    except LookupError as e:
        LOGGER.error(f"LookupError error while searching for song: `{e}`")
        return emojize(
            f":warning: wtf kind of song is `{song_title_query}` :warning:", use_aliases=True
        )
    except Exception as e:
        LOGGER.error(f"Unexpected error while searching for song: `{e}`")
        return emojize(
            f":warning: wtf kind of song is `{song_title_query}` :warning:", use_aliases=True
        )
