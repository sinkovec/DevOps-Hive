"""
Module for handling API requests to OpenSenseMap API.

This module defines the OpenSenseMapApi class, which is responsible for handling
API requests to the OpenSenseMap API and retrieving measurements.
"""
import requests

from .model import Measurement


class OpenSenseMapApi:
    """
    Class to handle API requests to OpenSenseMap API.

    This class encapsulates functionality to make requests to the OpenSenseMap API and
    retrieve the latest measurements for a specified Sense Box and Sensor.
    """
    def __init__(self, base_url):
        self.base_url = base_url

    def get_measurements(self, sense_box_id, sensor_id, from_date):
        """
        Retrieves the 10000 latest measurements from the given date until now for the given
        Sense Box and Sensor using the OpenSenseMap API.

        Args:
            sense_box_id (str): Identifier for the Sense Box.
            sensor_id (str): Identifier for the sensor.
            from_date (datetime): The starting timestamp for measurements.

        Returns:
            list: List of Measurement instances representing the retrieved measurements.
        """
        response = requests.get(
            f"{self.base_url}/boxes/{sense_box_id}/data/{sensor_id}?from_date={from_date}"
        )
        if response.status_code == 200:
            return [Measurement.from_json(json_data) for json_data in response.json()]
        return None
