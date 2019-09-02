from tornado.options import define, options

async def db_fetch(query, *args):
    pgpool = options.pgpool
    async with pgpool.acquire() as conn:
        async with conn.transaction():
            return await conn.fetch(query, *args)

async def db_execute(query, *args):
    pgpool = options.pgpool
    async with pgpool.acquire() as conn:
        async with conn.transaction():
            return await conn.execute(query, *args)

async def db_fetchrow(query, *args):
    pgpool = options.pgpool
    async with pgpool.acquire() as conn:
        async with conn.transaction():
            return await conn.fetchrow(query, *args)

async def db_fetchval(query, *args):
    pgpool = options.pgpool
    async with pgpool.acquire() as conn:
        async with conn.transaction():
            return await conn.fetchval(query, *args)

def db_limit(self)->str:
    page_size=self.get_argument('page_size',50)
    page=self.get_argument('page',1)
    sql=" limit %d offset %d"%(int(page_size),int(int(page_size)*(int(page)-1)))
    return sql

