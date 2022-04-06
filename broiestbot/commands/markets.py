"""Fetch crypto or stock market data."""
import chart_studio
import requests
from emoji import emojize
from requests.exceptions import HTTPError

from clients import cch, sch
from config import (
    COINMARKETCAP_API_KEY,
    COINMARKETCAP_LATEST_ENDPOINT,
    PLOTLY_API_KEY,
    PLOTLY_USERNAME,
)
from logger import LOGGER

# Plotly
chart_studio.tools.set_credentials_file(username=PLOTLY_USERNAME, api_key=PLOTLY_API_KEY)


def get_crypto_chart(symbol: str) -> str:
    """
    Fetch crypto price and generate 60-day performance chart.

    :param str symbol: Crypto symbol to fetch prices for.

    :returns: str
    """
    try:
        chart = cch.get_chart(symbol)
        return chart
    except HTTPError as e:
        LOGGER.error(
            f"HTTPError {e.response.status_code} while fetching crypto price for `{symbol}`: {e}"
        )
        return emojize(f":warning: omg the internet died AAAAA :warning:", use_aliases=True)
    except Exception as e:
        LOGGER.error(f"Unexpected error while fetching crypto price for `{symbol}`: {e}")
        return emojize(
            f":warning: jfc stop abusing the crypto commands u fgts, you exceeded the API limit :@ :warning:",
            use_aliases=True,
        )


def get_crypto_price(symbol: str, endpoint: str) -> str:
    """
    Fetch crypto price for a given coin symbol.

    :param str symbol: Crypto symbol to fetch price performance for.
    :param str endpoint: Endpoint for the requested crypto.

    :returns: str
    """
    try:
        return cch.get_price(symbol, endpoint)
    except HTTPError as e:
        LOGGER.error(
            f"HTTPError {e.response.status_code} while fetching crypto price for `{symbol}`: {e}"
        )
        return emojize(f":warning: omg the internet died AAAAA :warning:", use_aliases=True)
    except Exception as e:
        LOGGER.error(f"Unexpected error while fetching crypto price for `{symbol}`: {e}")
        return emojize(
            f":warning: jfc stop abusing the crypto commands u fgts, you exceeded the API limit :@ :warning:",
            use_aliases=True,
        )


def get_stock(symbol: str) -> str:
    """
    Fetch stock price and generate 30-day performance chart.

    :param str symbol: Stock symbol to fetch prices for.

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
        return emojize(f":warning: i broke bc im a shitty bot :warning:", use_aliases=True)


def get_top_crypto() -> str:
    """
    Fetch top 10 crypto coin performance.

    :returns: str
    """
    try:
        params = {"start": "1", "limit": "10", "convert": "USD"}
        headers = {
            "Accepts": "application/json",
            "X-CMC_PRO_API_KEY": COINMARKETCAP_API_KEY,
        }
        resp = requests.get(COINMARKETCAP_LATEST_ENDPOINT, params=params, headers=headers)
        if resp.status_code == 200:
            coins = resp.json().get("data")
            return format_top_crypto_response(coins)
    except HTTPError as e:
        LOGGER.warning(f"HTTPError while fetching top coins: {e.response.content}")
        return emojize(
            f":warning: FUCK the bot broke :warning:",
            use_aliases=True,
        )
    except Exception as e:
        LOGGER.warning(f"Unexpected exception while fetching top coins: {e}")
        return emojize(
            f":warning: FUCK the bot broke :warning:",
            use_aliases=True,
        )


def format_top_crypto_response(coins: dict):
    """
    Format a response depicting top-10 coin performance by market cap.

    :params dict coins: Performance of top 10 cryptocurrencies.

    :returns: dict
    """
    try:
        top_coins = "\n\n\n"
        for i, coin in enumerate(coins):
            top_coins += f"<b>{coin['name']} ({coin['symbol']})</b> ${'{:.3f}'.format(coin['quote']['USD']['price'])}\n"
            top_coins += (
                f"1d change of {'{:.2f}'.format(coin['quote']['USD']['percent_change_24h'])}%\n"
            )
            top_coins += (
                f"7d change of {'{:.2f}'.format(coin['quote']['USD']['percent_change_7d'])}%\n"
            )
            if i < len(coins):
                top_coins += "\n"
        return top_coins
    except KeyError as e:
        LOGGER.error(f"KeyError while formatting top cryptocurrencies: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected exception while formatting top cryptocurrencies: {e}")
