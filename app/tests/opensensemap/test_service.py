"""
Module: test_open_sense_map_service.py

This module contains unit tests for the methods in the hive.opensensemap.service module.
"""

from datetime import datetime, timezone
from unittest.mock import Mock

from hive.opensensemap.model import Sensor, Measurement
from hive.opensensemap.service import OpenSenseMapService

def create_sensor(value):
    """
    Helper function to create a Sensor object with a specific value.

    :param value: Numeric value for the sensor measurement.
    :return: Sensor object
    """
    return Sensor("some-id", "some-title", Measurement(datetime.now(timezone.utc), value))

def test_calculate_average_temperature_positive():
    """
    Test the `OpenSenseMapService.calculate_average_temperature` method 
    with positive temperature values.

    Checks if the average temperature is correctly calculated when provided 
    with positive temperature values.
    """
    # given
    mock_repository = Mock()
    mock_repository.get_sensor_data.return_value = [
        create_sensor(4),
        create_sensor(4.5),
        create_sensor(5),
    ]
    uut = OpenSenseMapService(mock_repository)
    # when
    result = uut.calculate_average_temperature()
    # then
    assert result == 4.5

def test_calculate_average_temperature_negative():
    """
    Test the `OpenSenseMapService.calculate_average_temperature` method 
    with negative temperature values.

    Checks if the average temperature is correctly calculated when provided 
    with negative temperature values.
    """
    # given
    mock_repository = Mock()
    mock_repository.get_sensor_data.return_value = [
        create_sensor(-5),
        create_sensor(-10),
    ]
    uut = OpenSenseMapService(mock_repository)
    # when
    result = uut.calculate_average_temperature()
    # then
    assert result == -7.5

def test_calculate_average_temperature_no_measurements():
    """
    Test the `OpenSenseMapService.calculate_average_temperature` method 
    with no measurements available.

    Checks if the method returns an appropriate message when no measurements are present.
    """
    # given
    mock_repository = Mock()
    mock_repository.get_sensor_data.return_value = []
    uut = OpenSenseMapService(mock_repository)
    # when
    result = uut.calculate_average_temperature()
    # then
    assert result == "No current measurements present."
