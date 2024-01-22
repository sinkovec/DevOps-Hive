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

from .di import get_service
from .service import OpenSenseMapService

router = APIRouter()


@router.get("/temperature")
def read_temperature(service: Annotated[OpenSenseMapService, Depends(get_service)]):
    """
    GET method to calculate and return the average temperature of sense box sensors.

    Returns:
        dict: Dictionary containing "status" and "temperature" keys.
    """
    avg_temperature = service.get_average_temperature()
    return {
        "status": service.temperature_status(avg_temperature),
        "temperature": avg_temperature,
    }
