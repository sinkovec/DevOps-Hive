from datetime import datetime

from hive.opensensemap.model import Sensor, Measurement

def test_measurement_from_json():
    # given
    json_data = {
        "createdAt": "2024-01-17T20:00:00.00Z",
        "value": "1.25"
    }
    # when
    result = Measurement.from_json(json_data)
    # then
    assert result is not None
    assert result.value == 1.25
    assert isinstance(result.created_at, datetime)


def test_sensor_from_json():
    # given
    json_data = {
        "title": "Temperatur",
        "unit": "°C",
        "sensorType": "Wetterstation",
        "icon": "osem-thermometer",
        "_id": "61e6c8ffac538c001b9f4bf1",
        "lastMeasurement": {
            "createdAt": "2024-01-17T16:09:36.045Z",
            "value": "-2.27"
        }
    }
    # when
    result = Sensor.from_json(json_data)
    # then
    assert result is not None
    assert result.title == "Temperatur"
    assert result.id == "61e6c8ffac538c001b9f4bf1"
    assert result.last_measurement is not None
    assert result.last_measurement.value == -2.27
