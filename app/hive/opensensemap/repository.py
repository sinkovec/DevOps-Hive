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
