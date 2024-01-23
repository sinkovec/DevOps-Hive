"""
Module for interacting with the OpenSenseMap service to calculate average temperatures.

This module defines the OpenSenseMapService class, which provides functionality for
retrieving data from the OpenSenseMap repository and calculating the average temperature
emitted by sensors in the given Sense Boxes.
"""
from datetime import datetime, timedelta, timezone
from statistics import mean

from .schemas import TemperatureBase, TemperatureStatus
from .repository import OpenSenseMapRepository


class OpenSenseMapService:
    """
    OpenSenseMapService class for interacting with the OpenSenseMap service.

    This class encapsulates functionality to interact with the OpenSenseMap repository
    and calculate the average temperature emitted by sensors in the given Sense Boxes.
    """

    def __init__(self, repository: OpenSenseMapRepository):
        self.repository = repository

    def get_temperature(self) -> TemperatureBase:
        """
        Returns the current average temperature and corresponding status message.

        Returns:
          TemperatureBase: status message and temperature
        """
        avg_temperature = self.calculate_average_temperature()
        status = self.temperature_status(avg_temperature)
        return TemperatureBase(status=status, temperature=avg_temperature)

    def temperature_status(self, temperature: float) -> TemperatureStatus:
        """
        Returns a string depending on the given temperature.

        Possible values: "Too Cold", "Good", "Too Hot".

        Returns:
            string: Textual representation of temperature.
        """
        if temperature is None:
            status = TemperatureStatus.NONE
        if temperature < 10:
            status = TemperatureStatus.TOO_COLD
        elif temperature <= 37:
            status = TemperatureStatus.GOOD
        else:
            status = TemperatureStatus.TOO_HOT
        return status

    def calculate_average_temperature(self) -> float:
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
            if sensor and from_date < sensor.last_measurement.created_at
        ]
        if not last_measurements:
            return None
        return round(mean(last_measurements), 2)

    def _past_hour_timestamp(self) -> datetime:
        """
        Return the timestamp for the past hour.

        Returns:
            datetime: The timestamp for the past hour.
        """
        return datetime.now(timezone.utc) - timedelta(hours=1)

    def sensor_data_available(self) -> bool:
        """
        Check if sensor data is available based on certain conditions.
        - More than 50% + 1 sensors are available AND
        - Caching content does not expire within 5 minutes.

        Returns:
            bool: True if sensor data is available; False otherwise.
        """
        sensors = self.repository.sensors_ready()
        if sensors.count(False) >= len(sensors) // 2 + 1:
            created_at = self.repository.get_created_at_times()
            return not all(map(self._is_older_than(timedelta(minutes=5)), created_at))
        return True

    def _is_older_than(self, td):
        now = datetime.now(timezone.utc)

        def predicate(timestamp):
            return not timestamp or timestamp + td < now

        return predicate
