"""Lookup movie information via IMDB API."""
from typing import Optional

from emoji import emojize
from imdb import IMDbError
from imdb.Movie import Movie

from clients import ia
from logger import LOGGER


def find_imdb_movie(movie_title: str) -> Optional[str]:
    """
    Get movie summary, rating, actors, poster, & box office info from IMDB.

    :param str movie_title: Movie to fetch IMDB info & box office info for.

    :returns: Optional[str]
    """
    try:
        movies = ia.search_movie(movie_title)
        if bool(movies):
            movie_id = movies[0].getID()
            movie = ia.get_movie(movie_id)
            if movie:
                cast = movie.data.get("cast")
                art = movie.data.get("cover url", None)
                director = movie.data.get("director")
                year = movie.data.get("year")
                genres = f"({', '.join(movie.data.get('genres'))}, {year})."
                title = f"{movie.data.get('title').upper()},"
                rating = f"{movie.data.get('rating')}/10"
                box_office = get_box_office_data(movie)
                synopsis = movie.data.get("synopsis")
                if cast:
                    cast = f"STARRING {', '.join([actor['name'] for actor in movie.data['cast'][:2]])}."
                if director:
                    director = f"DIRECTED by {movie.data.get('director')[0].get('name')}."
                if synopsis:
                    try:
                        synopsis = synopsis[0]
                        synopsis = " ".join(synopsis[0].split(". ")[:2])
                    except KeyError as e:
                        LOGGER.error(f"IMDB movie `{title}` does not have a synopsis: {e}")
                response = " ".join(
                    filter(
                        None,
                        [
                            title,
                            rating,
                            genres,
                            cast,
                            director,
                            synopsis,
                            box_office,
                            art,
                        ],
                    )
                )
                return response
            LOGGER.warning(f"No IMDB info found for `{movie_title}`.")
            return emojize(f":warning: wtf kind of movie is {movie} :warning:", use_aliases=True)
    except IMDbError as e:
        LOGGER.warning(f"IMDB failed to find `{movie_title}`: {e}")
        return emojize(f":warning: wtf kind of movie is {movie_title} :warning:", use_aliases=True)
    except Exception as e:
        LOGGER.error(f"Unexpected error while fetching IMDB movie `{movie_title}`: {e}")
        return emojize(f":warning: omfg u broke me with ur shit movie :warning:", use_aliases=True)


def get_box_office_data(movie: Movie) -> Optional[str]:
    """
    Get IMDB box office performance for a given film.

    :param Movie movie: IMDB movie object.

    :returns: Optional[str]
    """
    try:
        response = []
        if movie.data.get("box office", None):
            budget = movie.data["box office"].get("Budget", None)
            opening_week = movie.data["box office"].get("Opening Weekend United States", None)
            gross = movie.data["box office"].get("Cumulative Worldwide Gross", None)
            if budget:
                response.append(f"BUDGET {budget}.")
            if opening_week:
                response.append(f"OPENING WEEK {opening_week}.")
            if gross:
                response.append(f"CUMULATIVE WORLDWIDE GROSS {gross}.")
            return " ".join(response)
        LOGGER.warning(f"No IMDB box office info found for `{movie}`.")
    except KeyError as e:
        LOGGER.warning(f"KeyError when fetching box office info for `{movie}`: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when fetching box office info for `{movie}`: {e}")
