import asyncio

import aioredis
from tornado.options import options


async def get_str_from_redis(name):
    redis = options['redispool']
    # r=redis.Redis(connection_pool=pool)
    s = await redis.execute('get', name)
    # s=r.get(name)
    return s


async def set_str_to_redis(name, value, ex=None):
    redis = options['redispool']
    await redis.execute('set', name, value)
    if ex is not None:
        await redis.execute('expire', name, ex)
        pass


async def test():
    pool = await aioredis.create_pool('redis://192.168.50.210')  # host是redis主机，需要redis服务端和客户端都起着 redis默认端口是6379
    await pool.execute('set', 'key', 'value')
    key = await pool.execute('get', 'key')
    print(key)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())
