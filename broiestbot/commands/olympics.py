"""2020 Olympics medal leaders"""
import pandas as pd
from emoji import emojize


def get_olympic_medals_per_nation() -> str:
    """Return olympic leaders by number of gold medals"""
    medals_df = pd.read_html(
        "https://www.espn.com/olympics/summer/2020/medals/_/view/overall/sort/gold",
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
    return f"\n\n{medals_df.to_string(header=True, index=False, col_space=10, justify='center')}"


def format_country_name(value: str):
    return f"{value}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
