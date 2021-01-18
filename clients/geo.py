import requests


class GeoIP:
    def __init__(self, key: str):
        self.url = "https://api.ipdata.co"
        self.key = key

    def get_location(self, ip: str):
        params = {"api-key", self.key}
        req = requests.get(f"self.url/{ip}", params=params)
        res = req.json()
