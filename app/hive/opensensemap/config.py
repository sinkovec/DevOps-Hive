"""
Module for configuring the OpenSenseMap API components.

This module initializes and configures the various components of the OpenSenseMap API, including
the API router, OpenSenseMap API instance, data access object (DAO), repository, and service.

Components:
    - api: Instance of OpenSenseMapApi for handling API requests.
    - dao: Instance of OpenSenseMapDao for data access to the OpenSenseMap database.
    - repository: Instance of OpenSenseMapRepository for interaction with the API and database.
    - service: Instance of OpenSenseMapService for calculating average temperatures.
    - router: FastAPI router instance for defining API routes.

Configuration:
    - OPEN_SENSE_MAP_API_BASE_URL (str): Base URL for the OpenSenseMap API.
"""
from redis import Redis
from hive.config import settings
from .api import OpenSenseMapApi
from .dao import OpenSenseMapDao
from .repository import OpenSenseMapRepository
from .service import OpenSenseMapService

OPEN_SENSE_MAP_API_BASE_URL = "https://api.opensensemap.org"

api = OpenSenseMapApi(OPEN_SENSE_MAP_API_BASE_URL)
dao = OpenSenseMapDao()
repository = OpenSenseMapRepository(api, dao)
redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
service = OpenSenseMapService(redis, repository)
