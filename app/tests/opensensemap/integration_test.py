"""
Module: test_open_sense_map_api.py

This module contains integration tests for the OpenSenseMap API endpoint in the hive.app module.
"""
from datetime import datetime, timezone
import json

from fastapi.testclient import TestClient
from testcontainers.redis import RedisContainer
import pytest

from hive.app import app
from hive.opensensemap.di import get_redis

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

    app.dependency_overrides[get_redis] = get_redis_client


def fake_sense_box_data():
    """
    Fixture to provide fake sensor data for testing.

    Returns:
        dict: Dictionary representing fake sensor data.
    """
    return {
        "_id": "a",
        "name": "fake-sense-box",
        "sensors": [
            {
                "_id": "1",
                "title": "Temperatur",
                "lastMeasurement": {
                    "createdAt": datetime.now(timezone.utc).isoformat(),
                    "value": "10",
                },
            }
        ],
    }


def test_temperature(mocker):
    """
    Test the temperature endpoint of the hive app.

    Checks if the temperature endpoint returns the expected result based on fake sensor data.

    Args:
        mocker: Pytest mocker fixture for mocking requests lib.
    """
    # given
    fake_resp = mocker.Mock()
    fake_resp.json.return_value = fake_sense_box_data()
    fake_resp.status_code = 200

    mocker.patch("hive.opensensemap.client.requests.get", return_value=fake_resp)

    # when
    response = client.get("/temperature")

    # then
    assert response.status_code == 200
    content = response.json()
    assert content["status"] == "Good"
    assert content["temperature"] == 10


def test_readyz_success(mocker):
    """
    Test the readyz endpoint of the hive app.

    Checks if the readyz endpoint returns OK response when sensors are available.

    Args:
        mocker: Pytest mocker fixture for mocking requests lib.
    """
    # given
    fake_resp = mocker.Mock()
    fake_resp.status_code = 200
    fake_resp.json.return_value = fake_sense_box_data()

    mocker.patch("hive.opensensemap.client.requests.get", return_value=fake_resp)

    # when
    response = client.get("/readyz")
    # then
    assert response.status_code == 200


def test_readyz_failed(mocker):
    """
    Test the readyz endpoint of the hive app.

    Checks if the readyz endpoint returns Service Unavailable response
    when sensors are not available and caching content is missing.

    Args:
        mocker: Pytest mocker fixture for mocking requests lib.
    """
    # given
    fake_resp = mocker.Mock()
    fake_resp.status_code = 404

    mocker.patch("hive.opensensemap.client.requests.get", return_value=fake_resp)

    # when
    response = client.get("/readyz")
    # then
    assert response.status_code == 503


def test_readyz_success_cache(mocker):
    """
    Test the readyz endpoint of the hive app.

    Checks if the readyz endpoint returns OK response
    when sensors are not available but caching content is present.

    Args:
        mocker: Pytest mocker fixture for mocking requests lib.
    """
    # given
    fake_resp = mocker.Mock()
    fake_resp.status_code = 404

    mocker.patch("hive.opensensemap.client.requests.get", return_value=fake_resp)

    fake_cache = json.dumps(
        {
            "last_modified": datetime.now(timezone.utc).isoformat(),
            "entity": fake_sense_box_data(),
        }
    )
    redis.get_client().set("a", fake_cache)
    redis.get_client().set("SenseBoxRepository_find_all", json.dumps(["a"]))

    # when
    response = client.get("/readyz")
    # then
    assert response.status_code == 200
