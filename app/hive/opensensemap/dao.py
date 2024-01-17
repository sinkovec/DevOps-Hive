"""
Module for handling data access to the OpenSenseMap database.

This module defines the OpenSenseMapDao class, which is responsible for retrieving sense box data
from the database.
"""
from .db import SENSOR_ID_DB


class OpenSenseMapDao:
    """
    Class to handle data access to OpenSenseMap database.
    """

    def __init__(self):
        self.sense_box_sensor_ids = SENSOR_ID_DB

    def load_sense_box_sensor_ids(self):
        """
        Retrieves sense boxes stored from the injected data.

        Returns:
            list: List containing sense box data.
        """
        return self.sense_box_sensor_ids
