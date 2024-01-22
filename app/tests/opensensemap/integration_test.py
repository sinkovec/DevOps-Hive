"""
Module: test_open_sense_map_api.py

This module contains integration tests for the OpenSenseMap API endpoint in the hive.app module.
"""
from datetime import datetime, timezone
from fastapi.testclient import TestClient
from testcontainers.redis import RedisContainer
import pytest

from hive.app import app

client = TestClient(app)
redis = RedisContainer()

@pytest.fixture(scope="module", autouse=True)
def setup(request):
    redis.start()

    def stop():
        redis.stop()

    request.addfinalizer(stop)


@pytest.fixture(name="fake_sensor_data")
def fixture_fake_sensor_data():
    """
    Fixture to provide fake sensor data for testing.

    Returns:
        dict: Dictionary representing fake sensor data.
    """
    return {
        "_id": "1",
        "title": "Sensor title",
        "lastMeasurement": {
            "createdAt": datetime.now(timezone.utc).isoformat(),
            "value": "10"
        }
    }


def test_temperature(mocker, fake_sensor_data):
    """
    Test the temperature endpoint of the hive app.

    Checks if the temperature endpoint returns the expected result based on fake sensor data.

    Args:
        mocker: Pytest mocker fixture for mocking requests lib.
        fake_sensor_data: Fake sensor data provided by the fixture.
    """
    # given
    fake_resp = mocker.Mock()
    fake_resp.json.return_value = fake_sensor_data
    fake_resp.status_code = 200

    mocker.patch("hive.opensensemap.api.requests.get", return_value=fake_resp)
    mocker.patch("hive.opensensemap.config.service.redis", redis.get_client())

    # when
    response = client.get("/temperature")

    # then
    assert response.status_code == 200
    content = response.json()
    assert content["status"] == "Good"
    assert content["temperature"] == 10
