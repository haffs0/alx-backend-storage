#!/usr/bin/env python3
"""Redis basic"""
import redis
import uuid
from typing import Union


class Cache:
    """Represent an object for storing data"""
    def __init__(self) -> None:
        """initializes a Cache instance."""
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """stores a value in redis and return the key."""
        data_key = str(uuid.uuid4())
        self._redis.set(data_key, data)
        return (data_key)
