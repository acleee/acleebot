"""Create cloud-hosted Candlestick charts of company stock data."""
from datetime import datetime
from typing import Optional

import chart_studio
import chart_studio.plotly as py
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from emoji import emojize
from requests.exceptions import HTTPError

from config import PLOTLY_API_KEY, PLOTLY_USERNAME

# Plotly
chart_studio.tools.set_credentials_file(username=PLOTLY_USERNAME, api_key=PLOTLY_API_KEY)


class CryptoChartHandler:
    """Fetch crypto price performance as summary or chart."""

    def __init__(self, token: str, price_endpoint: str, chart_endpoint: str):
        self.token = token
        self.price_endpoint = price_endpoint
        self.chart_endpoint = chart_endpoint

    def get_coin_price(self, symbol: str, endpoint: str) -> str:
        """
        Get crypto data and generate Plotly chart.

        :param str symbol: Crypto symbol to fetch price performance for.
        :param str endpoint: Endpoint for the requested crypto.

        :returns: str
        """
        """
        Get crypto price for provided ticker label.

        :param str symbol: Crypto symbol to fetch price performance for.
        :param str endpoint: Endpoint for the requested crypto.

        :returns: str
        """
        prices = self._fetch_price_data(symbol, endpoint)
        percentage = prices["change"]["percentage"] * 100
        if prices.get("last") > 1:
            return emojize(
                f"\n\n\n:coin: <b>{symbol.upper()}:</b>\n"
                f':money_bag: CURRENTLY at ${prices["last"]:.2f}\n'
                f':up-right_arrow: HIGH today of ${prices["high"]:.2f}\n'
                f':red_triangle_pointed_down: LOW of ${prices["low"]:.2f}\n'
                f":nine-thirty: (24-hour change of {percentage:.2f}%)",
                language="en",
            )
        elif prices.get("last"):
            return emojize(
                f"\n\n\n:coin: <b>{symbol.upper()}:</b>\n"
                f':money_bag: Currently at ${prices["last"]}\n'
                f':up-right_arrow: HIGH today of ${prices["high"]}\n'
                f':red_triangle_pointed_down: LOW of ${prices["low"]}\n'
                f":nine-thirty: (change of {percentage:.2f}%)",
                language="en",
            )
        return emojize("⚠️ dats nought a COIN u RETART :@ ⚠️", language="en")

    def get_crypto_chart(self, symbol: str) -> str:
        """
        Get crypto data and generate Plotly chart.

        :param str symbol: Crypto symbol to fetch price performance for.

        :returns: Optional[str]
        """
        return self._create_chart(symbol)

    @staticmethod
    def _fetch_price_data(symbol: str, endpoint: str) -> Optional[dict]:
        """
        Get crypto price for a coin symbol.

        :param str symbol: Crypto symbol to fetch price performance for.
        :param str endpoint: Endpoint for the requested crypto.

        :returns: Optional[dict]
        """
        try:
            resp = requests.get(url=endpoint)
            if resp.status_code == 429:
                return emojize(f":warning: jfc you exceeded the crypto API limit :@ :warning:", language="en")
            if resp.status_code == 200:
                return resp.json()["result"]["price"]
        except HTTPError as e:
            raise HTTPError(
                f"HTTPError error {e.response.status_code} while fetching crypto price for `{symbol}`: {e.response.content}"
            )
        except Exception as e:
            raise Exception(f"Unexpected error while crypto price for `{symbol}`: {e}")

    def _get_chart_data(self, symbol: str) -> Optional[dict]:
        """
        Fetch 60-day crypto prices.

        :param str symbol: Symbol for a crypto coin.

        :returns: Optional[dict]
        """
        params = {
            "function": "DIGITAL_CURRENCY_DAILY",
            "symbol": symbol,
            "market": "USD",
            "apikey": self.token,
        }
        try:
            resp = requests.get(self.chart_endpoint, params=params)
            if resp.status_code == 200 and resp.json():
                return resp.json()
        except HTTPError as e:
            raise HTTPError(f"Failed to fetch crypto data for `{symbol}`: {e.response.content}")
        except Exception as e:
            raise Exception(f"Unexpected error while crypto data for `{symbol}`: {e}")

    @staticmethod
    def _parse_chart_data(coin_data: dict) -> Optional[pd.DataFrame]:
        """
        Parse JSON response into Pandas DataFrame.

        :param dict coin_data: Time series data of prices for a given coin.

        :returns: Optional[pd.DataFrame]
        """
        df = pd.DataFrame.from_dict(coin_data["Time Series (Digital Currency Daily)"], orient="index")[:60]
        return df

    def _create_chart(self, symbol: str) -> Optional[str]:
        """
        Create Plotly chart for given crypto symbol.

        :param str symbol: Symbol for a crypto coin.

        :returns: Optional[str]
        """
        try:
            chart_data = self._get_chart_data(symbol)
            if chart_data:
                crypto_df = self._parse_chart_data(chart_data)
                crypto_df = crypto_df.apply(pd.to_numeric)
                fig = go.Figure(
                    data=[
                        go.Candlestick(
                            x=crypto_df.index,
                            open=crypto_df["1a. open (USD)"],
                            high=crypto_df["2a. high (USD)"],
                            low=crypto_df["3a. low (USD)"],
                            close=crypto_df["4a. close (USD)"],
                            decreasing={
                                "line": {"color": "rgb(240, 99, 90)"},
                                "fillcolor": "rgba(142, 53, 47, 0.5)",
                            },
                            increasing={
                                "line": {"color": "rgb(48, 190, 161)"},
                                "fillcolor": "rgba(22, 155, 124, 0.6)",
                            },
                            whiskerwidth=1,
                        )
                    ],
                    layout=go.Layout(
                        font={"size": 15, "family": "Open Sans", "color": "#fff"},
                        title={
                            "x": 0.5,
                            "font": {"size": 23},
                            "text": f"60-day performance of {symbol.upper()}",
                        },
                        xaxis={
                            "type": "date",
                            "rangeslider": {"visible": False},
                            "ticks": "",
                            "gridcolor": "#283442",
                            "linecolor": "#506784",
                            "automargin": True,
                            "zerolinecolor": "#283442",
                            "zerolinewidth": 2,
                        },
                        yaxis={
                            "ticks": "",
                            "gridcolor": "#283442",
                            "linecolor": "#506784",
                            "automargin": True,
                            "zerolinecolor": "#283442",
                            "zerolinewidth": 2,
                        },
                        autosize=True,
                        plot_bgcolor="rgb(23, 27, 31)",
                        paper_bgcolor="rgb(23, 27, 31)",
                    ),
                )
                chart = py.plot(
                    fig,
                    filename=f"{symbol}_{datetime.now()}",
                    sharing="public",
                    auto_open=False,
                )
                # return fig.write_image("figure.png", engine="kaleido")
                return chart.replace("https://plotly.com/", "https://chart-studio.plotly.com/")[:-1] + ".png"
        except HTTPError as e:
            return emojize(f":warning: fk bro's plotly subscription died: {e} :warning:", language="en")
        except Exception as e:
            return emojize(f":warning: idk wot happened: {e} :warning:", language="en")
