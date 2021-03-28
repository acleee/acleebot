from clients import genius
from logger import LOGGER


def get_song_lyrics(song_title_query: str) -> str:
    """
    Search for song lyrics by song title.

    :param song_title_query: Song title to fetch lyrics for.
    :type song_title_query: str
    :returns: str
    """
    try:
        song = genius.search_song(song_title_query)
        if song is not None and song.lyrics is not None:
            lyrics = f"{song.full_title} \n\n {song.lyrics[0:600]}..."
            return lyrics
        return f"wtf kind of song is `{song_title_query}`"
    except Exception as e:
        LOGGER.error(f"Unexpected error while searching for song: `{e}`")
