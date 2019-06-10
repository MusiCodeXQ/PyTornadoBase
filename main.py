import tornado.ioloop
import tornado.web
import os
import asyncio 
import asyncpg 
import aioredis
from tornado.options import define
from src.ctl.userctl import UserCtl,SmsCtl,LoginCtl

POSTGRES_HOST = os.getenv("POSTGRES_HOST", 'localhost')
POSTGRES_USER = os.getenv("POSTGRES_USER", "db")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "db")
POSTGRES_DB = os.getenv("POSTGRES_DB", "db")


async def init_db():
    while True:
        try:
            define('pgpool', default=await asyncpg.create_pool(host=POSTGRES_HOST, port=5432, user=POSTGRES_USER, password=POSTGRES_PASSWORD,
                                                               database=POSTGRES_DB))
            define('redispool',default=await aioredis.create_pool('redis://localhost'))      
            break
        except Exception:
            await asyncio.sleep(1)
            print("init pgsql & redis..")
    pass


def make_app():
    return tornado.web.Application([
        (r"/user", UserCtl),
        (r"/login", LoginCtl),
        (r"/sms/((13[0-9]|14[579]|15[0-3,5-9]|16[6]|17[0135678]|18[0-9]|19[89])\d{8}$)", SmsCtl),
        (r"/sms", SmsCtl),
        # (r"/", UserCtl),
        # (r"/", UserCtl),
    ],cookie_secret="yuxiaoqiyuanyuanruilixue",debug=True)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init_db())
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
    pass