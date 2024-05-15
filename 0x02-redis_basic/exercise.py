#!/usr/bin/env python3
"""
Cache module
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
    '''
        Counts the number of times a method is called.
    '''

    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        '''
            Wrapper function.
        '''
        key: str = method.__qualname__
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
    def __init__(self) -> None:
        """store an instance of the Redis and flush the instance"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ takes a data argument and returns a string """
        key: str = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[bytes, None]:
        """ used to convert the data back to the desired format """
        value: bytes = self._redis.get(key)
        if value is None:
            return None
        if fn is not None:
            return fn(value)
        return value

    def get_str(self, key: str) -> Optional[str]:
        """parametrizes Cache.get with the correct conversion function"""
        return self.get(key, lambda x: x.decode('utf-8') if x else None)

    def get_int(self, key: int) -> Optional[int]:
        """parametrizes Cache.get with the correct conversion function"""
        return self.get(key, fn=int)
