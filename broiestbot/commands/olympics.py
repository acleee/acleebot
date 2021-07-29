""""""
import pandas as pd
from emoji import emojize


def get_olympic_medals_per_nation() -> str:
    medals_df = pd.read_html(
        "https://www.espn.com/olympics/summer/2020/medals",
        flavor="bs4",
        attrs={"class": "medals olympics has-team-logos"},
        header=0,
    )
    medals_df = medals_df[0].head(10)
    medals_df.rename(
        columns={
            "G": f"{emojize(':1st_place_medal:', use_aliases=True)}",
            "S": f"{emojize(':2nd_place_medal:', use_aliases=True)}",
            "B": f"{emojize(':3rd_place_medal:', use_aliases=True)}",
        },
        inplace=True,
    )
    return f"\n\n{medals_df.to_string(index=False, col_space=10, header=True, justify='center')}"
