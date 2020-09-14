"""Create cloud-hosted Candlestick charts of company stock data."""
from typing import Optional
import requests
import pandas as pd
import plotly.graph_objects as go
import chart_studio.plotly as py


class StockChartHandler:
    """Create chart from stock market data."""

    def __init__(self, token: str, endpoint: str):
        self.token = token
        self.endpoint = endpoint

    def get_chart(self, symbol: str):
        """Create chart of a company's 30-day stock performance."""
        message = self._get_price(symbol)
        chart = self._create_chart(symbol)
        return f'{message} {chart}'

    def _get_price(self, symbol: str):
        """Get daily price summary."""
        params = {'token': self.token}
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
        return None

    def _get_chart_data(self, symbol: str) -> Optional[pd.DataFrame]:
        """Fetch 30-day performance data from API."""
        params = {'token': self.token, 'includeToday': 'true'}
        url = f'{self.endpoint}{symbol}/chart/1m'
        req = requests.get(url, params=params)
        if req.status_code == 200:
            stock_df = pd.read_json(req.content)
            if stock_df.empty is False:
                stock_df = stock_df.loc[stock_df['date'].dt.dayofweek < 5]
                stock_df.set_index(keys=stock_df['date'], inplace=True)
                return stock_df
        return None

    def _create_chart(self, symbol: str) -> Optional[str]:
        """Create Plotly chart."""
        stock_df = self._get_chart_data(symbol)
        if stock_df.empty is False:
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
            chart_image = chart[:-1] + '.png'
            return chart_image
        return None
