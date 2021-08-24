import pandas as pd
from ipdata import ipdata
from ipdata.ipdata import APIKeyNotSet, IncompatibleParameters, IPData
from pandas import DataFrame


class GeoIP:
    def __init__(self, api_key: str):
        self.api_key = api_key

    @property
    def client(self) -> IPData:
        try:
            return ipdata.IPData(self.api_key)
        except APIKeyNotSet as e:
            raise APIKeyNotSet(e)

    def get_ip_metadata(self, ip_address: str) -> dict:
        """
        Fetch metadata associated with user's IP address.

        :param str ip_address: Chatango user's IP address.

        :returns: dict
        """
        try:
            return self.client.lookup(
                ip=ip_address,
                fields=[
                    "city",
                    "region",
                    "country_name",
                    "latitude",
                    "longitude",
                    "postal",
                    "emoji_flag",
                    "time_zone",
                    "threat",
                    "asn",
                    "carrier",
                ],
            )
        except IncompatibleParameters as e:
            raise IncompatibleParameters(e)

    def parse(self, room_name: str, user_name: str, ip_address: str) -> DataFrame:
        """
        Parse IP metadata into Pandas Dataframe.

        :param str room_name: Chatango room.
        :param str user_name: Chatango user's username.
        :param str ip_address: Chatango user's IP address.

        :returns: DataFrame
        """
        record = {"user": user_name, "chatango_room": room_name}
        ip_metadata = self.get_ip_metadata(ip_address)
        record.update(ip_metadata)
        metadata_df = pd.json_normalize([record], sep="_")
        metadata_df = metadata_df.infer_objects()
        return metadata_df
