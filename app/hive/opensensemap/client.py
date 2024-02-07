"""
Module for handling API requests to OpenSenseMap API.

This module defines the OpenSenseMapApi class, which is responsible for handling
API requests to the OpenSenseMap API.
"""
import requests


# pylint: disable=too-few-public-methods
class OpenSenseMapClient:
    """
    Class to handle API requests to OpenSenseMap API.

    This class encapsulates functionality to make requests to the OpenSenseMap API and
    retrieve the latest measurements for a specified Sense Box and Sensor.
    """

    def __init__(self, base_url: str):
        self.base_url = base_url

    def fetch_sense_box(self, sense_box_id):
        """
        Fetches sense box from API by id.

        Args:
            sense_box_id (str): Identifier for the Sense Box.

        Returns:
            SenseBox: SenseBox instance.
        """
        response = requests.get(f"{self.base_url}/boxes/{sense_box_id}", timeout=30)
        data = None
        if response.status_code == 200:
            data = response.json()
        return data
