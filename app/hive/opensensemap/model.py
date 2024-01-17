"""
Module to define common models used when interacting with OpenSenseMap.
"""
from datetime import datetime

class Sensor:
    """
    Represents an OpenSenseMap Sensor.
    A sensor is identifable and emits measurements of a specific type, e.g., temperature.
    """

    def __init__(self, id, title, last_measurement):
        self.id = id
        self.title = title
        self.last_measurement = last_measurement

    @classmethod
    def from_json(cls, json_data):
        """
        Factory method to create a Sensor instance from a Json object.
        """
        return cls(
            id=json_data["_id"],
            title=json_data["title"],
            last_measurement=Measurement.from_json(json_data["lastMeasurement"])
        )

class Measurement:
    """
    Represents an OpenSenseMap Measurements.
    Measurements are emitted by Sensors.
    """

    def __init__(self, created_at, value):
        self.created_at = created_at
        self.value = value

    @classmethod
    def from_json(cls, json_data):
        """
        Factory method to create a Measurement instance from a Json object.
        """
        return cls(
            created_at=datetime.fromisoformat(json_data["createdAt"]),
            value=float(json_data["value"])
        )
