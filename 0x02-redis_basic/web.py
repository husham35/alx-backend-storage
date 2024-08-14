#!/usr/bin/env python3
"""
A module that uses the requests module to obtain the HTML content of a
particular URL and returns it.
"""

import redis
import requests
from datetime import timedelta


def get_page(url: str) -> str:
    """
    Returns the HTML content of a particular URL
    """
    # return requests.get(url).text
    r = redis.Redis()
    key = "count:{}{}{}".format('{', url, '}')
    r.incr(key)
    res = requests.get(url)
    r.setex(url, timedelta(seconds=10), res.text)
    return res.text
