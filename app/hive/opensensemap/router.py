"""
Module for handling temperature-related API endpoints.

This module defines an API endpoint to calculate and 
return the average temperature of sense box sensors.

Endpoints:
    - GET /temperature: Endpoint to calculate and 
        return the average temperature of sense box sensors.

"""
from typing import Annotated
from fastapi import APIRouter, Depends
from prometheus_client import Gauge
from redis import Redis

from .di import get_service, get_repository, get_redis
from .service import OpenSenseMapService
from .repository import OpenSenseMapRepository

router = APIRouter()
temperature_metric = Gauge(
        "temperature_average",
        "Average temperature emitted by OpenSenseMap sensors",
        namespace="opensensemap",
    )


@router.get("/temperature")
def read_temperature(service: Annotated[OpenSenseMapService, Depends(get_service)]):
    """
    GET method to calculate and return the average temperature of sense box sensors.

    Returns:
        dict: Dictionary containing "status" and "temperature" keys.
    """
    avg_temperature = service.calculate_average_temperature()
    temperature_metric.set(avg_temperature)
    return {
        "status": service.temperature_status(avg_temperature),
        "temperature": avg_temperature,
    }
