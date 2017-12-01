# coding: utf-8

from redis import StrictRedis
from common.config import REDIS_CONF

_redis_client = None


def get_redis():

    global _redis_client
    if not _redis_client:
        _redis_client = StrictRedis.from_url(**REDIS_CONF)
    return _redis_client
