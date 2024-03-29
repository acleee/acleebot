from typing import Union

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

    def lookup_user(self, ip_address: str) -> dict:
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
        except Exception as e:
            raise Exception(e)

    @staticmethod
    def save_metadata(room_name: str, user_name: str, ip_metadata: dict) -> Union[DataFrame, str]:
        """
        Parse IP metadata into Pandas Dataframe.

        :param str room_name: Chatango room.
        :param str user_name: Chatango user's username.
        :param dict ip_metadata: Metadata associated with a given message.

        :returns: DataFrame
        """
        try:
            record = {"username": user_name, "chatango_room": room_name}
            record.update(ip_metadata)
            metadata_df = pd.json_normalize([record], sep="_")
            metadata_df = metadata_df.infer_objects()
            metadata_df.astype(
                {
                    "username": "string",
                    "chatango_room": "string",
                    "city": "string",
                    "region": "string",
                    "country_name": "string",
                    "latitude": "float",
                    "longitude": "float",
                    "postal": "Int64",
                    "emoji_flag": "string",
                    "status": "Int64",
                    "time_zone_name": "string",
                    "time_zone_abbr": "string",
                    "time_zone_offset": "Int64",
                    "time_zone_is_dst": "Int8",
                    "carrier_name": "string",
                    "carrier_mnc": "string",
                    "carrier_mcc": "string",
                    "asn_asn": "string",
                    "asn_name": "string",
                    "asn_domain": "string",
                    "asn_route": "string",
                    "asn_type": "string",
                    "ip": "string",
                }
            )
            return metadata_df
        except Exception as e:
            return f"Could not parse user data for {user_name}: {e}"
