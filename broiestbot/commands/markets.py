"""Fetch crypto or stock market data."""
import chart_studio
from emoji import emojize
from requests.exceptions import HTTPError

from clients import cch, sch
from config import PLOTLY_API_KEY, PLOTLY_USERNAME
from logger import LOGGER

# Plotly
chart_studio.tools.set_credentials_file(
    username=PLOTLY_USERNAME, api_key=PLOTLY_API_KEY
)


def get_crypto(symbol: str) -> str:
    """
    Fetch crypto price and generate 60-day performance chart.

    :param symbol: Crypto symbol to fetch prices for.
    :type symbol: str
    :returns: str
    """
    try:
        chart = cch.get_chart(symbol)
        return chart
    except HTTPError as e:
        LOGGER.error(f"HTTPError while fetching crypto price for `{symbol}`: {e}")
        return emojize(
            f":warning: omg the internet died AAAAA :warning:", use_aliases=True
        )
    except Exception as e:
        LOGGER.error(
            f"Unexpected error while fetching crypto price for `{symbol}`: {e}"
        )
        return emojize(
            f":warning: yea nah idk wtf ur searching for :warning:", use_aliases=True
        )


def get_stock(symbol: str) -> str:
    """
    Fetch stock price and generate 30-day performance chart.

    :param symbol: Stock symbol to fetch prices for.
    :type symbol: str
    :returns: str
    """
    try:
        chart = sch.get_chart(symbol)
        return chart
    except HTTPError as e:
        LOGGER.error(f"HTTPError while fetching stock price for `{symbol}`: {e}")
        return emojize(
            f":warning: ough nough da site i get stocks from died :warning:",
            use_aliases=True,
        )
    except Exception as e:
        LOGGER.error(f"Unexpected error while fetching stock price for `{symbol}`: {e}")
        return emojize(
            f":warning: i broke bc im a shitty bot :warning:", use_aliases=True
        )
