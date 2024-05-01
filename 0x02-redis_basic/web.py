#!/usr/bin/env python3
""" mod's doc string """


import redis
import requests
import time
import functools
from typing import Callable


r = redis.Redis()


def dec(method: Callable) -> Callable:
    """ decorator implements caching """

    @functools.wraps(method)
    def wr(url):
        """ wrapper func """
        key = "count:" + url
        content_key = "cached:" + url
        r.incr(key)
        cached_page = r.get(content_key)
        if cached_page:
            return str(cached_page.decode("utf-8"))

        res = method(url)
        r.setex(content_key, 10, res)
        return res

    return wr


@dec
def get_page(url: str) -> str:
    """ returns a page at url"""
    res = requests.get(url)
    return res.text


if __name__ == "__main__":
    url = "https://flexrecords.cloza.tech/"
    key = "count:" + url
    for i in range(10):
        res = get_page(url)
        print(r.get(key))
        print(res[:20])
    time.sleep(5)
    res = get_page(url)
    print("===== after 5 secs =====")
    print(res[:20])
    time.sleep(5)
    res = get_page(url)
    print("===== after 10 secs =====")
    print(res[:20])
    print(r.get(key))
