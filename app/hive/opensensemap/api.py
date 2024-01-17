"""
Module for handling API requests to OpenSenseMap API.

This module defines the OpenSenseMapApi class, which is responsible for handling
API requests to the OpenSenseMap API.
"""
import requests

from .model import Sensor


class OpenSenseMapApi:
    """
    Class to handle API requests to OpenSenseMap API.

    This class encapsulates functionality to make requests to the OpenSenseMap API and
    retrieve the latest measurements for a specified Sense Box and Sensor.
    """
    def __init__(self, base_url):
        self.base_url = base_url

    def fetch_sensor_data(self, sense_box_id, sensor_id):
        """
        Retrieves current sensor data for the given Sense Box and Sensor id
        using the OpenSenseMap API.

        Args:
            sense_box_id (str): Identifier for the Sense Box.
            sensor_id (str): Identifier for the sensor.

        Returns:
            list: Sensor instance representing the retrieved current sensor data.
        """
        response = requests.get(
            f"{self.base_url}/boxes/{sense_box_id}/sensors/{sensor_id}"
        )
        if response.status_code == 200:
            return Sensor.from_json(response.json())
        return None
