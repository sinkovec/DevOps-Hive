"""
Module for handling API requests to OpenSenseMap API.

This module defines the OpenSenseMapApi class, which is responsible for handling
API requests to the OpenSenseMap API.
"""
from datetime import datetime, timezone
import json
import requests

from redis import Redis

from .model import Sensor


class OpenSenseMapApi:
    """
    Class to handle API requests to OpenSenseMap API.

    This class encapsulates functionality to make requests to the OpenSenseMap API and
    retrieve the latest measurements for a specified Sense Box and Sensor.
    """

    # pylint: disable=too-few-public-methods
    def __init__(self, base_url: str, redis: Redis):
        self.base_url = base_url
        self.redis = redis
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
                self._sensor_url(sense_box_id, sensor_id), timeout=30
            )
            if response.status_code == 200:
                data = response.content
                self.redis.set(cache_key, data, ex=self.redis_expire_time)

        if data:
            data = Sensor.from_json(json.loads(data))

        return data

    def sensor_data_ok(self, sense_box_id, sensor_id):
        """
        Performs an HEAD request to the sensor endpoint to check its availability.

        Returns:
            bool: true if the response status code is ok.
        """
        response = requests.head(self._sensor_url(sense_box_id, sensor_id), timeout=30)
        return response.status_code == 200

    def expire_time(self, sense_box_id, sensor_id):
        """
        For a given sensor, provides the expire time of cached data, i.e.,
        when the sensor data will be evicted from Redis cache.

        Returns:
            datetime: datetime object representing timestamp when cache is evicted.
        """
        cache_key = self._cache_key(sense_box_id, sensor_id)
        expire_time = self.redis.expiretime(cache_key)
        if expire_time < 0:
            return None
        return datetime.fromtimestamp(expire_time, timezone.utc)

    def _cache_key(self, sense_box_id, sensor_id):
        return f"opensensemap_{sense_box_id}_{sensor_id}"

    def _sensor_url(self, sense_box_id, sensor_id):
        return f"{self.base_url}/boxes/{sense_box_id}/sensors/{sensor_id}"
