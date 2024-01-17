"""
Module to define common models used when interacting with OpenSenseMap.
"""


class SenseBox:
    """
    Represents an OpenSenseMap Sense Box.
    A Sense Box is identifiable, named and consists of mulitple sensors.
    """

    def __init__(self, id, name, sensors):
        self.id = id
        self.name = name
        self.sensors = sensors


class Sensor:
    """
    Represents an OpenSenseMap Sensor.
    A sensor is identifable and emits measurements of a specific type, e.g., temperature.
    """

    def __init__(self, id, title):
        self.id = id
        self.title = title


class Measurement:
    """
    Represents an OpenSenseMap Measurements.
    Measurements are emitted by Sensors.
    """

    def __init__(self, location, created_at, value):
        self.location = location
        self.created_at = created_at
        self.value = value

    @classmethod
    def from_json(cls, json_data):
        """
        Factory method to create a Measurement instance from a Json object.
        """
        return cls(
            location=json_data["location"],
            created_at=json_data["createdAt"],
            value=float(json_data["value"])
        )
