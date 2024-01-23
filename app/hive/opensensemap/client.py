"""
Module for handling API requests to OpenSenseMap API.

This module defines the OpenSenseMapApi class, which is responsible for handling
API requests to the OpenSenseMap API.
"""
import requests


class OpenSenseMapClient:
    """
    Class to handle API requests to OpenSenseMap API.

    This class encapsulates functionality to make requests to the OpenSenseMap API and
    retrieve the latest measurements for a specified Sense Box and Sensor.
    """

    def __init__(self, base_url: str):
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
        response = self._get_sensor_data(sense_box_id, sensor_id)
        data = None
        if response.status_code == 200:
            data = response.json()
        return data

    def sensor_data_ok(self, sense_box_id, sensor_id):
        """
        Performs an HEAD request to the sensor endpoint to check its availability.

        Returns:
            bool: true if the response status code is ok.
        """
        response = self._get_sensor_data(sense_box_id, sensor_id)
        return response.status_code == 200

    def _get_sensor_data(self, sense_box_id, sensor_id):
        return requests.get(self._sensor_url(sense_box_id, sensor_id), timeout=30)

    def _sensor_url(self, sense_box_id, sensor_id):
        return f"{self.base_url}/boxes/{sense_box_id}/sensors/{sensor_id}"
