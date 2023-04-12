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


def replay(func: Callable) -> None:
    """Print call history of Cache class method"""
    if fn is None or not hasattr(func, '__self__'):
        return
    redis_store = getattr(func.__self__, 'redis', None)
    if not isinstance(redis_store, redis.Redis):
        return
    func_name = func.__qualname__
    in_key = '{}:inputs'.format(func_name)
    out_key = '{}:outputs'.format(func_name)
    func_call_count = 0
    if redis_store.exits(func_name) != 0:
        func_call_count = int(redis_store.get(func_name))
    print('{} was called {} times:'.format(func_name, func_call_count))
    func_inputs = redis_store.lrange(in_key, 0, -1)
    func_outputs = redis_store.lrange(out_key, 0, -1)
    for func_input, func_output in zip(func_inputs, func_outputs):
        print('{}(*{}) -> {}'.format(
            func_name,
            func_input.decode("utf-8"),
            func_output,
        ))


class Cache:
    """Represent an object for storing data"""
    def __init__(self) -> None:
        """initializes a Cache instance."""
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @call_history
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
