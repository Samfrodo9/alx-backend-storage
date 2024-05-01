#!/usr/bin/env python3
""" mod's doc string """


from functools import wraps
import random
import string
import redis
from typing import List, Set, Dict, Tuple, Any, Union, Callable
import uuid


def replay(fn: Callable) -> None:
    """ prints out call_history od Cache.store """
    r = redis.Redis()
    input_key = fn.__qualname__ + ":inputs"
    output_key = fn.__qualname__ + ":outputs"
    inputs = r.lrange(input_key, 0, -1)
    outputs = r.lrange(output_key, 0, -1)
    matched = list(zip(inputs, outputs))
    print("Cache.store was called {} times:".format(len(matched)))
    for inp, outp in matched:
        in_out = "Cache.store(*{}) -> {}".format(inp.decode("utf-8"),
                                                 outp.decode("utf-8"))
        print(in_out)


def count_calls(method: Callable) -> Callable:
    """ a decorator that saves the no of times the
    wrapped function is called """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwds):
        self._redis.incr(key)
        return method(self, *args, **kwds)
    return wrapper


def call_history(method: Callable) -> Callable:
    """ a decorator that saves the input args of f to a list
    and output to anothr list """
    @wraps(method)
    def wrapper(self, *args, **kwds):
        # args[0]._redis.incr(f.__qualname__, 1)
        key = method.__qualname__
        self._redis.rpush(key + ":inputs", str(args))
        res = method(self, *args, **kwds)
        self._redis.rpush(key + ":outputs", res)
        return res
    return wrapper


class Cache:
    """ cache class """

    def __init__(self) -> None:
        """ class constructor """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ stores data using a rand key """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(
            self, key: str, fn: Union[Callable, None] = None
    ) -> Union[str, bytes, int, float, None]:
        """ a wrapper to redis.get to return python object """
        if fn:
            res = fn(self._redis.get(key))
            return res
        return self._redis.get(key)

    def get_int(
        self, key: str, fn: Union[Callable, None] = int
    ) -> Union[str, bytes, int, float, None]:
        """ sets self.get fn parameter with int func """
        return self.get(key, int)

    def get_str(
        self, key: str, fn: Union[Callable, None] = str
    ) -> Union[str, bytes, int, float, None]:
        """ sets self.get fn parameter with str func """
        return self.get(key, str)
