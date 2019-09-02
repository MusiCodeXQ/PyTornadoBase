import tornado.ioloop
import tornado.web
import os
import asyncio 
import asyncpg 
import redis
from tornado.options import define
from src.com.request_com import app
import re
POSTGRES_HOST = os.getenv("POSTGRES_HOST", 'localhost')
POSTGRES_USER = os.getenv("POSTGRES_USER", "db")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "db")
POSTGRES_DB = os.getenv("POSTGRES_DB", "db")

dirs = './src/handler/'
for root, dirs, files in os.walk(dirs):
    root = root.replace('./', '').replace('/', '.')
    if root[-1] != '.':
        root = root+'.'
    for file in files:
        if re.match('[a-z]*_hdl.py$', file):
            __import__(str(root+file)[:-3])

async def init_db():
    while True:
        try:
            define('pgpool', default=await asyncpg.create_pool(host=PGSQL_HOST, port=5432, user=PGSQL_USER, password=PGSQL_PSW,
                                                               database=POSTGRES_DB))
            break
        except Exception as erro:
            print(str(erro))
            await asyncio.sleep(1)
            print("init pgsql")

    while True:
        try:
            # host是redis主机，需要redis服务端和客户端都起着 redis默认端口是6379
            define('redis', default=redis.Redis("localhost"))
            break
        except Exception as erro:
            print(str(erro))
            await asyncio.sleep(1)
            print(" redis..")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init_db())
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()