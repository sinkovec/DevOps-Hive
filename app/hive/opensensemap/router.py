"""
Module for handling temperature-related API endpoints.

This module defines an API endpoint to calculate and 
return the average temperature of sense box sensors.

Endpoints:
    - GET /temperature: Endpoint to calculate and 
        return the average temperature of sense box sensors.

"""
import json
from fastapi import APIRouter
from redis import Redis

from .config import service

redis = Redis(host="localhost", port=6379)
router = APIRouter()

@router.get("/temperature")
def read_temperature():
    """
    GET method to calculate and return the average temperature of sense box sensors.

    Returns:
        dict: Dictionary containing "status" and "temperature" keys.
    """
    data = get_cache()

    if not data:
        data = create_response()
        set_cache(data)

    return data

def create_response():
    """
    Creates a response containing the status and average temperature.

    Returns:
        dict: Dictionary containing "status" and "temperature" keys.
    """
    avg_temperature = service.calculate_average_temperature()
    return {
        "status": service.temperature_status(avg_temperature),
        "temperature": avg_temperature
    }

def get_cache():
    """
    Retrieves cached data from Redis.

    Returns:
        dict: Dictionary containing cached data or None if not found.
    """
    data = redis.get("opensensemap_temperature")
    if data:
        data = json.loads(data)
    return data

def set_cache(data):
    """
    Sets data into the Redis cache.

    Args:
        data: Data to be stored in the cache.
    """
    redis.set("opensensemap_temperature", json.dumps(data), ex=120)
