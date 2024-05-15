#!/usr/bin/env python3
"""
This module provides a Cache class for managing caching using Redis.
"""

import redis
import uuid
from typing import Union, Callable, Optional, Any
from functools import wraps


def replay(method: Callable) -> None:
    """
    Displays the history of calls of a particular function
    """
    name = method.__qualname__
    client = redis.Redis()
    inputs = client.lrange("{}:inputs".format(name), 0, -1)
    outputs = client.lrange("{}:outputs".format(name), 0, -1)
    print('{} was called {} times:'.format(name, len(inputs)))
    for input, output in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(name, input.decode("utf-8"),
                                     output.decode("utf-8")))


def count_calls(method: Callable) -> Callable:
    """Decorator to count how many times a method is called."""

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    '''
        stores the history of inputs and outputs for a particular function
    '''
    key: str = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):  # sourcery skip: avoid-builtin-shadow
        """ Wrapper for decorator functionality """
        self._redis.rpush(inputs, str(args))
        data = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(data))
        return data

    return wrapper


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

    def get(self, key: str, fn: Callable = None) -> \
            Union[str, bytes, int, float, None]:
        """Retrieve data from the cache.

        Args:
            key (str): The key under which the data is stored.
            fn (Callable, optional): A callable function to convert
            the data back to the desired format.

        Returns:
            Union[str, bytes, int, float, None]: The retrieved data.
        """
        data = self._redis.get(key)
        if data is not None and fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Union[str, None]:
        """Retrieve string data from the cache.

        Args:
            key (str): The key under which the string data is stored.

        Returns:
            Union[str, None]: The retrieved string data.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """Retrieve integer data from the cache.

        Args:
            key (str): The key under which the integer data is stored.

        Returns:
            Union[int, None]: The retrieved integer data.
        """
        return self.get(key, fn=int)
