"""
Module: test_open_sense_map_service.py

This module contains unit tests for the methods in the hive.opensensemap.service module.
"""

from datetime import datetime, timezone, timedelta
from unittest.mock import Mock
import pytest

from hive.opensensemap.model import Sensor, Measurement
from hive.opensensemap.service import OpenSenseMapService


def fake_sensor(value):
    """
    Helper function to create a Sensor object with a specific value.

    :param value: Numeric value for the sensor measurement.
    :return: Sensor object
    """
    return Sensor(
        "some-id", "some-title", Measurement(datetime.now(timezone.utc), value)
    )


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
        fake_sensor(4),
        fake_sensor(4.5),
        fake_sensor(5),
    ]
    uut = OpenSenseMapService(mock_repository)
    # when
    result = uut.calculate_average_temperature()
    # then
    assert result == pytest.approx(4.5)


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
        fake_sensor(-5),
        fake_sensor(-10),
    ]
    uut = OpenSenseMapService(mock_repository)
    # when
    result = uut.calculate_average_temperature()
    # then
    assert result == pytest.approx(-7.5)


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
    assert result is None


def test_calculate_average_temperature_contains_none_measurements():
    """
    Test the `OpenSenseMapService.calculate_average_temperature` method
    with, but not limited to, None measurements returned.

    Checks if the method returns an appropriate message when measurements
    from repository contains None values.
    """
    # given
    mock_repository = Mock()
    mock_repository.get_sensor_data.return_value = [fake_sensor(0), None]
    uut = OpenSenseMapService(mock_repository)
    # when
    result = uut.calculate_average_temperature()
    # then
    assert result == 0


def test_calculate_average_temperature_only_none_measurements():
    """
    Test the `OpenSenseMapService.calculate_average_temperature` method
    with only None measurements returned.

    Checks if the method returns an appropriate message when measurements
    from repository contains only None values.
    """
    # given
    mock_repository = Mock()
    mock_repository.get_sensor_data.return_value = [None]
    uut = OpenSenseMapService(mock_repository)
    # when
    result = uut.calculate_average_temperature()
    # then
    assert result is None


@pytest.mark.parametrize(
    "temperature, expected_result",
    [
        (-10, "Too Cold"),
        (9, "Too Cold"),
        (10, "Good"),
        (37, "Good"),
        (38, "Too Hot"),
        (9999, "Too Hot"),
    ],
)
def test_temperature_status(temperature, expected_result):
    """
    Test the `OpenSenseMapService.temperature_status` method
    with several temperatures as input (parameterized) including boundary testing.

    Checks if the method returns an appropriate message for given temperatures.
    """
    # given
    uut = OpenSenseMapService(None)
    # when
    result = uut.temperature_status(temperature)
    # then
    assert result == expected_result


@pytest.mark.parametrize(
    "sensors_ready, timedeltas, expected_result",
    [
        ([True, True, False], [], True),
        ([True, False, False], [1, None, 10], True),
        ([False, False, False], [None, None, 6], False),
    ],
)
def test_sensor_data_available(sensors_ready, timedeltas, expected_result):
    """
    Test the `OpenSenseMapService.sensor_data_available` method
    with several sensor_ready results and timedeltas as input (parameterized).

    Checks if the method returns True when enough sensors are available or caches are present,
    False otherwise.
    """
    # given
    mock_repository = Mock()
    mock_repository.sensors_ready.return_value = sensors_ready
    now = datetime.now(timezone.utc)
    created_at_times = map(
        lambda td: now - timedelta(minutes=td) if td else None, timedeltas
    )
    mock_repository.get_created_at_times.return_value = created_at_times
    uut = OpenSenseMapService(mock_repository)
    # when
    result = uut.sensor_data_available()
    # then
    assert result == expected_result


@pytest.mark.parametrize(
    "td, expected_result",
    [(60, True), (5, True), (1, False), (None, True)],
)
def test_is_older_than_5_minutes(td, expected_result):
    """
    Test the `OpenSenseMapService._is_older_than` method
    with several timdeltas as input (parameterized).

    Checks if the method returns True if the timestamp is more than 5 minutes ago from now on.
    """
    # given
    uut = OpenSenseMapService(None)
    # when
    timestamp = datetime.now(timezone.utc) - timedelta(minutes=td) if td else None
    # pylint: disable=protected-access
    result = uut._is_older_than(timedelta(minutes=5))(timestamp)
    # then
    assert result == expected_result
