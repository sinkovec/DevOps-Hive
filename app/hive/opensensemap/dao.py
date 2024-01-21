"""
Module for handling data access to the OpenSenseMap database.

This module defines the OpenSenseMapDao class, which is responsible for retrieving sense box data
from the database.
"""
import re

from hive.config import settings
from .db import SENSOR_ID_DB


class OpenSenseMapDao:
    """
    Class to handle data access to OpenSenseMap database.
    """
    # pylint: disable=too-few-public-methods
    def __init__(self):
        self.sense_box_sensor_ids = self._load_sense_boxes()

    def _load_sense_boxes(self):
        """
        Helper method to load sense boxes from environment variables.
        If no sense boxes are provided as environment variables, sense boxes
        stored in a DB variable are returned by default.

        Returns:
            list: List containing sense box data.

        Raises:
            RuntimeError: If the provided senseBoxes do not match the expected format.
        """
        sense_box_sensor_ids = settings.get("SENSE_BOXES", None)

        if sense_box_sensor_ids is None:
            sense_box_sensor_ids = SENSOR_ID_DB
        elif re.match(r"^[a-z0-9]+,[a-z0-9]+(;[a-z0-9]+,[a-z0-9]+)*", sense_box_sensor_ids):
            sense_box_sensor_ids = [
                senseBox.split(",")
                for senseBox in sense_box_sensor_ids.split(";")
            ]
        else:
            raise RuntimeError(f"Provided senseBoxes {sense_box_sensor_ids} \
                               does not match input format.")
        return sense_box_sensor_ids

    def load_sense_box_sensor_ids(self):
        """
        Retrieves sense boxes stored from the injected data.

        Returns:
            list: List containing sense box data.
        """
        return self.sense_box_sensor_ids
