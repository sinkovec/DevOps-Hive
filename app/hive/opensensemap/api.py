"""
Module for handling API requests to OpenSenseMap API.

This module defines the OpenSenseMapApi class, which is responsible for handling
API requests to the OpenSenseMap API.
"""
from datetime import datetime, timezone, timedelta
from dataclasses import asdict
import json
import requests

from redis import Redis

from .model import Sensor, SensorCache


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

        if data:
            data = SensorCache.from_json(json.loads(data))

        # when missing or caching content is older than 5 minutes
        should_recompute = not data or data.created_at < datetime.now(
            timezone.utc
        ) - timedelta(minutes=5)

        if should_recompute:
            response = requests.get(
                self._sensor_url(sense_box_id, sensor_id), timeout=30
            )
            if response.status_code == 200:
                data = SensorCache(
                    datetime.now(timezone.utc),
                    response.json(),
                )
                self.redis.set(cache_key, json.dumps(asdict(data), default=str))

        if data:
            data = Sensor.from_json(data.content)

        return data

    def sensor_data_ok(self, sense_box_id, sensor_id):
        """
        Performs an HEAD request to the sensor endpoint to check its availability.

        Returns:
            bool: true if the response status code is ok.
        """
        response = requests.get(self._sensor_url(sense_box_id, sensor_id), timeout=30)
        return response.status_code == 200

    def cache_created_at(self, sense_box_id, sensor_id):
        """
        For a given sensor, provides the creation datetime of cached data.

        Returns:
            datetime: datetime object representing timestamp when cache was created.
        """
        cache_key = self._cache_key(sense_box_id, sensor_id)
        data = self.redis.get(cache_key)
        return SensorCache.from_json(json.loads(data)).created_at if data else None

    def _cache_key(self, sense_box_id, sensor_id):
        return f"opensensemap_{sense_box_id}_{sensor_id}"

    def _sensor_url(self, sense_box_id, sensor_id):
        return f"{self.base_url}/boxes/{sense_box_id}/sensors/{sensor_id}"
