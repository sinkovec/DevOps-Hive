"""
Module for interacting with the OpenSenseMap service to calculate average temperatures.

This module defines the OpenSenseMapService class, which provides functionality for
retrieving data from the OpenSenseMap repository and calculating the average temperature
emitted by sensors in the given Sense Boxes.
"""
from datetime import datetime, timedelta
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

        This method retrieves measurements from the past hour for each sensor in each Sense Box,
        and then calculates the average temperature.

        Returns:
            float: The average temperature value of all sensors.
        """
        sense_boxes = self.repository.get_sense_boxes()
        from_date = self._past_hour_timestamp()
        measurements_per_sensor = [
            self._get_measurement_values(sense_box, sensor, from_date)
            for sense_box in sense_boxes
            for sensor in sense_box.sensors
        ]
        average_per_sensor = [mean(measurements) for measurements in measurements_per_sensor]
        return round(mean(average_per_sensor), 2)

    def _get_measurement_values(self, sense_box, sensor, from_date):
        """
        Retrieves measurement values for a specific sensor and time period.

        Args:
            sense_box (object): A Sense Box instance.
            sensor (object): A Sensor instance.
            from_date (datetime): The starting timestamp for measurements.

        Returns:
            list: List of measurement values for the specified sensor and time period.
        """
        result = self.repository.get_measurements(
            sense_box.id, sensor.id, from_date.isoformat(timespec="seconds")
        )
        return list(map(lambda x: x.value, result))

    def _past_hour_timestamp(self):
        """
        Return the timestamp for the past hour.

        Returns:
            datetime: The timestamp for the past hour.
        """
        return datetime.now() - timedelta(hours=1)
