import asyncio
import sqlalchemy as sa
import asyncpgsa

metadata = sa.MetaData()
tbl = sa.Table(
    'tbl', metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('val', sa.String(255)),
)

async def create_table(conn):
    await conn.execute('DROP TABLE IF EXISTS tbl')
    await conn.execute('''CREATE TABLE tbl (
    id serial PRIMARY KEY,
    val varchar(255))''')

async def main():
    pool = await asyncpgsa.create_pool(
        host='127.0.0.1', port=15432,
        database='testing',
        user='postgres', password='helloworld',
        min_size=5, max_size=10,
    )
    async with pool.acquire() as conn:
        await create_table(conn)
    async with pool.acquire() as conn:
        await conn.execute(tbl.insert().values(val='abc'))
        for row in await conn.fetch(tbl.select()):
            print(row['id'], row['val'])

asyncio.run(main())
