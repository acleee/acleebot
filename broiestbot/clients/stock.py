"""Create cloud-hosted Candlestick charts of company stock data."""
from typing import Optional
import requests
import pandas as pd
import plotly.graph_objects as go
import chart_studio.plotly as py
from emoji import emojize
from requests.exceptions import HTTPError


class StockChartHandler:
    """Create chart from stock price data."""

    def __init__(self, token: str, endpoint: str):
        self.token = token
        self.endpoint = endpoint

    def get_chart(self, symbol: str) -> str:
        """Create chart of a company's 30-day stock performance."""
        message = self._get_price(symbol)
        chart = self._create_chart(symbol)
        if message or chart:
            return f'{message} {chart}'
        return emojize('⚠️ dats nought a stock symbol u RETART :@ ⚠️')

    def _get_price(self, symbol: str) -> Optional[str]:
        """Get daily price summary."""
        params = {'token': self.token}
        try:
            req = requests.get(
                f'{self.endpoint}{symbol}/quote',
                params=params
            )
            if req.status_code == 200:
                price = req.json().get('latestPrice', None)
                company_name = req.json().get("companyName", None)
                change = req.json().get("ytdChange", None)
                if price and company_name:
                    message = f"{company_name}: Current price of ${price:.2f}."
                    if change:
                        message = f"{company_name}: Current price of ${price:.2f}, change of {change:.2f}%"
                    return message
        except HTTPError as e:
            raise HTTPError(f'Failed to fetch stock price for `{symbol}`: {e.response.content}')
        return None

    def _get_chart_data(self, symbol: str) -> Optional[bytes]:
        """Fetch 30-day performance data from API."""
        params = {'token': self.token, 'includeToday': 'true'}
        url = f'{self.endpoint}{symbol}/chart/1m'
        try:
            req = requests.get(url, params=params)
            if req.status_code == 200 and req.content:
                return req.content
        except HTTPError as e:
            raise HTTPError(f'Failed to fetch stock timeseries data for `{symbol}`: {e.response.content}')
        return None

    @staticmethod
    def _parse_chart_data(data: bytes) -> Optional[pd.DataFrame]:
        """Parse JSON response into Pandas DataFrame"""
        stock_df = pd.read_json(data)
        stock_df = stock_df.loc[stock_df['date'].dt.dayofweek < 5]
        stock_df.set_index(keys=stock_df['date'], inplace=True)
        return stock_df

    def _create_chart(self, symbol: str) -> Optional[str]:
        """Create Plotly chart."""
        data = self._get_chart_data(symbol)
        if bool(data):
            stock_df = self._parse_chart_data(data)
            fig = go.Figure(data=[
                go.Candlestick(
                    x=stock_df.index,
                    open=stock_df['open'],
                    high=stock_df['high'],
                    low=stock_df['low'],
                    close=stock_df['close'],
                    decreasing={
                        "line": {
                            "color": "rgb(240, 99, 90)"
                        },
                        "fillcolor": "rgba(142, 53, 47, 0.5)"
                    },
                    increasing={
                        "line": {
                            "color": "rgb(48, 190, 161)"
                        },
                        "fillcolor": "rgba(22, 155, 124, 0.6)"
                    },
                    whiskerwidth=1,
                )],
                layout=go.Layout(
                    font={
                        "size": 15,
                        "family": "Open Sans",
                        "color": "#fff"
                    },
                    title={
                        "x": 0.5,
                        "font": {"size": 23},
                        "text": f'30-day performance of {symbol.upper()}'
                    },
                    xaxis={
                        'type': 'date',
                        'rangeslider': {
                            'visible': False
                        },
                        "ticks": "",
                        "gridcolor": "#283442",
                        "linecolor": "#506784",
                        "automargin": True,
                        "zerolinecolor": "#283442",
                        "zerolinewidth": 2
                    },
                    yaxis={
                        "ticks": "",
                        "gridcolor": "#283442",
                        "linecolor": "#506784",
                        "automargin": True,
                        "zerolinecolor": "#283442",
                        "zerolinewidth": 2
                    },
                    autosize=True,
                    plot_bgcolor="rgb(23, 27, 31)",
                    paper_bgcolor="rgb(23, 27, 31)",
                )
            )
            chart = py.plot(
                fig,
                filename=symbol,
                auto_open=False,
                fileopt='overwrite',
                sharing='public'
            )
            chart_url = chart.replace('plotly.com', 'chart-studio.plotly.com')
            return chart_url[:-1] + '.jpeg'
        return None
