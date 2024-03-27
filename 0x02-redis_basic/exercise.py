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

        gen: str = (uuid.uuid4())
        self._redis.set(generate, data)
        
        return gen
