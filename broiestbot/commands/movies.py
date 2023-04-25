"""Lookup movie information via IMDB API."""
from typing import Optional

from emoji import emojize
from imdb import IMDbError
from imdb.Movie import Movie

from clients import ia
from logger import LOGGER


def find_imdb_movie(movie_title: str) -> str:
    """
    Get movie summary, rating, actors, poster, & box office info from IMDB.

    :param str movie_title: Movie to fetch IMDB info & box office info for.

    :returns: str
    """
    try:
        movies = ia.search_movie(movie_title)
        if bool(movies):
            movie_id = movies[0].getID()
            movie = ia.get_movie(movie_id)
            if movie:
                title = f"<b>{movie.data.get('title').upper()}</b>"
                cast = movie.data.get("cast")
                director = movie.data.get("director")
                year = movie.data.get("year")
                genres = movie.data.get("genres")
                rating = movie.data.get("rating")
                art = movie.data.get("cover url")
                box_office = get_box_office_data(movie)
                synopsis = movie.data.get("synopsis")
                if title and year:
                    title = f"{title} ({year})"
                if rating:
                    rating = f":star: {movie.data.get('rating')}/10"
                if cast:
                    cast = f":people_hugging: STARRING {', '.join([actor['name'] for actor in movie.data['cast'][:2]])}"
                if director:
                    director = f":clapper_board: DIRECTED by {movie.data.get('director')[0].get('name')}"
                if genres:
                    genres = f":movie_camera: {', '.join(movie.data.get('genres'))}"
                if box_office:
                    box_office = f":money_bag: {box_office}"
                if synopsis:
                    synopsis = synopsis[0]
                    synopsis = " ".join(synopsis.split(". ")[:2])
                    synopsis = f":speech_balloon: {synopsis}"
                response = "\n".join(
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
                return emojize(f"\n\n\n{response}", language="en")
            LOGGER.warning(f"No IMDB info found for `{movie_title}`.")
            return emojize(f":warning: wtf kind of movie is {movie} :warning:", language="en")
    except IMDbError as e:
        LOGGER.warning(f"IMDB failed to find `{movie_title}`: {e}")
        return emojize(f":warning: wtf kind of movie is {movie_title} :warning:", language="en")
    except Exception as e:
        LOGGER.error(f"Unexpected error while fetching IMDB movie `{movie_title}`: {e}")
        return emojize(f":warning: omfg u broke me with ur shit movie :warning:", language="en")


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
