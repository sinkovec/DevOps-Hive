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

    def get_sense_boxes(self):
        """
        Retrieves sense boxes from the data sources.

        Returns:
            list: List of sense boxes.
        """
        return self.dao.get_sense_boxes()

    def get_measurements(self, sense_box_id, sensor_id, from_date):
        """
        Retrieves measurements using the OpenSenseMap API.

        Args:
            sense_box_id (str): Identifier for the Sense Box.
            sensor_id (str): Identifier for the sensor.
            from_date (datetime): The starting timestamp for measurements.

        Returns:
            list: List of measurements for the specified Sense Box and sensor.
        """
        return self.api.get_measurements(sense_box_id, sensor_id, from_date)
