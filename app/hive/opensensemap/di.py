"""
Module for configuring the OpenSenseMap API components.

This module initializes and configures the various components of the OpenSenseMap API, including
the API router, OpenSenseMap API instance, data access object (DAO), repository, and service.

Components:
    - api: Instance of OpenSenseMapApi for handling API requests.
    - dao: Instance of OpenSenseMapDao for data access to the OpenSenseMap database.
    - redis: Instance of Redis to cache service results.
    - repository: Instance of OpenSenseMapRepository for interaction with the API and database.
    - service: Instance of OpenSenseMapService for calculating average temperatures.
    - router: FastAPI router instance for defining API routes.

Configuration:
    - OPEN_SENSE_MAP_API_BASE_URL (str): Base URL for the OpenSenseMap API.
"""
from typing import Annotated
from fastapi import Depends
from redis import Redis
from hive.config import settings
from .client import OpenSenseMapClient
from .dao import OpenSenseMapDao
from .repository import OpenSenseMapRepository
from .service import OpenSenseMapService

OPEN_SENSE_MAP_API_BASE_URL = "https://api.opensensemap.org"


def get_redis():
    """
    Creates Redis instance.
    """
    return Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)


def get_api():
    """
    Creates OpenSenseMapApi instance.
    """
    return OpenSenseMapClient(OPEN_SENSE_MAP_API_BASE_URL)


def get_dao():
    """
    Creates OpenSenseMapDao instance.
    """
    return OpenSenseMapDao()


def get_repository(
    api: Annotated[OpenSenseMapClient, Depends(get_api)],
    dao: Annotated[OpenSenseMapDao, Depends(get_dao)],
    redis: Annotated[Redis, Depends(get_redis)],
):
    """
    Creates OpenSenseMapRepository instance.
    """
    return OpenSenseMapRepository(api, dao, redis)


def get_service(
    repository: Annotated[OpenSenseMapRepository, Depends(get_repository)],
):
    """
    Creates OpenSenseMapService instance.
    """
    return OpenSenseMapService(repository)
