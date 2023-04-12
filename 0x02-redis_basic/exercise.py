#!/usr/bin/env python3
"""Redis basic"""
import redis
import uuid
from typing import Union, Callable, Any
from functools import wraps


def call_history(method: Callable) -> Callable:
    """tracks call details of method in Cache class"""
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        """return the output and store its input"""
        in_key = '{}:inputs'.format(method.__qualname__)
        out_key = '{}:outputs'.format(method.__qualname__)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(in_key, str(args))
        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(out_key, output)
        return output
    return invoker


def count_calls(method: Callable) -> Callable:
    """count the number of calls made on the method"""
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        """invoker the method"""
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return invoker


class Cache:
    """Represent an object for storing data"""
    def __init__(self) -> None:
        """initializes a Cache instance."""
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """stores a value in redis and return the key."""
        data_key = str(uuid.uuid4())
        self._redis.set(data_key, data)
        return (data_key)

    def get(
            self,
            key: str,
            fn: Callable = None
            ) -> Union[str, bytes, int, float]:
        """REtrieves data from redis storage"""
        data = self._redis.get(key)
        return fn(data) if fn is not None else data

    def get_str(self, key: str) -> str:
        """return a string value from redis"""
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """return a integer value from redis storage"""
        return self.get(key, lambda x: int(x))
