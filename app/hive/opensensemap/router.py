"""
Module for handling temperature-related API endpoints.

This module defines an API endpoint to calculate and 
return the average temperature of sense box sensors.

Endpoints:
    - GET /temperature: Endpoint to calculate and 
        return the average temperature of sense box sensors.

"""
from fastapi import APIRouter

from .config import service

router = APIRouter()

@router.get("/temperature")
def read_temperature():
    """
    GET method to calculate and return the average temperature of sense box sensors.

    Returns:
        dict: Dictionary containing "status" and "temperature" keys.
    """
    avg_temperature = service.get_average_temperature()
    return {
        "status": service.temperature_status(avg_temperature),
        "temperature": avg_temperature
    }
