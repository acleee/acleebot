from ipdata import ipdata
import requests
from requests.exceptions import HTTPError

from config import IP_DATA_ENDPOINT, IP_DATA_KEY


class GeoIP:
    def __init__(self, key: str):
        self.url = "https://api.ipdata.co"
        self.key = key

    def get_ip_metadata(self, ip: str) -> dict:
        try:
            params = {"api-key", self.key}
            req = requests.get(f"self.url/{ip}", params=params)
            return req.json()
        except HTTPError as e:
            raise HTTPError(
                f"Failed to fetch IP data for `{ip}`: {e.response.content}"
            )
        except Exception as e:
            raise Exception(
                f"Unexpected error while fetching IP data for `{ip}`: {e}"
            )
            
    def parse(res: dict) -> dict:
        pass
