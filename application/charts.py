import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
from .google_storage import GCS
from config import Config


def create_chart(df, symbol, title):
    """Generate market chart."""
    gcs = GCS(Config.GOOGLE_BUCKET_NAME, Config.GOOGLE_BUCKET_URL)
    gcs.upload_file(f'images/{symbol}.jpg', f'{symbol}.jpg')
    fig = px.line(df, x="timestamp", y="close", title=title)
    fig.write_image(f"images/{symbol}.jpg")
