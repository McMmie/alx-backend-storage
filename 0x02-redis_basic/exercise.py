#!/usr/bin/env python3
"""
This module shows how to use redis in python
"""
import redis
from typing import Union, Callable, Optional
import uuid


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
