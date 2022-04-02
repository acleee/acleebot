"""2020/2022 Olympics medal leaders"""
import pandas as pd
from emoji import emojize
from pandas import Series

from config import OLYMPICS_LEADERBOARD_ENDPOINT, WINTER_OLYMPICS_LEADERBOARD_ENDPOINT
from logger import LOGGER


def get_summer_olympic_medals() -> str:
    """
    Summer Olympics country leaders, by number of gold medals.

    :returns: str
    """
    return get_medals_by_nation(OLYMPICS_LEADERBOARD_ENDPOINT)


def get_winter_olympic_medals() -> str:
    """
    Winter Olympics country leaders, by number of gold medals.

    :returns: str
    """
    return get_medals_by_nation(WINTER_OLYMPICS_LEADERBOARD_ENDPOINT)


def get_medals_by_nation(endpoint: str) -> str:
    """
    Fetch olympic medal leaders and format leaderboard.

    :param str endpoint: URL containing olympic medal leaders to scrape.

    :returns: str
    """
    try:
        medals_df = pd.read_html(
            endpoint,
            flavor="bs4",
            attrs={"class": "medals olympics has-team-logos"},
            header=0,
            index_col=None,
        )
        medals_df = medals_df[0].head(10)
        medals_df.rename(
            columns={
                "Group": "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;",
                "G": f"{emojize(':1st_place_medal:', language='en')}",
                "S": f"{emojize(':2nd_place_medal:', language='en')}",
                "B": f"{emojize(':3rd_place_medal:', language='en')}",
            },
            inplace=True,
        )
        medals_df = medals_df.apply(add_nation_flag_emojis, axis=1)
        return (
            f"\n\n{medals_df.to_string(header=True, index=False, col_space=10, justify='center')}"
        )
    except Exception as e:
        LOGGER.error(f"Exception occurred while fetching winter olympics leaderboard: {e}")
        return emojize(":warning: lmao nobody has won anything yet retart :warning:")


def add_nation_flag_emojis(row: Series):
    """
    Add flag emojis to Olympic leaders.

    :param Series row: Row containing number of medals per nation.

    :returns: Series
    """
    row[0] = emojize(
        row[0]
        .replace("NOR", ":flag_for_Norway: NOR")
        .replace("USA", ":flag_for_United_States: USA")
        .replace("NED", ":flag_for_Netherlands: NED")
        .replace("GER", ":flag_for_Germany: GER")
        .replace("SWE", ":flag_for_Sweden: SWE")
        .replace("AUT", ":flag_for_Austria: AUT&nbsp;")
        .replace("CHN", ":flag_for_China: CHN")
        .replace("ROC", ":flag_for_Russia: ROC")
        .replace("ITA", ":flag_for_Italy: ITA&nbsp;&nbsp;")
        .replace("SUI", ":flag_for_Switzerland: SUI&nbsp;&nbsp;")
        .replace("CAN", ":flag_for_Canada: CAN")
        .replace("FRA", ":flag_for_France: FRA")
        .replace("KOR", ":flag_for_South_Korea: KOR")
        .replace("AUS", ":flag_for_Australia: AUS")
        .replace("FIN", ":flag_for_Finland: FIN")
        .replace("SLO", ":flag_for_Slovenia: SLO")
        .replace("FIN", ":flag_for_Finland: FIN")
        .replace("CZE", ":flag_for_Czech_Republic: CZE")
        .replace("POL", ":flag_for_Poland: POL")
        .replace("NZL", ":flag_for_New_Zealand: NZL")
        .replace("JPN", ":flag_for_Japan: JPN"),
        language="en",
    )
    row[0] = f"{row[0]}&nbsp;&nbsp;"
    row[4] = f"<strong>{row[4]}</strong>"
    return row


def format_country_name(value: str):
    return f"{value}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
