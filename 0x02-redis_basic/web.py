#!/usr/bin/env python3
"""get page function implementation"""
import requests
import redis
from functools import wraps
from typing import Callable


# redis instance
redis_store = redis.Redis()


def cache(func: Callable) -> Callable:
    """Caches output of fetched data"""
    @wraps(func)
    def invoker(url) -> str:
        """wrapper function"""
        redis_store.incr('count:{}'.format(url))
        result = redis_store.get('result:{}'.format(url))
        if result:
            return result.decode('utf-8')
        result = method(url)
        redis_store.set('count:{}'.format(url), 0)
        redis_store.setex('result:{}'.format(url), 10, result)
        return result
    return invoker


@cache
def get_page(url: str) -> str:
    """return HTML content from url"""
    return requests.get(url).text
