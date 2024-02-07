"""
Module for configuring the OpenSenseMap API components.

This module initializes and configures the various components of the OpenSenseMap API client,
repository, and service.

Components:
    - client: Instance of OpenSenseMapClient for handling API requests.
    - redis: Instance of Redis to cache entities.
    - caching_repository: Instance of CachingRepository to cache OpenSenseMapRepository results.
    - repository: Instance of OpenSenseMapRepository for interaction with the API and database.
    - service: Instance of OpenSenseMapTemperatureService for calculating average temperatures.
    - availability_service: Instance of OpenSenseMapAvailabilityService for requesting availability

Configuration:
    - OPEN_SENSE_MAP_API_BASE_URL (str): Base URL for the OpenSenseMap API.
"""
from typing import Annotated
from fastapi import Depends
from redis import Redis

from hive.config import settings
from .model import SenseBox
from .client import OpenSenseMapClient
from .repository import SenseBoxRepository, CachingRepository
from .service import OpenSenseMapTemperatureService, OpenSenseMapAvailabilityService

OPEN_SENSE_MAP_API_BASE_URL = "https://api.opensensemap.org"


def get_redis():
    """
    Creates Redis instance.
    """
    return Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)


def get_client():
    """
    Creates OpenSenseMapClient instance.
    """
    return OpenSenseMapClient(OPEN_SENSE_MAP_API_BASE_URL)


def get_repository(client: Annotated[OpenSenseMapClient, Depends(get_client)]):
    """
    Creates SenseBoxRepository instance.
    """
    repository = SenseBoxRepository(client)
    repository.sense_box_ids = [
        sense_box_id.strip() for sense_box_id in settings.SENSE_BOX_IDS.split(",")
    ]
    return repository


def get_caching_repository(
    delegate: Annotated[SenseBoxRepository, Depends(get_repository)],
    redis: Annotated[Redis, Depends(get_redis)],
):
    """
    Creates CachingRepository instance.
    """
    return CachingRepository(delegate, SenseBox, redis)


def get_service(
    repository: Annotated[CachingRepository, Depends(get_caching_repository)],
):
    """
    Creates OpenSenseMapTemperatureService instance.
    """
    return OpenSenseMapTemperatureService(repository)


def get_availability_service(
    repository: Annotated[SenseBoxRepository, Depends(get_repository)],
    caching_repository: Annotated[CachingRepository, Depends(get_caching_repository)],
):
    """
    Creates OpenSenseMapAvailabilityService instance.
    """
    return OpenSenseMapAvailabilityService(repository, caching_repository)
