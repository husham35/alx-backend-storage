#!/usr/bin/env python3
""" exercise module """
from functools import wraps
import redis
from typing import Callable, Optional, Union
import uuid


def call_history(method: Callable) -> Callable:
    """
    A decorator of a wrapper function to record input output history
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function
        """
        method_name = method.__qualname__
        self._redis.rpush(method_name + ":inputs", str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(method_name + ":outputs", output)
        return output

    return wrapper


def count_calls(method: Callable) -> Callable:
    """
    A decorator to a wrapper function to count number of times a it was called
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function
        """
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)

    return wrapper


def replay(method: Callable) -> None:
    """
    A function to display the history of calls of a particular function.
    """
    method_name = method.__qualname__
    redis_db = method.__self__._redis
    inputs = redis_db.lrange(method_name + ":inputs", 0, -1)
    outputs = redis_db.lrange(method_name + ":outputs", 0, -1)

    print(f"{method_name} was called {len(inputs)} times:")
    for input, output in zip(inputs, outputs):
        input = input.decode("utf-8")
        output = output.decode("utf-8")
        print(f"{method_name}(*{input}) -> {output}")


class Cache:
    """
    A Cache class that makes use of redis to store and retrieve data
    """

    def __init__(self) -> None:
        """
        Initializes a redis store
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores data to the redis store using a uuid key and returns the
        key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(
        self,
        key: str,
        fn: Optional[Callable] = None
    ) -> Union[str, bytes, int, float, None]:
        """
        Returns retrived data by converting it to its original data type based
        based on the function fn. if the key is not found, it returns None
        """
        val = self._redis.get(key)
        if val is not None and fn is not None:
            val = fn(val)
        return val

    def get_int(self, key: str) -> Union[int, None]:
        """
        Returns retrieved value stored in redis store at the key as an integer
        """
        return self.get(key, int)

    def get_str(self, key: str) -> Union[str, None]:
        """
        Returns retrieved value stored in redis store at the key as string
        """
        return self.get(key, str)
