"""
Module to define common models used when interacting with OpenSenseMap.
"""
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Measurement:
    """
    Represents an OpenSenseMap Measurements.
    Measurements are emitted by Sensors.
    """

    created_at: datetime
    value: float

    @classmethod
    def from_json(cls, json_data):
        """
        Factory method to create a Measurement instance from a Json object.
        """
        return cls(
            created_at=datetime.fromisoformat(json_data["createdAt"]),
            value=float(json_data["value"]),
        )


@dataclass
class Sensor:
    """
    Represents an OpenSenseMap Sensor.
    A sensor is identifable and emits measurements of a specific type, e.g., temperature.
    """

    sensor_id: str
    title: str
    last_measurement: Measurement

    @classmethod
    def from_json(cls, json_data):
        """
        Factory method to create a Sensor instance from a Json object.
        """
        return cls(
            sensor_id=json_data["_id"],
            title=json_data["title"],
            last_measurement=Measurement.from_json(json_data["lastMeasurement"]),
        )


@dataclass
class SensorCache:
    """
    Represents an OpenSeseMap Sensor stored in cache.
    """

    created_at: datetime
    content: dict

    @classmethod
    def from_json(cls, json_data):
        """
        Factory method to create a Sensor cache instance from a Json object.
        """
        return cls(
            datetime.fromisoformat(json_data["created_at"]),
            content=json_data["content"],
        )
