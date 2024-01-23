"""
Module for interacting with the OpenSenseMap API.

This module defines the OpenSenseMapRepository class, which serves as a repository to
interact with both the OpenSenseMap API and the database.
"""


class OpenSenseMapRepository:
    """
    Repository to interact with OpenSenseMap API and database.

    This class encapsulates functionality to retrieve sense boxes from the data sources
    and to fetch measurements using the OpenSenseMap API.
    """

    # pylint: disable=too-few-public-methods
    def __init__(self, api, dao):
        self.api = api
        self.dao = dao

    def get_sensor_data(self):
        """
        Fetches sensor data using the OpenSenseMap API
        of the sensors provided in the database.

        Returns:
            list: Sensor data for the stored Sense Box and sensor.
        """
        return [
            self.api.fetch_sensor_data(sense_box_id, sensor_id)
            for (sense_box_id, sensor_id) in self.dao.load_sense_box_sensor_ids()
        ]

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


    def get_expire_times(self):
        """
        Fetches caching expire times for each sensor provided
        in the database.

        Returns:
            list: Caching expire times for each sensor data
        """
        return [
            self.api.expire_time(sense_box_id, sensor_id)
            for (sense_box_id, sensor_id) in self.dao.load_sense_box_sensor_ids()
        ]
