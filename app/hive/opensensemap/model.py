"""
Module to define common models used when interacting with OpenSenseMap.
"""
from typing import Annotated, List
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class Measurement(BaseModel):
    """
    Represents an OpenSenseMap Measurements.
    Measurements are emitted by Sensors.
    """

    model_config = ConfigDict(populate_by_name=True)

    created_at: Annotated[datetime, Field(alias="createdAt")]
    value: float


class Sensor(BaseModel):
    """
    Represents an OpenSenseMap Sensor.
    A sensor is identifable and emits measurements of a specific type, e.g., temperature.
    """

    model_config = ConfigDict(populate_by_name=True)

    id: Annotated[str, Field(alias="_id")]
    title: str
    last_measurement: Annotated[Measurement, Field(alias="lastMeasurement")]


class SenseBox(BaseModel):
    """
    Represents an OpenSenseMap Sense Box.
    A Sense Box is identifiable and consists of several sensors.
    """

    model_config = ConfigDict(populate_by_name=True)

    id: Annotated[str, Field(alias="_id")]
    name: str
    sensors: List[Sensor]


class CachedEntity(BaseModel):
    """
    Represents a cached entity.
    """

    last_modified: datetime
    entity: dict
