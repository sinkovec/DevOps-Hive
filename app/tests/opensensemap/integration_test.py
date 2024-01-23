"""
Module: test_open_sense_map_api.py

This module contains integration tests for the OpenSenseMap API endpoint in the hive.app module.
"""
from datetime import datetime, timezone
from unittest.mock import Mock
import json

from fastapi.testclient import TestClient
from testcontainers.redis import RedisContainer
import pytest

from hive.app import app
from hive.opensensemap.di import get_redis, get_dao

client = TestClient(app)
redis = RedisContainer()


@pytest.fixture(autouse=True)
def setup(request):
    """
    Setup Redis testcontainer and supply client to app.
    """
    redis.start()

    def stop():
        redis.stop()

    request.addfinalizer(stop)

    def get_redis_client():
        return redis.get_client()

    def get_mock_dao():
        mock_dao = Mock()
        mock_dao.load_sense_box_sensor_ids.return_value = [
            ("a", "1"), ("b", "2"), ("c", "3")
        ]
        return mock_dao

    app.dependency_overrides[get_redis] = get_redis_client
    app.dependency_overrides[get_dao] = get_mock_dao


def fake_sensor_data(sensor_id):
    """
    Fixture to provide fake sensor data for testing.

    Returns:
        dict: Dictionary representing fake sensor data.
    """
    return json.dumps(
        {
            "_id": sensor_id,
            "title": "Sensor title",
            "lastMeasurement": {
                "createdAt": datetime.now(timezone.utc).isoformat(),
                "value": "10",
            },
        }
    )

def test_temperature(mocker):
    """
    Test the temperature endpoint of the hive app.

    Checks if the temperature endpoint returns the expected result based on fake sensor data.

    Args:
        mocker: Pytest mocker fixture for mocking requests lib.
    """
    # given
    fake_resp = mocker.Mock()
    fake_resp.content = fake_sensor_data(1)
    fake_resp.status_code = 200

    mocker.patch("hive.opensensemap.api.requests.get", return_value=fake_resp)

    # when
    response = client.get("/temperature")

    # then
    assert response.status_code == 200
    content = response.json()
    assert content["status"] == "Good"
    assert content["temperature"] == 10


def test_readyz_success(mocker):
    # given
    fake_resp = mocker.Mock()
    fake_resp.status_code = 200

    mocker.patch("hive.opensensemap.api.requests.head", return_value=fake_resp)

    # when
    response = client.head("/readyz")
    # then
    assert response.status_code == 200


def test_readyz_failed(mocker):
    # given
    fake_resp = mocker.Mock()
    fake_resp.status_code = 404

    mocker.patch("hive.opensensemap.api.requests.head", return_value=fake_resp)

    # when
    response = client.head("/readyz")
    # then
    assert response.status_code == 503


def test_readyz_success_cache(mocker):
    # given
    fake_resp = mocker.Mock()
    fake_resp.status_code = 404

    mocker.patch("hive.opensensemap.api.requests.head", return_value=fake_resp)

    redis.get_client().set("opensensemap_a_1", fake_sensor_data(1), ex=3600)

    # when
    response = client.head("/readyz")
    # then
    assert response.status_code == 200
