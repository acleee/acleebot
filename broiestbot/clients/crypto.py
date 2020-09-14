"""Create cloud-hosted Candlestick charts of company stock data."""
from typing import Optional
import requests
import pandas as pd
import plotly.graph_objects as go
import chart_studio.plotly as py


class CryptoChartHandler:
    """Create chart from stock market data."""

    def __init__(self, token: str, price_endpoint: str, chart_endpoint: str):
        self.token = token
        self.price_endpoint = price_endpoint
        self.chart_endpoint = chart_endpoint

    def get_chart(self, symbol: str):
        """Get crypto data and generate Plotly chart."""
        price = self._get_price(symbol)
        chart = self._create_chart(symbol)
        return f'{price} {chart}'

    def _get_price(self, symbol) -> str:
        """Get crypto price for provided ticker label."""
        endpoint = f'{self.price_endpoint}{symbol.lower()}usd/summary'
        req = requests.get(url=endpoint)
        prices = req.json()["result"]["price"]
        percentage = prices["change"]['percentage'] * 100
        if prices["last"] > 1:
            response = f'{symbol.upper()}: Currently at ${prices["last"]:.2f}. ' \
                       f'HIGH today of ${prices["high"]:.2f}, LOW of ${prices["low"]:.2f} ' \
                       f'(change of {percentage:.2f}%).'
        else:
            response = f'{symbol.upper()}: Currently at ${prices["last"]}. ' \
                       f'HIGH today of ${prices["high"]} LOW of ${prices["low"]} ' \
                       f'(change of {percentage:.2f}%).'
        return response

    def _get_chart_data(self, symbol: str) -> Optional[pd.DataFrame]:
        """Fetch 60-day crypto prices."""
        params = {
            'function': 'DIGITAL_CURRENCY_DAILY',
            'symbol': symbol,
            'market': 'USD',
            'apikey': self.token
        }
        req = requests.get(self.chart_endpoint, params=params)
        data = req.json()
        df = pd.DataFrame.from_dict(data['Time Series (Digital Currency Daily)'], orient='index')[:60]
        if df.empty is False:
            return df
        return None

    def _create_chart(self, symbol: str) -> Optional[str]:
        """Create Plotly chart for given crypto symbol."""
        df = self._get_chart_data(symbol)
        df = df.apply(pd.to_numeric)
        fig = go.Figure(data=[
            go.Candlestick(
                x=df.index,
                open=df['1a. open (USD)'],
                high=df['2a. high (USD)'],
                low=df['3a. low (USD)'],
                close=df['4a. close (USD)'],
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
            )
        ],
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
