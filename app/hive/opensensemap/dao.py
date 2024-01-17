"""
Module for handling data access to the OpenSenseMap database.

This module defines the OpenSenseMapDao class, which is responsible for retrieving sense box data
from the database.
"""
from .db import SENSE_BOXES_DB


class OpenSenseMapDao:
    """
    Class to handle data access to OpenSenseMap database.
    """

    def __init__(self):
        self.sense_boxes = SENSE_BOXES_DB

    def get_sense_boxes(self):
        """
        Retrieves sense boxes stored from the injected data.

        Returns:
            list: List containing sense box data.
        """
        return self.sense_boxes
