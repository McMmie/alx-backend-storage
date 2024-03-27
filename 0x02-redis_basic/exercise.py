#!/usr/bin/env python3
"""
This module shows how to use redis in python
"""
import redis
from typing import Union, Callable, Optional
import uuid
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number of times a method is called.
    """
    @wraps(method)
    def wrapper(self, *args, **kwds):
        """
        """
        key_name = method.__qualname__
        self._redis.incr(key_name)
        return method(self, *args, **kwds)

    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator to track input-output history of a method."""

    @wraps(method)
    def wrapper(self, *args, **kwds):
        """
        """
        _key = method.__qualname__
        outpt = _key + ":outputs"
        inpt = _key + ":inputs"
        data = str(args)
        self._redis.rpush(inpt, data)
        results = method(self, *args, **kwds)
        self._redis.rpush(outpt, str(results))

        return results

    return wrapper


def replay(func: Callable):
    """Function to replay the history of method calls stored in Redis."""

    r = redis.Redis()
    key_m = func.__qualname__
    inp_m = r.lrange("{}:inputs".format(key_m), 0, -1)
    outp_m = r.lrange("{}:outputs".format(key_m), 0, -1)
    calls_number = len(inp_m)
    times_str = 'times' if calls_number != 1 else 'time'

    print('{} was called {} {}:'.format(key_m, calls_number, times_str))

    for i, j in zip(inp_m, outp_m):
        print('{}(*{}) -> {}'.format(key_m,
              i.decode('utf-8'), j.decode('utf-8')))


class Cache():
    """
    a redis class
    """

    def __init__(self):
        """
        initializes the class instances
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        takes a data argument and returns a string
        """

        gen = uuid.uuid4()
        self._redis.set(gen, data)

        return str(gen)

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """
        a get method that take a key string argument
        and an optional Callable argument named fn
        """
        val = self._redis.get(key)
        return val if not fn else fn(val)

    def get_int(self, key):
        """
        """
        return self.get(key, int)

    def get_str(self, key):
        """
        """
        val = self._redis.get(key)
        return val.decode("utf-8")
