from tornado.options import options

async def getStrFromRedis(name):
    redis=options['redispool']
    # r=redis.Redis(connection_pool=pool)
    s= await redis.execute('get',name)
    # s=r.get(name)
    return s


async def setStrToRedis(name,value,ex=None):
    redis=options['redispool']
    # r=redis.Redis(connection_pool=pool)
    s= await redis.execute('set',name,value)