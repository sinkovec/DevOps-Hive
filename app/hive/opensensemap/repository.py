"""
Module for interacting with the OpenSenseMap API.

This module defines the OpenSenseMapRepository class, which serves as a repository to
interact with both the OpenSenseMap API and the database.
"""
from datetime import datetime, timezone, timedelta
from dataclasses import asdict
import json

from redis import Redis

from .dao import OpenSenseMapDao
from .client import OpenSenseMapClient
from .model import CachedResponse, Sensor


class OpenSenseMapRepository:
    """
    Repository to interact with OpenSenseMap API and database.

    This class encapsulates functionality to retrieve sense boxes from the data sources
    and to fetch measurements using the OpenSenseMap API.
    """

    def __init__(self, api: OpenSenseMapClient, dao: OpenSenseMapDao, redis: Redis):
        self.api = api
        self.dao = dao
        self.redis = redis

    def get_sensor_data(self):
        """
        Fetches sensor data using the OpenSenseMap API
        of the sensors provided in the database.

        Returns:
            list: Sensor data for the stored Sense Box and sensor.
        """
        return [
            self._get_sensor_data(sense_box_id, sensor_id)
            for (sense_box_id, sensor_id) in self.dao.load_sense_box_sensor_ids()
        ]

    def _get_sensor_data(self, sense_box_id, sensor_id):
        cache_key = self._cache_key(sense_box_id, sensor_id)
        data = self.redis.get(cache_key)

        if data:
            data = CachedResponse.from_json(json.loads(data))

        # when missing or caching content is older than 5 minutes
        should_recompute = not data or data.created_at < datetime.now(
            timezone.utc
        ) - timedelta(minutes=5)

        if should_recompute:
            data = self.api.fetch_sensor_data(sense_box_id, sensor_id)
            if data:
                cache = CachedResponse(
                    datetime.now(timezone.utc),
                    data,
                )
                self.redis.set(cache_key, json.dumps(asdict(cache), default=str))

        if data:
            data = Sensor.from_json(data)

        return data

    def sensors_ready(self):
        """
        For each sensor, checks via OpenSenseMapApi if a response is ok.

        Returns:
            list: true for each sensor, if API returns ok.
        """
        return [
            self.api.sensor_data_ok(sense_box_id, sensor_id)
            for (sense_box_id, sensor_id) in self.dao.load_sense_box_sensor_ids()
        ]

    def get_created_at_times(self):
        """
        Fetches caching expire times for each sensor provided
        in the database.

        Returns:
            list: Caching expire times for each sensor data
        """
        return [
            self.cache_created_at(sense_box_id, sensor_id)
            for (sense_box_id, sensor_id) in self.dao.load_sense_box_sensor_ids()
        ]

    def cache_created_at(self, sense_box_id, sensor_id):
        """
        For a given sensor, provides the creation datetime of cached data.

        Returns:
            datetime: datetime object representing timestamp when cache was created.
        """
        cache_key = self._cache_key(sense_box_id, sensor_id)
        data = self.redis.get(cache_key)
        return CachedResponse.from_json(json.loads(data)).created_at if data else None

    def _cache_key(self, sense_box_id, sensor_id):
        return f"opensensemap_{sense_box_id}_{sensor_id}"
