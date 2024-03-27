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
    """
    @wraps(method)
    def wrapper(self, *args, **kwds):
        """
        """
        key_name = method.__qualname__
        self._redis.incr(key_name, 0) + 1
        return method(self, *args, **kwds)

    return wrapper

def call_history(method: Callable) -> Callable:
    """
    """
    @wraps(method)
    def wrapper(self, *args, **kwds):
        """
        """
        _key = method.__qualname__
        outpt = _key + ":outputs"
        inpt = _key + ":inputs"
        data = str(args)
        self._redis.rpush(inpt, data)
        methd = method(self, *args, **kwds)
        self._redis.rpush(outpt, str(methd))
        
        return methd

    return wrapper

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
