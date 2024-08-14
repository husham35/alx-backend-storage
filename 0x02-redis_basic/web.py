#!/usr/bin/env python3
"""
A module that uses the requests module to obtain the HTML content of a
particular URL and returns it.
"""

from functools import wraps
import redis
import requests
from typing import Callable


redis_store = redis.Redis()


def data_cacher(method: Callable) -> Callable:
    """
    A wrapper function that caches the output of fetched data.
    """
    @wraps(method)
    def invoker(url) -> str:
        """
        A wrapper function for caching the output.
        """
        # redis_store.incr(f'count:{url}')
        # result = redis_store.get(f'result:{url}')
        
        # if result:
        #     return result.decode('utf-8')

        # result = method(url)
        # redis_store.set(f'count:{url}', 0)
        # redis_store.setex(f'result:{url}', 10, result)
        # return result
        
        key = "count:{}".format(url)
        value = "cached:{}".format(url)

        redis_store.incr(key)
        cache = redis_store.get(value)

        if cache:
            return cache.decode('utf-8')

        html = method(url)
        redis_store.set(key, 0)
        redis_store.setex(value, 10, html)
        return html

    return invoker


@data_cacher
def get_page(url: str) -> str:
    """
    Returns the HTML content of a particular URL
    """
    return requests.get(url).text
