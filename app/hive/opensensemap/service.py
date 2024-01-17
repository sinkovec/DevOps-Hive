"""
Module for interacting with the OpenSenseMap service to calculate average temperatures.

This module defines the OpenSenseMapService class, which provides functionality for
retrieving data from the OpenSenseMap repository and calculating the average temperature
emitted by sensors in the given Sense Boxes.
"""
from datetime import datetime, timedelta, timezone
from statistics import mean


class OpenSenseMapService:
    """
    OpenSenseMapService class for interacting with the OpenSenseMap service.

    This class encapsulates functionality to interact with the OpenSenseMap repository
    and calculate the average temperature emitted by sensors in the given Sense Boxes.
    """

    def __init__(self, repository):
        self.repository = repository

    def calculate_average_temperature(self):
        """
        Calculate the average temperature emitted by sensors in the given Sense Boxes.

        This method retrieves the latest measurement from the past hour for each sensor 
        in each Sense Box, and then calculates the average temperature.

        Returns:
            float: The average temperature value of all sensors.
        """
        from_date = self._past_hour_timestamp()
        sensor_data = self.repository.get_sensor_data()
        last_measurements = [
            sensor.last_measurement.value
            for sensor in sensor_data
            if from_date < sensor.last_measurement.created_at
        ]
        if last_measurements:
            return round(mean(last_measurements), 2)
        return "No current measurements present."

    def _past_hour_timestamp(self):
        """
        Return the timestamp for the past hour.

        Returns:
            datetime: The timestamp for the past hour.
        """
        return datetime.now(timezone.utc) - timedelta(hours=1)
