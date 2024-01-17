from datetime import datetime, timezone
from unittest.mock import Mock

from hive.opensensemap.model import Sensor, Measurement
from hive.opensensemap.service import OpenSenseMapService

def create_sensor(value):
    return Sensor("some-id", "some-title", Measurement(datetime.now(timezone.utc), value))

def test_calculate_average_temperature_positive():
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
    # given
    mock_repository = Mock()
    mock_repository.get_sensor_data.return_value = []
    uut = OpenSenseMapService(mock_repository)
    # when
    result = uut.calculate_average_temperature()
    # then
    assert result == "No current measurements present."
