import asyncio
import redis
from tornado.options import options


def get_str_from_redis(name):
    r = options['redis']
    s = r.get(name)
    return s


def set_str_to_redis(name, value, ex=None):
    r = options['redis']
    r.set(name, value, ex=ex)


def test():
    r = redis.Redis("rui.b612.site")
    r.set('key', 'value')
    key = r.get('key')
    print(key)

