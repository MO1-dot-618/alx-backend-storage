#!/usr/bin/env python3
"""
This module provides a Cache class for managing caching using Redis.
"""

import redis
import uuid
from typing import Union


class Cache:
    """A class to manage caching using Redis."""

    def __init__(self):
        """Initialize the Cache instance and connect to Redis."""
        self._redis = redis.Redis()
        self._redis.flushdb()
    
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in the cache.

        Args:
            data: The data to be stored. Can be a str, bytes, int, or float.

        Returns:
            str: The key under which the data is stored in the cache.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return (key)
