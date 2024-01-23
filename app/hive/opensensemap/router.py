"""
Module for handling temperature-related API endpoints.

This module defines an API endpoint to calculate and 
return the average temperature of sense box sensors.

Endpoints:
    - GET /temperature: Endpoint to calculate and 
        return the average temperature of sense box sensors.

"""
from typing import Annotated
from fastapi import APIRouter, Depends, Response
from prometheus_client import Gauge

from .di import get_service
from .service import OpenSenseMapService
from .schemas import TemperatureBase

router = APIRouter()
temperature_metric = Gauge(
    "temperature_average",
    "Average temperature emitted by OpenSenseMap sensors",
    namespace="opensensemap",
)


@router.get("/temperature")
def read_temperature(
    service: Annotated[OpenSenseMapService, Depends(get_service)]
) -> TemperatureBase:
    """
    GET method to calculate and return the average temperature of sense box sensors.

    Returns:
        TemperatureBase: object containing "status" and "temperature" keys.
    """
    return service.get_temperature()


@router.get("/readyz")
def head_readyz(service: Annotated[OpenSenseMapService, Depends(get_service)]):
    """
    Readiness probe that returns an OK response unless
    - 50% + 1 sensors are not accessible AND
    - caching content does not expire within 5 minutes.

    Returns:
        Response: containing status_code for readiness probe.
    """
    if service.sensor_data_available():
        status_code = 200
    else:
        status_code = 503  # service unavailable
    return Response(status_code=status_code)
