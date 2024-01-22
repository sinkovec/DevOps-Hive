"""
Module for handling API requests to OpenSenseMap API.

This module defines the OpenSenseMapApi class, which is responsible for handling
API requests to the OpenSenseMap API.
"""
import json
import requests

from .model import Sensor


class OpenSenseMapApi:
    """
    Class to handle API requests to OpenSenseMap API.

    This class encapsulates functionality to make requests to the OpenSenseMap API and
    retrieve the latest measurements for a specified Sense Box and Sensor.
    """

    # pylint: disable=too-few-public-methods
    def __init__(self, base_url, redis):
        self.base_url = base_url
        self.redis = redis
        self.redis_cache_key = "opensensemap_%s_%s"
        self.redis_expire_time = 60 * 30

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
        cache_key = self._cache_key(sense_box_id, sensor_id)
        data = self.redis.get(cache_key)

        if not data:
            response = requests.get(
                f"{self.base_url}/boxes/{sense_box_id}/sensors/{sensor_id}", timeout=30
            )
            if response.status_code == 200:
                data = response.content
                self.redis.set(cache_key, data, ex=self.redis_expire_time)

        if data:
            data = Sensor.from_json(json.loads(data))

        return data

    def _cache_key(self, sense_box_id, sensor_id):
        return self.redis_cache_key.format(sense_box_id, sensor_id)
