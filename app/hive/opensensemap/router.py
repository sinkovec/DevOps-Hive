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

from .di import get_service, get_availability_service
from .service import OpenSenseMapTemperatureService, OpenSenseMapAvailabilityService
from .schemas import TemperatureBase

router = APIRouter()
temperature_metric = Gauge(
    "temperature_average",
    "Average temperature emitted by OpenSenseMap sensors",
    namespace="opensensemap",
)


@router.get("/temperature")
def read_temperature(
    service: Annotated[OpenSenseMapTemperatureService, Depends(get_service)]
) -> TemperatureBase:
    """
    GET method to calculate and return the average temperature of sense box sensors.

    Returns:
        TemperatureBase: object containing "status" and "temperature" keys.
    """
    result = service.get_temperature()
    temperature_metric.set(result.temperature)
    return result


@router.get("/readyz")
def head_readyz(
    service: Annotated[
        OpenSenseMapAvailabilityService, Depends(get_availability_service)
    ]
):
    """
    Readiness probe that returns an OK response unless
    - 50% + 1 sensors are not accessible AND
    - caching content does not expire within 5 minutes.

    Returns:
        Response: containing status_code for readiness probe.
    """
    if service.is_available():
        status_code = 200
    else:
        status_code = 503  # service unavailable
    return Response(status_code=status_code)
