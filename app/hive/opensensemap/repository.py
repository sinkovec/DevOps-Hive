"""
Repository module for OpenSenseMap sense boxes.

This module defines 
    - the SenseBoxRepository class, which serves as a repository to
      interact with both the OpenSenseMap API.
    - the CachingRepository class, which caches results of repository
      delegate into a Redis cache.
"""
from typing import Type, TypeVar
from datetime import datetime, timezone, timedelta
import json

from redis import Redis

from .client import OpenSenseMapClient
from .model import CachedEntity, SenseBox


class SenseBoxRepository:
    """
    Repository to interact with OpenSenseMap API to retrieve sense boxes.
    """

    def __init__(self, client: OpenSenseMapClient):
        self.client = client
        self.sense_box_ids = []

    def find_all(self):
        """
        Find all sense boxes based on given sense box ids.
        """
        return [self.find(sense_box_id) for sense_box_id in self.sense_box_ids]

    def find(self, sense_box_id):
        """
        Find sense box on given id.
        """
        data = self.client.fetch_sense_box(sense_box_id)
        if data:
            data = SenseBox(**data)
        return data


class CachingRepository:
    """
    Decorator repository to cache results of the delegated repository in Redis.
    """

    T = TypeVar("T")

    def __init__(
        self,
        delegate: SenseBoxRepository,
        entity_type: Type[T],
        redis: Redis,
        refresh_after: timedelta = timedelta(minutes=5),
    ):
        self.delegate = delegate
        self.entity_type = entity_type
        self.redis = redis
        self.refresh_after = refresh_after

    def find_all(self):
        """
        Finds all results. First, Redis cache is checked.
        If there is not current result, then delegates `find_all` method is invoked.
        The result is then cached / saved.
        """
        cache_key = self._cache_key_find_all()
        cache = self.redis.get(cache_key)

        if cache:
            entity_ids = json.loads(cache)
            data = [self.find(entity_id) for entity_id in entity_ids]
        else:
            data = self.delegate.find_all()
            entity_ids = [self._cache_entity(entity) for entity in data]
            self.redis.set(
                cache_key, json.dumps(entity_ids), ex=timedelta(minutes=30).seconds
            )

        return data

    def find(self, entity_id):
        """
        Finds result based on given id.
        Results are cached in Redis.
        """
        cache = self.redis.get(entity_id)
        should_recompute = True

        if cache:
            cache = CachedEntity(**json.loads(cache))
            entity = self.entity_type(**cache.entity)
            should_recompute = (
                cache.last_modified < datetime.now(timezone.utc) - self.refresh_after
            )

        if should_recompute:
            entity = self.delegate.find(entity_id)
            if entity:
                self._cache_entity(entity)

        return entity

    def _cache_entity(self, entity):
        """
        Stores the entity in Redis cache.
        """
        cache = CachedEntity(
            last_modified=datetime.now(timezone.utc),
            entity=entity.model_dump(),
        )
        self.redis.set(entity.id, json.dumps(cache.model_dump(), default=str))
        return entity.id

    def last_modified_all(self):
        """
        Returns the last_modified timestamp of all entites stored in Redis.
        """
        cache_key = self._cache_key_find_all()
        data = self.redis.get(cache_key)
        if data:
            entity_ids = json.loads(data)
            return [self.last_modified(entity_id) for entity_id in entity_ids]
        return []

    def last_modified(self, entity_id):
        """
        Returns the last_modified timestamp of the entity for the given id.
        """
        data = self.redis.get(entity_id)
        return CachedEntity(**json.loads(data)).last_modified if data else None

    def _cache_key_find_all(self):
        return type(self.delegate).__qualname__ + "_find_all"
