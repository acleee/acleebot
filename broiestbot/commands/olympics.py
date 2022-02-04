"""2020/2022 Olympics medal leaders"""
import pandas as pd
from emoji import emojize

from config import OLYMPICS_LEADERBOARD_ENDPOINT, WINTER_OLYMPICS_LEADERBOARD_ENDPOINT
from logger import LOGGER


def get_olympic_medals_per_nation() -> str:
    """
    Return olympic leaders by number of gold medals.

    :returns: str
    """
    try:
        medals_df = pd.read_html(
            OLYMPICS_LEADERBOARD_ENDPOINT,
            flavor="bs4",
            attrs={"class": "medals olympics has-team-logos"},
            header=0,
            index_col=None,
        )
        medals_df = medals_df[0].head(10)
        medals_df.rename(
            columns={
                "Group": "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;",
                "G": f"{emojize(':1st_place_medal:', use_aliases=True)}&nbsp;",
                "S": f"{emojize(':2nd_place_medal:', use_aliases=True)}&nbsp;",
                "B": f"{emojize(':3rd_place_medal:', use_aliases=True)}&nbsp;",
            },
            inplace=True,
        )
        return (
            f"\n\n{medals_df.to_string(header=True, index=False, col_space=10, justify='center')}"
        )
    except Exception as e:
        LOGGER.error(f"Exception occurred while fetching olympics leaderboard: {e}")
        return emojize(":warning: lmao nobody has won anything yet retart :warning:")


def get_winter_olympic_medals_per_nation() -> str:
    """
    Return winter olympic leaders by number of gold medals.

    :returns: str
    """
    try:
        medals_df = pd.read_html(
            WINTER_OLYMPICS_LEADERBOARD_ENDPOINT,
            flavor="bs4",
            attrs={"class": "medals olympics has-team-logos"},
            header=0,
            index_col=None,
        )
        medals_df = medals_df[0].head(10)
        medals_df.rename(
            columns={
                "Group": "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;",
                "G": f"{emojize(':1st_place_medal:', use_aliases=True)}&nbsp;",
                "S": f"{emojize(':2nd_place_medal:', use_aliases=True)}&nbsp;",
                "B": f"{emojize(':3rd_place_medal:', use_aliases=True)}&nbsp;",
            },
            inplace=True,
        )
        return (
            f"\n\n{medals_df.to_string(header=True, index=False, col_space=10, justify='center')}"
        )
    except Exception as e:
        LOGGER.error(f"Exception occurred while fetching winter olympics leaderboard: {e}")
        return emojize(":warning: lmao nobody has won anything yet retart :warning:")


def format_country_name(value: str):
    return f"{value}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
