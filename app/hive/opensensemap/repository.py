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
    def __init__(self, api, dao):
        self.api = api
        self.dao = dao

    def get_sense_box_sensor_ids(self):
        """
        Retrieves sense box and sensor ids from the data sources.

        Returns:
            list: List of sense boxes.
        """
        return self.dao.get_sense_box_sensor_ids()

    def get_sensor_data(self, sense_box_id, sensor_id):
        """
        Retrieves sensor data using the OpenSenseMap API.

        Args:
            sense_box_id (str): Identifier for the Sense Box.
            sensor_id (str): Identifier for the sensor.

        Returns:
            list: Sensor data for the specified Sense Box and sensor.
        """
        return self.api.get_sensor_data(sense_box_id, sensor_id)
